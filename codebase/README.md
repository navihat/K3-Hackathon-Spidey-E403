# codebase — Trợ lý tìm lại link tài liệu Discord

Toàn bộ code của prototype nằm trong thư mục này. Lát cắt và quality bar: xem [`../spec.md`](../spec.md).

## 1. Cấu trúc

```
codebase/
├── .venv/                  ← môi trường ảo (gitignore)
├── .env                    ← secret, tự tạo từ .env.example (gitignore)
├── .env.example            ← mẫu, KHÔNG chứa secret thật
├── requirements.txt
├── index.db                ← SQLite FTS5, sinh ra khi chạy (gitignore)
│
├── timlai/                 ← ★ PACKAGE — logic sản phẩm
│   ├── config.py           ← đọc .env, hằng số, ép UTF-8 cho console Windows
│   ├── index.py            ← ② retrieval: FTS5 + BM25
│   ├── tra_cuu.py          ← ③ quyết định AI + chống bịa   ← KHÔNG import discord
│   ├── render.py           ← trình bày 4 đường đi trải nghiệm
│   └── bot.py              ← ① Discord client + /timlai
│
├── scripts/                ← ★ ENTRY POINT — chạy tay, không phải logic
│   ├── kiem_tra_doc.py     ← smoke test: bot đọc được Discord chưa?
│   ├── seed_gia.py         ← nạp 20 tin nhắn giả (chạy được khi chưa có server)
│   ├── backfill.py         ← dựng index từ Discord thật
│   ├── thu_hoi.py          ← hỏi 1 câu từ terminal (vòng lặp dev)
│   └── chay_eval.py        ← chạy 22 case golden set → bảng % cho R4
│
└── tests/                  ← ★ TEST TỰ ĐỘNG — pytest, không cần API key
    ├── conftest.py         ← fixture: index in-memory + 3 tin mẫu
    ├── test_index.py       ← 7 test lớp ②
    └── test_tra_cuu.py     ← 11 test lớp ③ (4 lớp chỗ khó + 4 đường đi)
```

**Quy tắc chia thư mục** — chỉ một quy tắc, nhưng nó quyết định 15 điểm R4:

> `timlai/tra_cuu.py` **không được import discord**. Quyết định AI phải là một hàm Python thuần gọi được ngoài Discord — nếu không thì `chay_eval.py` không chạy nổi 22 case và R4 mất trắng.

`scripts/` chỉ nối dây, không chứa logic. Logic nào cần test thì phải nằm trong `timlai/`.

## 2. Cài đặt

**Bước 1 — venv.** Bắt buộc: `discord.py` ghim version, không nên cài vào Python hệ thống.

```powershell
cd codebase
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # thấy (.venv) ở đầu dòng lệnh là xong
pip install -r requirements.txt
```

```bash
# Git Bash / macOS / Linux
cd codebase
python -m venv .venv
source .venv/Scripts/activate       # Linux/mac: source .venv/bin/activate
pip install -r requirements.txt
```

> PowerShell chặn script? Chạy một lần: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
> Không muốn activate? Gọi trực tiếp: `.\.venv\Scripts\python.exe scripts/thu_hoi.py "..."`

**Bước 2 — secret.**

```powershell
Copy-Item .env.example .env         # bash: cp .env.example .env
```

