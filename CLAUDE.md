# 芯光點點 Light Within Studio

新北板橋的手作課程工作室網站。純靜態 HTML/CSS/JS，沒有框架、沒有建置步驟，
由 GitHub Pages 直接部署到自訂網域 `lightwithinstudio.tw`。

---

## 分支：兩個版本，不是主線與功能分支

| 分支 | 內容 | 狀態 |
| --- | --- | --- |
| `main` | **純奧剛版**。只有奧剛能量藝術一個領域，兩門課。 | GitHub Pages 目前部署這個 |
| `future-expansion` | **四領域擴充版**。奧剛／曼陀羅／塔羅／八字。 | 設計預覽，尚未定案 |
| tag `orgonite` | 純奧剛版的內容快照 | 隨時可回到當時狀態 |

兩者是**同一個網站的兩個版本**，不是「穩定版 vs 開發中」。改動前先確認自己在哪個分支，
兩邊的檔案結構不一樣（見下方「圖片路徑」）。

Pages 的分支可以隨時切換（Settings → Pages → Branch → Save，約 1 分鐘生效）。
切到 `future-expansion` 期間，正式網址顯示的是草稿，所有頁面都有 `noindex` 保護，
但**不要放超過一天**。

擴充版的完整規劃見 `_drafts/未來擴展版_網站架構規劃.md`（只存在於 `future-expansion` 分支）。

---

## 絕對不要做的事

**不要改 `main` 的圖片路徑。** `main` 有 3 個檔案的網址被寫死在 `og:image` 與
JSON-LD 裡，已經被 Google 與 FB／LINE 的預覽快取收錄：

```
images/course/c_0004.jpg    images/course/c_0012.jpg    images/title/t_0001.JPG
```

GitHub Pages 不支援 301 轉址，圖片一搬走舊網址就 404，分享出去的連結會破圖。
路徑要改，只能在擴充版正式上線時一併處理（檢查表在規劃文件裡）。

**不要重新編圖片號碼。** 現有編號有缺號（`c_0011`、`c_0016`、`c_0025`），
那是正常的。為了補號而重編，HTML 會整片指錯。

**不要把預覽用的標記帶上線。** `<body class="draft">` 會讓預留圖顯示「照片準備中」；
`<meta name="robots" content="noindex">` 會讓頁面不被搜尋引擎收錄。
兩者都只該存在於未完成的頁面。

---

## 圖片與檔案

檔名一律是「前綴 + 四位流水號」，**換照片直接覆蓋同檔名，不用改 HTML**：

```
t_  品牌／主視覺      a_  教室環境      c_  課程頁照片      s_  作品展示
```

資料夾結構兩個分支不同：

```
main:               images/{title,about_us,course,showcase}/
future-expansion:   images/common/{title,about_us}/
                    images/{orgonite,mandala,tarot,bazi}/{course,showcase}/
                    pdf/{orgonite,mandala,tarot,bazi}/
```

擴充版的完整規則（含 HEIC 原始檔擺法）見 `images/資料夾與命名規則.txt`（只存在於 `future-expansion` 分支）。

`.HEIC` 是 iPhone 原始檔，瀏覽器不支援，**不放在這個 repo 裡**，
改放隔壁的 `C:\Fatek_9702\web_side_原始檔\<領域>\`，檔名與 jpg 相同。
放在 repo 內會有問題：HEIC 被 gitignore、未追蹤，切分支時不會跟著移動，
會在舊路徑留下空的幽靈目錄。`.gitignore` 仍保留 `*.HEIC` 當保險。

---

## CSS 慣例

`css/style.css` 是單一檔案，沒有前處理器。改動請沿用既有的區塊註解結構。

**導覽列的下拉選單是 mobile-first：手機的縮排子清單是預設，浮動下拉包在
`@media (min-width: 769px)` 裡。不要反過來寫。**

反過來寫（桌機當預設、手機再逐條撤銷）踩過一次坑：media query 不增加特異性，
`.nav-item:focus-within .nav-sub` 是 `(0,3,0)`，手機端用 `.nav-sub` `(0,1,0)` 蓋不掉，
手指一點子項目取得 focus，桌機用來置中的 `translateX(-50%)` 就活了過來，
把滿版子選單往左推出畫面一半。

hover 展開包在 `(hover: hover) and (pointer: fine)` 裡——觸控裝置的 `:hover` 會黏住。
`:focus-within` 不受此限制，鍵盤 Tab 要能展開。

擴充版的領域配色掛在 `<body class="theme-orgonite|mandala|tarot|bazi">`，
新元件用 `var(--accent)` / `var(--accent-deep)`，不要寫死色碼。

---

## 本機預覽

```bash
python -m http.server 8123
```

瀏覽器開 `http://localhost:8123`。不影響線上網站。
改完 CSS/JS 記得確認 HTML 裡的 `?v=` 版本號有沒有需要更新（用來破快取）。

---

## 文字內容

面向客戶的文案（課程說明、價格、時數）**不要自行編寫或推測**。
擴充版裡還沒定案的地方一律標示為〔文案待定〕、〔課程名稱待定〕，
照片用工作室 logo 當預留圖，寧可空著也不要放假資訊。
