# yk_GetYahooWeather
<span style="color:red;">__These programs run only Japanese environment.__</style>

## Abstract
[Yahoo!天気・災害](https://weather.yahoo.co.jp/weather/)から発信される情報から、任意の地域の3時間ごとの天気情報を取得し、pythonのTkinter Windowに表示させます。

## Requirements (Software 必要なプログラム)
* python3 (equial or more than version 3.7)

## Requirements (python libraries 必要なpython外部ライブラリ)
* beautifulsoup4>=4.12.2
* requests>=2.31.0

## Usage (使い方)
1. Launcher.batをダブルクリックするか、ターミナル上で実行します。
2. 取得対象の地域名の一部を入力してEnterを押します。市町村名の入力を推奨します。
3. 候補の地域一覧から、取得したい地域の番号を入力してEnterを押します。"戻る"の番号を入力すると地域名入力に戻ります。"戻る"しか表示されない場合、別の地域名(対象の地域を含むより広い地域名など)をお試しください。
4. Tkinter Windowに3時間ごとの天気予報が表示されます。