Điền `GEMINI_API_KEY` (lấy free tại [aistudio.google.com/apikey](https://aistudio.google.com/apikey)),
và `DISCORD_TOKEN` + `GUILD_ID` nếu đã có server test.
`.env` đã bị `.gitignore` chặn — **đừng bao giờ commit nó**.

## 3. Ba đường chạy

### A. Chưa có server Discord — chạy được ngay

Đề bài ràng buộc 3 cho phép **data giả tự sinh**. Đường này cho bạn demo được toàn bộ pipeline trước khi lo chuyện Discord.

```powershell
python scripts/seed_gia.py                          # nạp 20 tin nhắn giả
python scripts/thu_hoi.py "link slide buổi 5" --chi-loc   # xem FTS5, KHÔNG tốn token
python scripts/thu_hoi.py "link slide buổi 5"             # gọi AI thật
python scripts/chay_eval.py                               # 22 case → eval/ket-qua/
```

### B. Có server Discord test

**Dựng 5 kênh.** Tên kênh phải khớp **đúng từng ký tự** với `KENH_INDEX` trong `.env` —
`backfill.py` lọc bằng `ch.name not in config.KENH_INDEX`, lệch một dấu gạch là kênh bị bỏ qua:

| Kênh cần tạo | Ứng với spec.md §4 |
|---|---|
| `thong-bao` | Kênh #Build/Thông báo #Build |
| `tai-nguyen` | Kênh Build/Tài nguyên |
| `thong-bao-chung` | Kênh Lớp học Khoá 3/Thông báo chung |
| `ly-thuyet-k3` | Kênh lý thuyết — Lớp học Khoá 3 |
| `lab-k3` | Kênh thực hành lab — Lớp học Khoá 3 |

**Nạp nội dung.** `python scripts/seed_gia.py --in-discord` in 20 tin nhắn theo từng kênh
để dán tay. Ba điều kiện, sai một cái là index rỗng hoặc golden set lệch:

- Dán bằng **tài khoản người**, không webhook/bot — `backfill.py` bỏ `m.author.bot`.
- Dán **đúng thứ tự** trong mỗi kênh — TH-18 đòi chọn bản slide buổi 5 mới nhất.
- **Không** đăng slide buổi 10 và **không** đăng QR checkin — hai cái đó là bẫy cố ý
  của TH-11/TH-12; có chúng thì mất case lớp ①.

Đừng copy tin nhắn thật từ Discord của khoá vào đây — ràng buộc 3 của đề bài chỉ cho
dùng data trong `data/` hoặc data giả tự sinh.

**Cấu hình + chạy.**

```powershell
# GUILD_ID: Discord → Settings → Advanced → bật Developer Mode
#           → chuột phải tên server → Copy Server ID → dán vào .env
python scripts/kiem_tra_doc.py      # 1. xác nhận đọc được tin nhắn
python scripts/backfill.py          # 2. dựng index từ lịch sử thật
python scripts/thu_hoi.py "..."     # 3. thử
```

Bot cần **MESSAGE CONTENT INTENT** (Developer Portal → tab Bot) và quyền
*Read Message History* trên cả 5 kênh; URL mời phải có cả scope `bot` **và**
`applications.commands`, thiếu cái sau thì `/timlai` không hiện.

> **Tin dán tay đều mang thời điểm hôm nay**, nên `canh_bao_cu()` không kích hoạt và
> case ④ (TH-17) không tái hiện được trên server thật. Vì vậy: **lượt eval R4 chạy trên
> `seed_gia.py`** (có lùi ngày, đủ 4 lớp chỗ khó), **Discord thật dùng để demo end-to-end**.
> spec.md §4 khai mức **Working** — hợp lệ, vì cùng một `tra_cuu()` chạy cho cả hai đường,
> chỉ khác nguồn nạp index; và cả hai nguồn đều là data giả theo ràng buộc 3 của đề bài.

### C. Bot chạy thật

```powershell
python -m timlai.bot
```

**Ba cách hỏi**, cùng chạy qua một hàm `bot.hoi()` nên hành vi giống hệt nhau:

| Cách | Gõ gì trong Discord | Dùng khi |
|---|---|---|
| Slash command | `/timlai link slide buổi 5` | có gợi ý tham số, không sợ gõ nhầm |
| @mention | `@Spidey link slide buổi 5` | gõ tự nhiên, không cần nhớ tên lệnh |
| Reply | reply vào tin của bot rồi gõ `ý mình là bài 2 của build` | đường **correction** ở spec §6 — hỏi lại không cần bắt đầu lại |

**Câu trả lời là công khai** — cả kênh cùng thấy, không còn `ephemeral`. Một người hỏi thì
cả lớp đỡ phải hỏi lại. Đánh đổi: bot sai thì cũng sai trước mặt mọi người, nên footer
"đã bỏ N kết luận không neo được" cũng hiện công khai — đó là chủ ý, không phải rò rỉ debug.

**Tự động trả lời mọi tin trong một kênh** (mặc định TẮT): điền tên kênh vào `KENH_TU_DONG`
trong `.env`. Đừng điền 5 kênh ở `KENH_INDEX` — đó là kênh thông báo/tài nguyên, bật lên thì
bot trả lời cả thông báo của LabCoach và đốt sạch hạn mức **20 lời gọi/ngày/model** của free
tier. Nên tạo riêng một kênh `#hoi-bot`. Tin ngắn dưới 5 ký tự bị bỏ qua để khỏi tốn lời gọi
cho "ok", "vâng".

Vòng lặp bot-trả-lời-bot bị chặn ở đúng một dòng: `on_message` thoát ngay nếu `msg.author.bot`.
Nhờ vậy câu trả lời của chính bot cũng không lọt vào index.

> **Tin mới tự vào index** qua `on_message` — không cần chạy lại `backfill.py`. Nhưng
> `backfill.py` **không xoá** tin cũ trong `index.db`: `them()` chỉ `DELETE` đúng dòng trùng
> `id`. Chạy backfill lên index đang có tin giả thì thành **lẫn lộn** — 20 tin giả của
> `seed_gia.py` (link chết `channels/111/222/…`) vẫn nằm đó và có thể bị trả về giữa lúc demo.
>
> ```powershell
> python scripts/backfill.py --sach   # xoá index.db rồi dựng lại, chỉ còn tin thật
> ```
>
> Kiểm nhanh index đang chứa gì:
>
> ```powershell
> python -c "from timlai import index; db=index.mo_db(); print(index.dem(db), 'tin;', db.execute(\"SELECT count(*) FROM tin_nhan WHERE id LIKE '10000000000000%'\").fetchone()[0], 'tin gia')"
> ```

## 4. Test — ba tầng, dùng đúng tầng cho đúng việc

| Tầng | Lệnh | Cần API key? | Thời gian | Trả lời câu hỏi gì |
|---|---|---|---|---|
| **1. pytest** | `pytest tests -q` | ❌ | ~0.2s | Logic chống bịa và 4 lớp chỗ khó còn đúng không? |
| **2. thu_hoi** | `python scripts/thu_hoi.py "..."` | ✅ (bỏ nếu `--chi-loc`) | ~5s | Một câu cụ thể ra kết quả thế nào? |
| **3. chay_eval** | `python scripts/chay_eval.py` | ✅ | ~2,5 phút | % qua quality bar — artifact nộp cho R4 |

Model: `gemini-3.6-flash` (free tier) — lý do chọn và số đo hai lần đo: comment ở `timlai/config.py`.
Hạn free tier tính theo **lời gọi/phút**, nên
`_goi_gemini` tự giãn 6,5s giữa hai lời gọi liền nhau (`config.GIAN_CACH_GOI`) — đó là lý do
trọn bộ 22 case mất ~2,5 phút chứ không phải ~30s. Một câu hỏi lẻ trong Discord **không** bị giãn.

Lời gọi được thử lại tối đa `config.SO_LAN_THU` lần với backoff 13s → 26s → 52s → 104s, chỉ cho
ba mã lỗi tạm thời trong `tra_cuu._LOI_TAM_THOI`: **429** hết hạn mức, **500/503** Google quá tải.
Mã khác (400 sai request, 403 sai key) ném lên ngay vì chờ không tự khỏi.

**Chạy tầng 1 sau mỗi lần sửa code.** Nó không tốn token và bắt được hầu hết lỗi hồi quy:

```powershell
pytest tests -q                     # 18 passed
pytest tests -q -k lop1             # chỉ nhóm chống bịa
pytest tests -v                     # xem tên từng test
```

### 4.1 · Chín case phải test bằng tay trước khi demo

Đây là các case mà pytest **không** bắt được vì chúng phụ thuộc hành vi LLM thật. Chạy tầng 2 cho từng dòng, ghi kết quả vào `../validation/`.

| # | Lệnh | Phải thấy gì | Sai thì lỗi ở đâu |
|---|---|---|---|
| 1 | `thu_hoi.py "link slide buổi 5"` | 1 link, kèm `discord.com/channels/...` | — happy path |
| 2 | `thu_hoi.py "slie buoi 5"` | vẫn ra slide buổi 5 | FTS5 tokenizer — lớp ② |
| 3 | `thu_hoi.py "link slide buổi 10"` | `tim_thay=False`, **không có link nào** | ① nếu nó bịa link → prompt hoặc `neo()` |
| 4 | `thu_hoi.py "link checkin"` | `tim_thay=False` | ① |
| 5 | `thu_hoi.py "link slide"` | `do_tin_cay=thap` + câu hỏi lại | ② nếu tự chọn 1 → luật 3 trong SYSTEM |
| 6 | `thu_hoi.py "giải thích hàm softmax"` | `ngoai_pham_vi=True` | ③ |
| 7 | `thu_hoi.py "link slide buổi 5 bản mới nhất"` | link **v2** (24/07), không phải v1 | ④ thứ tự `truy_xuat` |
| 8 | `thu_hoi.py "link lab 2"` | có dòng `⚠️ Tin này từ N ngày trước` | ④ `canh_bao_cu` |
| 9 | `thu_hoi.py "link"` | hỏi lại kèm ví dụ | ② |

Case **3, 4** là quan trọng nhất: quality bar trong `spec.md §7` là **0 case bịa nguồn**. Một link bịa ở đây là fail cả bar, không phải trừ điểm.

### 4.2 · Kiểm runner trước khi chạy thật

`chay_eval.py` gọi AI 22 lần. Trước khi tốn token, kiểm runner bằng LLM giả:

```powershell
python scripts/chay_eval.py --gia    # LLM giả, 0 token
```

LLM giả cố tình trả 1 message_id bịa mỗi lần được gọi. Kết quả đúng phải là **`bịa nguồn: 19`** (không phải 22 — 3 case mà FTS5 trả 0 ứng viên thì `tra_cuu()` chặn trước, không gọi AI, nên không có gì để bịa). Nếu con số này về **0**, cơ chế `neo()` đã hỏng và mọi số liệu sau đó vô nghĩa.

Con số pass ở lượt `--gia` (~73%) **không có ý nghĩa gì** — nó chỉ chứng minh runner chạy và biết phát hiện sai lệch.

```powershell
python scripts/chay_eval.py --kho    # chỉ 8 case ①②③④, ~40% token
python scripts/chay_eval.py          # trọn bộ 22 case → nộp cho R4
```

Kết quả ghi ra `../eval/ket-qua/luot-N.md`, **kèm cả case chưa đạt**. Rubric ghi rõ: kết quả thấp vẫn được tính đủ điểm nếu ghi nhận trung thực; số liệu bị che thì không được tính.

## 5. Lỗi thường gặp

| Hiện tượng | Nguyên nhân | Sửa |
|---|---|---|
| `ModuleNotFoundError: No module named 'audioop'` khi `import discord` | discord.py ≤2.4 import `audioop`, mà module này bị xoá khỏi stdlib từ Python 3.13 | `pip install --upgrade "discord.py==2.7.1"` (nó tự kéo `audioop-lts`) |
| `kiem_tra_doc.py` in `(không có text)` mọi dòng | Chưa bật **MESSAGE CONTENT INTENT** | Developer Portal → tab Bot → bật → **restart bot** |
| `UnicodeEncodeError: 'charmap'` | Console Windows cp1252 | Đã xử lý trong `config.py`; nếu vẫn gặp thì script đó chưa `import config` |
| `/timlai` không hiện trong Discord | Thiếu scope `applications.commands` | Sinh lại URL OAuth2 với **cả** `bot` và `applications.commands` |
| `Thiếu DISCORD_TOKEN` | Chưa có `.env` | `Copy-Item .env.example .env` rồi điền |
| `index.db trống` | Chưa nạp dữ liệu | `python scripts/seed_gia.py` hoặc `backfill.py` |
| `sqlite3.OperationalError: fts5: syntax error` | Có input lọt qua `_cau_truy_van` | Thêm case đó vào `test_ky_tu_dac_biet_khong_lam_sap` rồi sửa regex `_TU` |
| Bot trả link nhưng sai bài | Lỗi lớp ② không phải ③ | Chạy `--chi-loc` xem FTS5 có ra tin đúng không trước khi sửa prompt |

## 6. Bản đồ code → rubric

| Rubric | Điểm | File |
|---|---|---|
| R3 · 4 lớp chỗ khó | 11 | `tra_cuu.py` SYSTEM + `neo()` + `canh_bao_cu()`; 4 đường đi ở `render.py` |
| R4 · Kiểm thử | **15** | `tests/`, `scripts/chay_eval.py`, `../eval/golden-set.yaml`, `../eval/ket-qua/` |
| R5 · Prototype | 8 | `timlai/bot.py` end-to-end; lời gọi AI thật + log `[trace]` ở `tra_cuu._goi_gemini` |
| R7 · Repo | 3 | cấu trúc mục 1 |
