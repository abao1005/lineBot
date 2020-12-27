# ジョルダン 乗換案内
此lineBot可查詢日本境內之乘車資訊，交通工具含新幹線、JR、私鐵、地下鐵、路面電車。
參用網站: https://www.jorudan.co.jp/

A Line bot based on a finite state machine

## Finite State Machine
![fsm](./img/fsm.png)

## Usage
一開始的state是 `initial`，
打任意文字之後，會從 `initial` 到 `start`
* `start` : 選擇服務項目。
	* 顯示畫面: 
		<div align="left">
			<img src="./img/start.jpg" width="40%" height = "40%">
		</div>
	* 點擊: "轉乘資訊"，進到下一個state `depart_arrive`。
		<div align="left">
			<img src="./img/depart_arrive.jpg" width="40%" height = "40%">
		</div>
	* 點擊: "我要直接看網頁!"，開啟此程式主要應用web crawler的網頁。

* `depart_arrive` : 選擇查詢出發or抵達時間
	* 顯示畫面: 
		<div align="left">
			<img src="./img/depart_arrive2.jpg" width="40%" height = "40%">
		</div>
	* 點擊: "出發"，進到下一個state `time`。
		<div align="left">
			<img src="./img/depart.jpg" width="40%" height = "40%">
		</div>
	* 點擊: "抵達"，進到下一個state `time`。
		<div align="left">
			<img src="./img/arrive.jpg" width="40%" height = "40%">
		</div>

* `time` : 輸入欲查詢時間
	* 顯示畫面:
		<div align="left">
			<img src="./img/time.jpg" width="40%" height = "40%">
		</div>
	* 點擊: "請選擇日期與時間"。
		<div align="left">
			<img src="./img/time_scroll.jpg" width="40%" height = "40%">
		</div>
	* 點擊: "傳送"，進到下一個state `station`。
		<div align="left">
			<img src="./img/time_decide.jpg" width="40%" height = "40%">
		</div>

* `station` : 輸入起訖站名
	* 顯示畫面:
		<div align="left">
			<img src="./img/station.jpg" width="40%" height = "40%">
		</div>
	* 輸入: 札幌 菊川 (敘述完整之兩站名)，
	經由state `get_station` 爬蟲判斷其完整後，進到下個state `show`。
		<div align="left">
			<img src="./img/complete.jpg" width="40%" height = "40%">
		</div>
	* 輸入: 弘明寺 東雲 (敘述不完整之兩站名)，
	經由state `get_station` 爬蟲判斷其不完整後，進到下個state `kouho`。
		<div align="left">
			<img src="./img/incomplete.jpg" width="40%" height = "40%">
		</div>

* `show` : 爬蟲並顯示轉乘資訊
	* 顯示畫面:
		<div align="left">
			<img src="./img/show.jpg" width="40%" height = "40%">
		</div>
		<div align="left">
			<img src="./img/show2.jpg" width="40%" height = "40%">
		</div>
	* 點擊: "謝謝"，回到原本的state `start`。
		<div align="left">
			<img src="./img/thanks.jpg" width="40%" height = "40%">
		</div>

* `kouho` :列出建議起迄站，供用戶選擇
	* 顯示畫面:
		<div align="left">
			<img src="./img/kouho.jpg" width="40%" height = "40%">
		</div>
	* 選擇起訖站後，經 `tmp` `tmp2` 兩states，爬蟲並顯示轉乘資訊。
		<div align="left">
			<img src="./img/show3.jpg" width="40%" height = "40%">
		</div>
		<div align="left">
			<img src="./img/show4.jpg" width="40%" height = "40%">
		</div>
	* 點擊: "謝謝"，回到原本的state `start`。
		<div align="left">
			<img src="./img/thanks2.jpg" width="40%" height = "40%">
		</div>

```sh
  所有state皆可藉由輸入"重新查詢"，回到state `start`。
```
<div align="left">
	<img src="./img/restart.jpg" width="40%" height = "40%">
</div>


## 程式特色


## 心得
此次計算理論課程之期末project讓我學習到非常多東西，了解到如何以FSM來控制程式流程、認識到如何製作一個LineBot聊天室、也學會了一些網路爬蟲的基礎。
過往時常都是使用C++來寫學校功課，而此次作業因為大量接觸python，做完後我才更認識到他的功能之強大。
程式中引用了許多套件，如linebot、beautifulsoup4等等，開發過程也使用了line developer的flex message simulator。以上種種方便好用的工具，都是前人辛苦開發的基業，能夠使用這些工具來寫程式，真的是我莫大的榮幸。寫程式的過程十分感動，總會想著:「如果沒有這些強大的工具該怎麼辦」。
程式的主題也是自己很喜歡的主題，因為日本的交通網路非常複雜，所以想著如果有個程式可以輸入起點終點，就告訴用戶該怎麼走、如何轉乘，那就太好了。剛好，因緣際會發現了 https://www.jorudan.co.jp/ 這個網站，於是倚仗著他，我用網路爬蟲實現了這樣的一個聊天室。
開發的過程中很有成就感，每完成一個小功能，看到lineBot有如想像中的回覆，就總能開心個好幾分鐘。

## Reference
https://github.com/NCKU-CCS/TOC-Project-2020/blob/master/README.md
https://www.youtube.com/watch?v=9Z9xKWfNo7k&ab_channel=%E5%BD%AD%E5%BD%AD%E7%9A%84%E8%AA%B2%E7%A8%8B
https://www.youtube.com/watch?v=vsxZ_4sFWoU&t=313s&ab_channel=Maso%E7%9A%84%E8%90%AC%E4%BA%8B%E5%B1%8B
https://ithelp.ithome.com.tw/articles/10229719
https://ithelp.ithome.com.tw/articles/10195640
https://blog.gtwang.org/programming/python-beautiful-soup-module-scrape-web-pages-tutorial/2/
https://www.jorudan.co.jp/
https://developers.line.biz/flex-simulator/?status=success
https://stackoverflow.com/ <3


