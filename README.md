# readme-token-animation

這個 repo 是〈README：一封寫給人工智慧的家書〉系列裡的「AI 如何讀這封信」視覺化，放的是 token 動畫的過程與各版本。

作品本體（信與 skill）在 [wufangci/README](https://github.com/wufangci/README)。這裡放的是把那封信拆成 token、再一步步視覺化成影像的過程：每個版本的程式、資料、截圖，以及每次修改背後的決定。

- **影片**：放在 [Releases](https://github.com/wufangci/readme-token-animation/releases)，每個版本對應一個 tag。
- **過程**：整理在 [`DECISIONS.md`](DECISIONS.md)，記錄每一版的要求、回饋、決定和理由。

## 數字

| | |
|---|---|
| 信（中文） | 5,945 字、17,229 bytes |
| 分詞器 | GPT-4o `o200k_base`（[gpt-tokenizer](https://www.npmjs.com/package/gpt-tokenizer) 2.9.0） |
| token | 5,366 個，其中 814 個是無法單獨成字的位元組碎片 |
| 詞彙表 | 199,998 |

資料來源：`data/zh.json` 是由 wufangci/README 的 `LETTER.md`（commit `93edfdd`）切出來的。程式會先去掉第一行的語言切換連結再切。

## 版本

| # | 資料夾 | 內容 | tag |
|---|---|---|---|
| 01 | `01-token-pdf` | 把信拆成 token 的 PDF（22 頁） | `v01-token-pdf` |
| 02 | `02-prototype` | 第一個動態原型：字 → token → ID | `v02-prototype` |
| 03 | `03-vertical-list` | 直式白底，token 與 ID 清單 | `v03-vertical-list` |
| 04 | `04-prototype-vertical` | 第一版原型改成直式，黑白兩版 | `v04-prototype-vertical` |
| 05 | `05-ai-reading` | 模擬 AI 讀信：逐 token 出現、注意力曲線；直式全文 15.5 分鐘 | `v05-ai-reading` |
| 06 | `06-landscape` | 橫式 1920×1080，閃爍數字 → 變暗 → 曲線；5 分鐘試作 | `v06-landscape` |
| 07 | `07-fine-lines` | 細線一條一條伸出來（30 秒、54 秒） | `v07-fine-lines` |
| 08 | `08-nine-stages` | 九個階段，「不以人的方式思考」，1 分鐘 v1、v2 | `v08-nine-stages` |
| 09 | `09-nine-stages-20min` | 九個階段 20 分鐘，跟著估計的朗讀速度 | `v09-nine-stages-20min` |
| 10 | `10-live-voice` | 聲音即時互動：開口畫面就動、停下就停 | `v10-live-voice` |
| 11 | `11-3d-v1` | 3D 第一版，1 分鐘 | `v11-3d-v1` |
| 12 | `12-3d-v2-rule` | 3D 第二版：同一條規則套用九次，等速環繞 | `v12-3d-v2-rule` |
| 13 | `13-3d-20min` | 3D 20 分鐘：每個階段的掃描佔滿整個階段 | `v13-3d-20min` |
| 14 | `14-image-patches` | 圖片版：一張照片被切成 576 塊（CLIP ViT-L/14-336） | `v14-image-patches` |

## 重新產生

需要 Node 18 以上、Python 3、Playwright（Chromium）、ffmpeg；PDF 另外需要 weasyprint。

```bash
npm ci
pip install playwright weasyprint && playwright install chromium

node tools/tokenize.js path/to/LETTER.md data/zh.json   # 重新切 token
python3 tools/make_timing.py                            # 重新估計朗讀時間表 → data/timing.json

python3 12-3d-v2-rule/render3d_v2.py stills 5,20,40     # 先看幾張靜態畫面
python3 12-3d-v2-rule/render3d_v2.py video              # 輸出影片到 out/
```

每個資料夾的 `README.md` 寫了該版本的指令。輸出一律寫到 `out/`，這個資料夾不會進 git。

## 說明牌用語（建議）

- 「token 與 ID 為 GPT-4o 分詞器的實際切分；連線與向量為藝術家依信件內容所繪之示意。」
- 圖片版：「依 CLIP ViT-L/14-336 規格切割；向量與注意力為示意。」

Claude 的分詞器沒有公開，所以這裡一律標示為 GPT-4o 分詞器。

## 授權

信的文字與影像屬於作者吳方娸 ljaljuy tjavelengan，保留一切權利。若要使用，請先聯繫作者。
