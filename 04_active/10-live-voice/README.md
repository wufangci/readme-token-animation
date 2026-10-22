# 10 — 聲音即時互動

`README_live.html` 是獨立網頁，資料都內嵌在裡面。用 Chrome 開啟，按「開始」並允許麥克風：先安靜 1 秒讓它聽環境聲，之後開口畫面就動，停下就停。聲音只在本機計算音量，不錄音、不上傳。

選用按鍵：空白／→ 對齊下一段、← 上一段、↑↓ 語速、[ ] 靈敏度、A 段落等待、H 狀態列、S 模擬說話、F 全螢幕、R 重來。

如果 Chrome 不讓 file:// 使用麥克風，在這個資料夾執行 `python3 -m http.server`，再開 http://localhost:8000/README_live.html 。

`README_live_v1.html` 是第一版，門檻寫死、要一直按空白鍵，保留作為紀錄。

## 指令（在 repo 根目錄執行）

```bash
python3 04_active/10-live-voice/test_live2.py     # 用 fake_voice.wav 模擬說話與停頓，檢查游標是否跟著動
```

輸出寫到 `out/`。

## 截圖

見 `stills/`。

過程與決定見 [`06_process/DECISIONS.md`](../../06_process/DECISIONS.md)。
