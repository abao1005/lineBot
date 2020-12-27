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


## 
## Reference
https://github.com/NCKU-CCS/TOC-Project-2020/blob/master/README.md
https://www.youtube.com/watch?v=9Z9xKWfNo7k&ab_channel=%E5%BD%AD%E5%BD%AD%E7%9A%84%E8%AA%B2%E7%A8%8B
https://www.youtube.com/watch?v=vsxZ_4sFWoU&t=313s&ab_channel=Maso%E7%9A%84%E8%90%AC%E4%BA%8B%E5%B1%8B
https://ithelp.ithome.com.tw/articles/10229719
https://ithelp.ithome.com.tw/articles/10195640
https://blog.gtwang.org/programming/python-beautiful-soup-module-scrape-web-pages-tutorial/2/
https://www.jorudan.co.jp/
of course https://stackoverflow.com/ <3


