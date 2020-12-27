from transitions.extensions import GraphMachine
from utils import *
import urllib.request as req
import os
import bs4
import urllib.parse


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.departure = -1  # 0:出發 1:抵達
        self.time = ""
        self.yr = ""
        self.month = ""
        self.day = ""
        self.hr = ""
        self.min = ""
        self.eki = ""
        self.canShow = -1
        self.eki1_ready = False
        self.eki2_ready = False

    def is_going_to_depart_or_arrive(self, event):
        text = event.message.text
        return text == "我要搭車啦!幫我查查"

    def is_going_to_time(self, event):
        text = event.message.text
        if text == "出發":
            self.departure = 0
        elif text == "抵達":
            self.departure = 1
        return text == "出發" or text == "抵達"

    def is_going_to_station(self, event):
        if event.postback.params["datetime"] != None:
            self.time = event.postback.params["datetime"]
        else:
            return False
        if (self.time.count('-') == 2) and (self.time.count('T') == 1 or self.time.count('t') == 1) and (self.time.count(":") == 1) and (len(self.time) == 16):
            # 2020-01-01T23:50
            self.yr = self.time[:4]
            self.month = self.time[5:-9]
            self.day = self.time[8:-6]
            self.hr = self.time[11:-3]
            self.min = self.time[-2:]
            return True
        else:
            return False

    def is_going_to_get_station(self, event):
        text = event.message.text
        if text.count(' ') == 1:
            self.eki = text.split(' ')
            return True
        else:
            return False

    def is_going_to_show(self, event):
        if self.canShow == 1:
            return True
        else:
            return False

    def is_going_to_kouho(self, event):
        if self.canShow == 0:
            return True
        else:
            return False

    def is_go_back(self, event):
        text = event.message.text
        return text == "謝謝!"

    def is_restart(self, event):
        text = event.message.text
        return text == "重新查詢"

    def is_going_to_tmp(self, event):
        if event.postback.data.find("station1") != -1:
            return True
        elif event.postback.data.find("station2") != -1:
            return True
        elif event.postback.data.find("none") != -1:
            return False
        else:
            return False

    def is_going_to_tmp2(self, event):
        if event.postback.data.find("station1") != -1:
            return True
        elif event.postback.data.find("station2") != -1:
            return True
        elif event.postback.data.find("none") != -1:
            return False
        else:
            return False

    def on_enter_tmp2(self, event):
        reply_token = event.reply_token
        if event.postback.data.find("station1") != -1:
            self.eki[0] = event.postback.data.strip("station1")
            self.eki1_ready = True
            #send_text_message(reply_token, "您選擇起站:"+self.eki[0])
        elif event.postback.data.find("station2") != -1:
            self.eki[1] = event.postback.data.strip("station2")
            self.eki2_ready = True
            #send_text_message(reply_token, "您選擇迄站:"+self.eki[1])
        if self.eki1_ready and self.eki2_ready:
            url = 'https://www.jorudan.co.jp/norikae/cgi/nori.cgi?eki1='+urllib.parse.quote(self.eki[0])+'&eki2='+urllib.parse.quote(
                self.eki[1])+'&eki3=&via_on=1&Dym='+str(self.yr)+str(self.month)+'&Ddd='+str(self.day)+'&Dhh='+str(self.hr)+'&Dmn1='+str(self.min)[:1]+'&Dmn2='+str(self.min)[-1:]+'&Cway='+str(self.departure)+'&Cfp=2&Czu=2&C7=1&C2=0&C3=0&C1=0&C4=0&C6=2&S='+urllib.parse.quote("検索")+'&Cmap1=&rf=nr&pg=0&eok1=&eok2=R-&eok3=&Csg=1'
            request = req.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
            with req.urlopen(request) as response:
                data = response.read().decode("utf-8")
            root = bs4.BeautifulSoup(data, "html.parser")
            route_first = root.find("div", class_="bk_result", id="bR1")

            date = root.find("div", class_="h_big").h2.em.string.split(" ")[0]
            ekis = route_first.find_all("td", class_="nm")
            rosens = route_first.find_all("td", class_="rn")
            noriTimes = route_first.find_all("td", class_="tm")
            trainTypes = route_first.find_all("td", class_="gf")
            timings = route_first.find("div", class_="data_tm").find_all("b")

            money = route_first.find(
                "dd", attrs={'id': 'bR1_total_KIP'}).b.string
            total_time = route_first.find(
                "dl", class_="data_total-time").dd.b.string
            total_nori_time = route_first.find("div", class_="data").find(
                "dt", string="乗車時間").find_parent("dl").dd.b.string
            norikae_num = route_first.find(
                "dl", class_="data_norikae-num").dd.b.string
            if route_first.find("div", class_="data").find(
                    "dt", string="距離") != None:
                distance = route_first.find("div", class_="data").find(
                    "dt", string="距離").find_parent("dl").dd.b.string
            else:
                distance = ""

            list_timing = []
            list_eki = []
            list_rosen = []
            list_noriTime = []
            list_type = []

            for element in timings:
                list_timing.append(element.string)
            for eki in ekis:
                if eki.strong.a != None:
                    list_eki.append(eki.strong.a.string.strip("\n"))
                else:
                    list_eki.append(eki.strong.string.strip("\n"))
            for rosen in rosens:
                if rosen.div.a != None:
                    list_rosen.append(rosen.div.a.string.strip("\n"))
                else:
                    list_rosen.append(rosen.div.string.strip("\n"))
            for noriTime in noriTimes:
                if noriTime.b != None:
                    list_noriTime.append(noriTime.b.string.strip("\n"))
            for trainType in trainTypes:
                if trainType.img != None:
                    list_type.append(trainType.img.get("src"))

            a_list = [
                {
                    "type": "text",
                    "text": date + " "+list_timing[0]+"発 "+"→"+" "+list_timing[2]+"着",
                    "color": "#b7b7b7",
                    "size": "xs"
                },
                {
                    "type": "text",
                    "text": "総額 " + money,
                    "color": "#b7b7b7",
                    "size": "xs"
                },
                {
                    "type": "text",
                    "text": "所要時間："+total_time,
                    "color": "#b7b7b7",
                    "size": "xs"
                },
                {
                    "type": "text",
                    "text": "乗車時間："+total_nori_time,
                    "color": "#b7b7b7",
                    "size": "xs"
                },
                {
                    "type": "text",
                    "text": "乗換"+norikae_num+"   距離："+distance,
                    "color": "#b7b7b7",
                    "size": "xs"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                            {
                                "type": "filler"
                            },
                        {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "filler"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [],
                                        "cornerRadius": "30px",
                                        "height": "12px",
                                        "width": "12px",
                                        "borderColor": "#EF454D",
                                        "borderWidth": "2px"
                                    },
                                    {
                                        "type": "filler"
                                    }
                                ],
                                "flex": 0,
                                "offsetStart": "-10px"
                        },
                        {
                                "type": "text",
                                "text": list_eki[0],
                                "gravity": "center",
                                "flex": 4,
                                "size": "sm",
                                "offsetStart": "-15px"
                        }
                    ],
                    "spacing": "lg",
                    "cornerRadius": "30px",
                    "margin": "xl"
                }]
            i = 0
            for i in range(0, len(list_rosen)):
                a_list.append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": list_noriTime[i].split("-")[0].strip("(").strip(")"),
                                        "size": "xxs",
                                        "offsetTop": "10px"
                                    },
                                    {
                                        "type": "text",
                                        "text": "|",
                                        "offsetTop": "10px",
                                        "size": "xxs",
                                        "offsetStart": "15px"
                                    },
                                    {
                                        "type": "text",
                                        "text": list_noriTime[i].split("-")[1].strip("(").strip(")"),
                                        "size": "xxs",
                                        "offsetTop": "10px"
                                    }
                                ],
                                "width": "35px"
                            },
                        {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "filler"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [],
                                                "width": "2px",
                                                "backgroundColor": "#B7B7B7"
                                            },
                                            {
                                                "type": "filler"
                                            }
                                        ],
                                        "flex": 1
                                    }
                                ],
                                "width": "12px"
                                },
                        {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "filler"
                                    },
                                    {
                                        "type": "image",
                                        "url": "https://www.jorudan.co.jp"+list_type[i]
                                    },
                                    {
                                        "type": "filler"
                                    }
                                ],
                                "height": "70px",
                                "width": "40px"
                                },
                        {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "filler"
                                    },
                                    {
                                        "type": "text",
                                        "text": list_rosen[i],
                                        "wrap": True,
                                        "size": "xs"
                                    },
                                    {
                                        "type": "filler"
                                    }
                                ]
                                }
                    ],
                    "spacing": "lg",
                    "height": "70px"
                })
                a_list.append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                            {
                                "type": "filler"
                            },
                        {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "filler"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [],
                                        "cornerRadius": "30px",
                                        "width": "12px",
                                        "height": "12px",
                                        "borderWidth": "2px",
                                        "borderColor": "#6486E3"
                                    },
                                    {
                                        "type": "filler"
                                    }
                                ],
                                "flex": 0,
                                "offsetStart": "-10px"
                            },
                        {
                                "type": "text",
                                "text": list_eki[i+1],
                                "gravity": "center",
                                "flex": 4,
                                "size": "sm",
                                "offsetStart": "-15px"
                            }
                    ],
                    "spacing": "lg",
                    "cornerRadius": "30px"
                })

            send_norigae_message(reply_token, a_list, self.eki[0], self.eki[1])

    def on_enter_tmp(self, event):
        reply_token = event.reply_token
        if event.postback.data.find("station1") != -1:
            self.eki[0] = event.postback.data.strip("station1")
            self.eki1_ready = True
            send_text_message(reply_token, "您選擇起站:"+self.eki[0])
        elif event.postback.data.find("station2") != -1:
            self.eki[1] = event.postback.data.strip("station2")
            self.eki2_ready = True
            send_text_message(reply_token, "您選擇迄站:"+self.eki[1])

    def on_enter_depart_or_arrive(self, event):
        reply_token = event.reply_token
        send_ask_DorA_message(reply_token)

    def on_enter_station(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "您輸入的時間為:\n"
                          + self.yr+"/"+self.month+"/"+self.day+" "+self.hr + ":"+self.min+"\n\n" +
                          "請輸入起訖站名(兩站以空格隔開)。\n" +
                          "或輸入<重新查詢>以重置時間。")

    def on_enter_time(self, event):
        reply_token = event.reply_token
        if self.departure == 0:
            send_template_message(reply_token, "出發")
        elif self.departure == 1:
            send_template_message(reply_token, "抵達")

    def on_enter_get_station(self, event):
        # 爬蟲!看寫的夠不夠仔細，如果夠，canShow =1，反之
        url = 'https://www.jorudan.co.jp/norikae/cgi/nori.cgi?eki1='+urllib.parse.quote(self.eki[0])+'&eki2='+urllib.parse.quote(
            self.eki[1])+'&eki3=&via_on=1&Dym='+str(self.yr)+str(self.month)+'&Ddd='+str(self.day)+'&Dhh='+str(self.hr)+'&Dmn1='+str(self.min)[:1]+'&Dmn2='+str(self.min)[-1:]+'&Cway='+str(self.departure)+'&Cfp=2&Czu=2&C7=1&C2=0&C3=0&C1=0&C4=0&C6=2&S='+urllib.parse.quote("検索")+'&Cmap1=&rf=nr&pg=0&eok1=&eok2=R-&eok3=&Csg=1'
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        root = bs4.BeautifulSoup(data, "html.parser")
        isKouho = root.find("title", string="出発地・到着地の確認｜乗換案内｜ジョルダン")
        if isKouho == None:
            self.canShow = 1
            self.advance(event)
        else:
            self.canShow = 0
            self.advance(event)

    def on_enter_show(self, event):
        reply_token = event.reply_token
        url = 'https://www.jorudan.co.jp/norikae/cgi/nori.cgi?eki1='+urllib.parse.quote(self.eki[0])+'&eki2='+urllib.parse.quote(
            self.eki[1])+'&eki3=&via_on=1&Dym='+str(self.yr)+str(self.month)+'&Ddd='+str(self.day)+'&Dhh='+str(self.hr)+'&Dmn1='+str(self.min)[:1]+'&Dmn2='+str(self.min)[-1:]+'&Cway='+str(self.departure)+'&Cfp=2&Czu=2&C7=1&C2=0&C3=0&C1=0&C4=0&C6=2&S='+urllib.parse.quote("検索")+'&Cmap1=&rf=nr&pg=0&eok1=&eok2=R-&eok3=&Csg=1'
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        root = bs4.BeautifulSoup(data, "html.parser")
        route_first = root.find("div", class_="bk_result", id="bR1")

        date = root.find("div", class_="h_big").h2.em.string.split(" ")[0]
        ekis = route_first.find_all("td", class_="nm")
        rosens = route_first.find_all("td", class_="rn")
        noriTimes = route_first.find_all("td", class_="tm")
        trainTypes = route_first.find_all("td", class_="gf")
        timings = route_first.find("div", class_="data_tm").find_all("b")

        money = route_first.find("dd", attrs={'id': 'bR1_total_KIP'}).b.string
        total_time = route_first.find(
            "dl", class_="data_total-time").dd.b.string
        total_nori_time = route_first.find("div", class_="data").find(
            "dt", string="乗車時間").find_parent("dl").dd.b.string
        norikae_num = route_first.find(
            "dl", class_="data_norikae-num").dd.b.string
        if route_first.find("div", class_="data").find(
                "dt", string="距離") != None:
            distance = route_first.find("div", class_="data").find(
                "dt", string="距離").find_parent("dl").dd.b.string
        else:
            distance = ""

        list_timing = []
        list_eki = []
        list_rosen = []
        list_noriTime = []
        list_type = []

        for element in timings:
            list_timing.append(element.string)
        for eki in ekis:
            if eki.strong.a != None:
                list_eki.append(eki.strong.a.string.strip("\n"))
            else:
                list_eki.append(eki.strong.string.strip("\n"))
        for rosen in rosens:
            if rosen.div.a != None:
                list_rosen.append(rosen.div.a.string.strip("\n"))
            else:
                list_rosen.append(rosen.div.string.strip("\n"))
        for noriTime in noriTimes:
            if noriTime.b != None:
                list_noriTime.append(noriTime.b.string.strip("\n"))
        for trainType in trainTypes:
            if trainType.img != None:
                list_type.append(trainType.img.get("src"))

        a_list = [
            {
                "type": "text",
                "text": date + " "+list_timing[0]+"発 "+"→"+" "+list_timing[2]+"着",
                "color": "#b7b7b7",
                "size": "xs"
            },
            {
                "type": "text",
                "text": "総額 " + money,
                "color": "#b7b7b7",
                "size": "xs"
            },
            {
                "type": "text",
                "text": "所要時間："+total_time,
                "color": "#b7b7b7",
                "size": "xs"
            },
            {
                "type": "text",
                "text": "乗車時間："+total_nori_time,
                "color": "#b7b7b7",
                "size": "xs"
            },
            {
                "type": "text",
                "text": "乗換"+norikae_num+"   距離："+distance,
                "color": "#b7b7b7",
                "size": "xs"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                        {
                            "type": "filler"
                        },
                    {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [],
                                    "cornerRadius": "30px",
                                    "height": "12px",
                                    "width": "12px",
                                    "borderColor": "#EF454D",
                                    "borderWidth": "2px"
                                },
                                {
                                    "type": "filler"
                                }
                            ],
                            "flex": 0,
                            "offsetStart": "-10px"
                    },
                    {
                            "type": "text",
                            "text": list_eki[0],
                            "gravity": "center",
                            "flex": 4,
                            "size": "sm",
                            "offsetStart": "-15px"
                    }
                ],
                "spacing": "lg",
                "cornerRadius": "30px",
                "margin": "xl"
            }]
        i = 0
        for i in range(0, len(list_rosen)):
            a_list.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": list_noriTime[i].split("-")[0].strip("(").strip(")"),
                                    "size": "xxs",
                                    "offsetTop": "10px"
                                },
                                {
                                    "type": "text",
                                    "text": "|",
                                    "offsetTop": "10px",
                                    "size": "xxs",
                                    "offsetStart": "15px"
                                },
                                {
                                    "type": "text",
                                    "text": list_noriTime[i].split("-")[1].strip("(").strip(")"),
                                    "size": "xxs",
                                    "offsetTop": "10px"
                                }
                            ],
                            "width": "35px"
                        },
                    {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [],
                                            "width": "2px",
                                            "backgroundColor": "#B7B7B7"
                                        },
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "flex": 1
                                }
                            ],
                            "width": "12px"
                            },
                    {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "image",
                                    "url": "https://www.jorudan.co.jp"+list_type[i]
                                },
                                {
                                    "type": "filler"
                                }
                            ],
                            "height": "70px",
                            "width": "40px"
                            },
                    {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "text",
                                    "text": list_rosen[i],
                                    "wrap": True,
                                    "size": "xs"
                                },
                                {
                                    "type": "filler"
                                }
                            ]
                            }
                ],
                "spacing": "lg",
                "height": "70px"
            })
            a_list.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                        {
                            "type": "filler"
                        },
                    {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [],
                                    "cornerRadius": "30px",
                                    "width": "12px",
                                    "height": "12px",
                                    "borderWidth": "2px",
                                    "borderColor": "#6486E3"
                                },
                                {
                                    "type": "filler"
                                }
                            ],
                            "flex": 0,
                            "offsetStart": "-10px"
                        },
                    {
                            "type": "text",
                            "text": list_eki[i+1],
                            "gravity": "center",
                            "flex": 4,
                            "size": "sm",
                            "offsetStart": "-15px"
                        }
                ],
                "spacing": "lg",
                "cornerRadius": "30px"
            })

        send_norigae_message(reply_token, a_list, self.eki[0], self.eki[1])
        # self.go_back(event)

    def on_enter_kouho(self, event):
        reply_token = event.reply_token
        url = 'https://www.jorudan.co.jp/norikae/cgi/nori.cgi?eki1='+urllib.parse.quote(self.eki[0])+'&eki2='+urllib.parse.quote(
            self.eki[1])+'&eki3=&via_on=1&Dym='+str(self.yr)+str(self.month)+'&Ddd='+str(self.day)+'&Dhh='+str(self.hr)+'&Dmn1='+str(self.min)[:1]+'&Dmn2='+str(self.min)[-1:]+'&Cway='+str(self.departure)+'&Cfp=2&Czu=2&C7=1&C2=0&C3=0&C1=0&C4=0&C6=2&S='+urllib.parse.quote("検索")+'&Cmap1=&rf=nr&pg=0&eok1=&eok2=&eok3=&Csg=1'
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        root = bs4.BeautifulSoup(data, "html.parser")
        kouhoBody = root.find("div", class_="body kouho")
        kouho_Ss = kouhoBody.find(
            "select", attrs={'name': 'eki1'}).find_all("option")

        root = bs4.BeautifulSoup(data, "html.parser")
        kouhoBody = root.find("div", class_="body kouho")
        kouho_Es = kouhoBody.find(
            "select", attrs={'name': 'eki2'}).find_all("option")
        list_S = []
        list_E = []

        for kouho_S in kouho_Ss:
            list_S.append(kouho_S.string)
        for kouho_E in kouho_Es:
            list_E.append(kouho_E.string)

        send_kouho_message(
            reply_token, self.eki[0], self.eki[1], list_S, list_E)
        print(kouho_Ss)
        print(kouho_Es)
        # def on_exit_state2(self):
        #    print("Leaving state2")

    def on_enter_start(self, event):
        reply_token = event.reply_token
        send_welcome_message(reply_token)
        self.departure = -1  # 0:出發 1:抵達
        self.time = ""
        self.yr = ""
        self.month = ""
        self.day = ""
        self.hr = ""
        self.min = ""
        self.eki = ""
        self.canShow = -1
        self.eki1_ready = False
        self.eki2_ready = False
