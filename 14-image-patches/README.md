# 14 — 圖片切割

依 CLIP ViT-L/14-336 規格，把一張照片切成 576 塊：位元組解碼 → 補邊、縮成 336×336 → 切成 24×24 → 攤平（588 個數字）→ 1024 維向量 → 雙向注意力 → 文字 token ID。`img/src.jpg` 是作者提供的照片。

## 指令（在 repo 根目錄執行）

```bash
python3 14-image-patches/prep_img.py
python3 14-image-patches/render_img.py stills 1,8,13.5,22
python3 14-image-patches/render_img.py video
```

輸出寫到 `out/`。

## 影片

由作者另外保存，檔名：

- README_image_patches_3d_30s.mp4

## 截圖

見 `stills/`。

過程與決定見 [`../DECISIONS.md`](../DECISIONS.md)。
