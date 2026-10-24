# 00 製作總表

> 一眼看完：有哪些版本、哪些還在發展、影片在哪裡、下一步做什麼。
> 每次工作結束時更新這張表。

## 主線（`04_active/`）

| # | 版本 | 狀態 | 影片 | 下一步 |
|---|---|---|---|---|
| 09 | 九個階段 2D・20 分鐘 | 🟡 等真實錄音 | README_nine_stages_full_light.mp4（49 MB） | 用真實朗讀時間重算 |
| 10 | 聲音即時互動 | 🟡 待實測 | 無（網頁） | 戴耳機實際朗讀，調語速、靈敏度 |
| 12 | 3D・同一條規則・1 分鐘 | 🟢 方向確定 | README_nine_stages_3d_v2_60s.mp4（49 MB） | 作為 13 的試驗場 |
| 13 | 3D・20 分鐘 | 🟡 未滿意 | README_nine_stages_3d_full_light.mp4（571 MB，1080p）／preview720（96 MB） | 待作者提出調整；接真實錄音 |
| 14 | 圖片切割 3D・30 秒 | 🟡 試作 | README_image_patches_3d_30s.mp4（14 MB） | 決定要不要做長版、和信的哪段呼應 |

狀態：🟢 方向確定　🟡 進行中／待決定　⚪ 封存

## 封存（`90_archive/`）

| # | 版本 | 被什麼取代 | 影片 |
|---|---|---|---|
| 01 | token PDF | 仍是有效成品（PDF 在資料夾內） | — |
| 02 | 動態原型（黑底） | 後續所有版本的基準 | README_token_prototype.mp4 |
| 03 | 直式清單 | 04 | README_token_vertical.mp4 |
| 04 | 原型直式 | 05 | README_token_prototype_vertical_dark／light.mp4 |
| 05 | 模擬 AI 讀信（直式） | 06 | README_token_read_dark／light.mp4、_full_dark／light.mp4 |
| 06 | 橫式・閃爍→曲線 | 07 | README_token_land_light_300s.mp4 |
| 07 | 細線逐條生長 | 08 | README_token_fog_light_30s／54s.mp4 |
| 08 | 九個階段 1 分鐘 v1、v2 | 09 | README_nine_stages_light_60s.mp4、_v2_light_60s.mp4 |
| 11 | 3D 第一版 | 12（過渡太隨性） | README_nine_stages_3d_60s.mp4（166 MB）／preview（74 MB） |

## 影片保存

- 影片不進 git，由作者自行保存。上表的檔名就是對照。
- 影片都可以用各版本資料夾的腳本重新算出來，輸出到 `out/`。

## 下一步（依優先順序）

### 來自錄像（readme-video 決策 07，2026-10-23）

動畫成為錄像第三章「打開我」的一部分，見 [readme-video 決策 07](https://github.com/wufangci/readme-video/blob/main/06_process/DECISIONS.md)、[第三章說明](https://github.com/wufangci/readme-video/blob/main/04_active/03-inside-ai/README.md)。

- [ ] **A 段約 2 分鐘**：把 13（20 分鐘）壓成九個階段的 2 分鐘版，白底。**11/1 demo 前要有。**
- [ ] **B 段並排回顧約 30 秒**：信的 token、14 圖片切割的臉（第一章被切成 576 塊）、第二章跳出信的畫面，放在同一個 3D 空間 → 第九階段「遺忘」（Δweights = 0）全部靜止。demo 可先做簡版。
- [ ] **C 段朗讀約 3 分鐘**（來自 [readme-video 決策 14](https://github.com/wufangci/readme-video/blob/main/06_process/DECISIONS.md)：朗讀改為信的結尾，第 5 段 vakai aken 到署名，383 字）：token 只在作者說話時變形，聲音停下畫面就停。demo 用 10 聲音互動邊唸邊螢幕錄影；正式版改吃錄好的音檔。
- [ ] **誠實標示**：畫面角落「分詞示意：GPT-4o（o200k_base）」。分詞器只是示意，不指稱特定 AI。
- [ ] （MIT 授權，螢幕錄影加來源標註；見 [readme-video 決策 12](https://github.com/wufangci/readme-video/blob/main/06_process/DECISIONS.md)）A 段第 5–7 階段旁浮出 [LLM Visualization](https://bbycroft.net/llm) 小窗。

### 原本的下一步

1. 調整 3D 動畫，直到滿意（13 為主，12 用來快速試驗）。
2. 錄製朗讀，產生真實時間表，取代 `02_timeline/timing.json` 的估計值。
3. 實測 10 聲音互動。
4. 決定 14 圖片版的定位。
