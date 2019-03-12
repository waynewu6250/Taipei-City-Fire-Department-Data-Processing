# 週報SOP
三個部分須製作: <br>
1. 局報,週報會議資料每週統計數據: 局報, 週報資料數據
2. 受理火災word
3. 局報,週報會議資料每週統計數據: 滿意度調查表

## 1. 局報,週報會議資料每週統計數據: 局報, 週報資料數據
1. 檔案位置: <br>
Ｏ槽->共用統計資料夾->役男給的資料放這裡->週報資料->108年->局報,週報會議資料每週統計數據->建立新檔案: ex.0303-0309局報,週報會議資料每週統計數據
2. 更改日期, 選擇局報,週報資料數據tab, 將資料清空
3. 桌面->jupyter打開->Documents->scraping->week.ipynb打開檔案, 進入按shift+enter執行, 第一個block先執行, 等待左側數字出現代表ok, 在執行第二個block (要記得改日期, date=..., mth=...)
(跨月份的話: 先執行月底, 記得修改天數num, 然後到下載把檔案清空, 改月份在修改天數num執行月初)
4. 等程式跑完, 會同時打開7個檔案 1,2,3,4,5,6,7.xlsx, 接著回到局報,週報會議資料每週統計數據.xlsx, 選擇開發人員->Visual Basic->左側ThisWorkbook點開->按下綠色箭頭->執行
5. 儲存檔案, 按住shift關掉excel可以一次全部關掉
6. 第四欄緊急傷病救護案件: 按下鍵盤: scroll Lock兩次+4, 切換到第四台電腦->一樣進入智派系統->案件維護->日報上傳消防署->選擇日期紀錄救護次數->填入excel

## 2. 受理火災word
1. 檔案位置: <br>
Ｏ槽->共用統計資料夾->役男給的資料放這裡->週報資料->108年->受理火災word->fire_post.xls
2. 修改日期->把資料清除
3. 回到剛剛week.ipynb, 執行第三個block (要記得改日期, date=..., month=...)
4. 每次下載檔案後要記得把跳出的視窗關掉, 才會進行下一次檔案下載, 否則會卡住要重來
5. 等程式跑完, 會同時打開7個檔案 1,2,3,4,5,6,7.xlsx, 選擇開發人員->Visual Basic->左側ThisWorkbook點開->按下綠色箭頭->執行
6. 把合計數字copy, 在旁邊貼上值, 再轉置貼到下面對應的日期, 以供之後日報使用
7. 回到週報資料->108年->受理火災word->建立新的word檔->把剛剛跑完的資料複製直接貼上word

## 3. 局報,週報會議資料每週統計數據: 滿意度調查表
1. Ｏ槽->共用統計資料夾->役男給的資料放這裡->週報資料->108年->滿意度: 將資料複製到局報,週報會議資料每週統計數據: 滿意度調查表貼上
2. 把電話貼到fire_post->satisfaction tab, 複製跑好的程式貼回原本的電話欄, 稍微修改一下後面滿意度的地方

------------------------------
# 每日SOP