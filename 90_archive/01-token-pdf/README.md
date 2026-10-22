# 01 — token PDF

把整封信切成 5,366 個 token，每個附上 GPT-4o 分詞器的 ID；位元組碎片顯示為十六進位。共 22 頁。

## 指令（在 repo 根目錄執行）

```bash
python3 90_archive/01-token-pdf/build_pdf.py      # → out/README_tokens.pdf（需要 weasyprint）
```

輸出寫到 `out/`。

## 成品

`README_tokens.pdf`（就在這個資料夾）

## 截圖

見 `stills/`。

過程與決定見 [`06_process/DECISIONS.md`](../../06_process/DECISIONS.md)。
