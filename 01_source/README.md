# 01_source — 原著與設定

| 檔案 | 內容 |
|---|---|
| `data/zh.json` | 信的 5,366 個 token：`{id, bytes, str}`；`str` 為 `null` 時是位元組碎片 |
| `data/links.json` | 作者從信裡挑的 8 組連線：你、照片、孩子、聲音、Ljaugiya、族名、十歲、家 |
| `data/anim_data.json`、`data/anim_v_data.json` | 早期原型（02、04）用的資料 |
| `SPECS.md` | 分詞器、CLIP 規格與說明牌用語 |

## 信的來源

- [wufangci/README](https://github.com/wufangci/README) 的 `LETTER.md`，commit `93edfdd`。
- 信改版時要重新切 token：`node 05_tools/tokenize.js path/to/LETTER.md 01_source/data/zh.json`，接著重算時間表（見 `02_timeline/`）。
