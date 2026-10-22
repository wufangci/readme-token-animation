# readme-token-animation

這個 repo 是〈README：一封寫給人工智慧的家書〉系列裡「AI 如何讀這封信」的 token 動畫，目前**還在製作中**。

作品本體（信與 skill）在 [wufangci/README](https://github.com/wufangci/README)。

## 從這裡開始

| 檔案 | 用途 |
|---|---|
| [`00_PRODUCTION_BOARD.md`](00_PRODUCTION_BOARD.md) | 製作總表：版本、狀態、影片、下一步 |
| [`SESSION_HANDOFF.md`](SESSION_HANDOFF.md) | 交接：上次做到哪、下次從哪開始 |
| [`AGENTS.md`](AGENTS.md) | 給 AI 的常用記憶：規則、美學偏好、工作習慣 |

## 資料夾

| 資料夾 | 內容 |
|---|---|
| `01_source/` | 原著與設定：token 資料、連線組、規格與說明牌用語 |
| `02_timeline/` | 時間軸：朗讀時間表（目前是估計值） |
| `03_assets/` | 素材：照片等原始檔 |
| `04_active/` | 主線：還在發展的版本（09、10、12、13、14） |
| `05_tools/` | 工具：切 token |
| `06_process/` | 創作歷程：決策紀錄、每次工作摘要 |
| `90_archive/` | 封存：被取代的版本（01–08、11） |
| `out/` | 算圖輸出（不進 git） |

影片檔太大，不進 git，由作者自行保存。檔名對照在製作總表。

## 重新產生

需要 Node 18 以上、Python 3、Playwright（Chromium）、ffmpeg；PDF 另外需要 weasyprint。

```bash
npm ci
pip install playwright weasyprint && playwright install chromium

python3 04_active/12-3d-v2-rule/render3d_v2.py stills 5,20,40   # 先看靜態畫面
python3 04_active/12-3d-v2-rule/render3d_v2.py video            # 輸出到 out/
```

每個版本資料夾的 `README.md` 都寫了指令。

## 數字

- **信**：5,945 字、17,229 bytes。
- **分詞**：用 GPT-4o 分詞器切成 5,366 個 token，其中 814 個是位元組碎片。
- 規格細節見 [`01_source/SPECS.md`](01_source/SPECS.md)。

## 授權

信的文字與影像屬於作者吳方娸 ljaljuy tjavelengan，保留一切權利。若要使用，請先聯繫作者。
