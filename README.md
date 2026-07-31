# Trợ lý tìm lại link tài liệu Discord — Nhóm Spidey · Batch 03

> Một học viên gõ câu hỏi tự nhiên trong Discord ("link slide buổi 5") → AI tìm trong tin nhắn
> của 5 kênh chỉ định → trả về link tài liệu kèm tên người gửi + link tới tin nhắn gốc;
> không có căn cứ thì nói **"Mình không tìm thấy"**, tuyệt đối không bịa link.

Hướng **B — Trợ lý Học viên (Discord)** · **Tính năng mới** · Mức prototype: **Working**

## Thành viên & phân công

| Mã HV | Họ tên | Phụ trách | Artifact chính |
|---|---|---|---|
| 2A202601801 | Trương Văn Thái | Code prototype + Demo | [`codebase/`](codebase/) · [`eval/ket-qua/`](eval/ket-qua/) |
| _(điền mã HV)_ | Trương Thảo Nguyên | Spec + evidence | [`spec.md`](spec.md) §1-§2 · [`data/khao-sat-log.md`](data/khao-sat-log.md) |
| _(điền mã HV)_ | Đinh Quốc Trung | Prompt + golden set | `SYSTEM` trong [`codebase/timlai/tra_cuu.py`](codebase/timlai/tra_cuu.py) · [`eval/golden-set.md`](eval/golden-set.md) |

## Vấn đề & bằng chứng

Khảo sát **36 học viên ngoài nhóm** (log đầy đủ: [`data/khao-sat-log.csv`](data/khao-sat-log.csv)):

| Con số | Ý nghĩa |
|---|---|
| **31/36 (86%)** | từng không tìm được thông tin trong Discord 7 ngày qua |
| **26/31 (84%)** | cần tìm slide/tài liệu buổi học — ứng viên được chọn |
| **26/31 (84%)** | chỉ nhớ mơ hồ → phải check 2-3 kênh |
| **15/31 (48%)** | mất 5-15 phút mỗi lần tìm |
| **24/31 (77%)** | khó chịu; **23%** bỏ cuộc hoặc lỡ deadline |

Bảng impact 4 ứng viên + lý do loại B/C/D: [`spec.md`](spec.md) §2.

## Chạy thử trong 4 lệnh

```powershell
cd codebase
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
Copy-Item .env.example .env          # rồi điền GEMINI_API_KEY
python scripts/seed_gia.py           # nạp 20 tin nhắn giả — không cần server Discord
python scripts/thu_hoi.py "link slide buổi 5"
```

Dựng server Discord thật, 9 case test tay, bảng lỗi thường gặp: [`codebase/README.md`](codebase/README.md).

## Bản đồ repo → rubric

| Đường dẫn | Nội dung | Rubric |
|---|---|---|
| [`spec.md`](spec.md) | AI Spec — §1-§2 evidence · §4 lát cắt · §5-§6 chỗ khó · §7 quality bar | R1, R2, R3, R4 |
| [`data/khao-sat-log.csv`](data/khao-sat-log.csv) · [`.md`](data/khao-sat-log.md) | Log khảo sát 36 người, đủ câu hỏi + từng câu trả lời | R1 |
| [`codebase/`](codebase/) | Prototype: 3 lớp Discord → FTS5 → Gemini, 18 pytest | R5 |
| [`eval/golden-set.md`](eval/golden-set.md) · [`.yaml`](eval/golden-set.yaml) | 22 case: 10 thường · 8 khó (2/lớp ①②③④) · 4 hiếm | R4 |
| [`eval/ket-qua/`](eval/ket-qua/) | Bảng kết quả từng lượt, kể cả case chưa đạt | R4 |
| [`validation/`](validation/) | Feedback log từ vòng user test | R6 |
| [`reflection/`](reflection/) | Mỗi người 1 file | riêng |
| [`demo-slides.pdf`](demo-slides.pdf) | Slide 6 trang · nguồn sinh ra nó: [`demo-slides.html`](demo-slides.html) | demo |
| [`CLAUDE.md`](CLAUDE.md) | Bối cảnh + luật chơi khi phát triển ý tưởng tiếp | — |

Sinh lại PDF sau khi sửa slide:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless --disable-gpu `
  --print-to-pdf="demo-slides.pdf" --no-pdf-header-footer "demo-slides.html"
```

## Quality bar & kết quả

**Bar chốt 23:59 ngày 1** ([`spec.md`](spec.md) §7): ≥85% pass golden set **và 0 case bịa nguồn** (lớp ①).

| Lượt | Model | Pass | Bịa nguồn |
|---|---|---|---|
| [luot-1](eval/ket-qua/luot-1.md) | ⚠️ LLM giả — kiểm runner, không phải kết quả thật | 72.7% | 19 |
| [luot-2](eval/ket-qua/luot-2.md) | `gemini-3.1-flash-lite` · 22/22 case | **81.8%** — chưa đạt | **0** — đạt |

Bốn case trượt quy về hai nguyên nhân, phân tích đầy đủ trong [luot-2.md](eval/ket-qua/luot-2.md).
Mọi lượt đều ghi đủ case, kể cả case chưa đạt.

---

# Thông tin sự kiện — Mini Hackathon AI Batch 03

**SPEC → Prototype → Demo.** Đây không phải cuộc thi code — đây là cuộc thi **tư duy sản phẩm AI**.

- Thời lượng: **1,5 ngày** (một ngày build + một buổi demo)
- Nhóm: **4-5 người** · zone tối đa 5 nhóm · thi theo lớp

## Bắt đầu từ đâu?

1. Đọc **`01-de-bai.md`** để chọn hướng và hiểu tiêu chí.
2. Mở **`02-guide.md`** — hướng dẫn từng giai đoạn, đứng ở đâu đọc mục đó.
3. Viết spec theo **`03-template-ai-spec.md`** — deliverable trung tâm của cả sự kiện.
4. Đọc **`04-rubric.md`** ngay từ đầu — biết trước bài được chấm theo tiêu chí nào.

| File / thư mục | Nội dung |
|---|---|
| `01-de-bai.md` | Đề bài 3 hướng · 5 tiêu chí nghiệm thu · ràng buộc chung |
| `02-guide.md` | Hướng dẫn 5 giai đoạn: khám phá → spec → build → đo & validate → demo |
| `03-template-ai-spec.md` | Template AI Spec (nộp 23:59 ngày 1) |
| `04-rubric.md` | Rubric 100 điểm (25 nộp checkpoint + 75 chấm bài) + checklist xác minh 6 mốc |
| `data/` | Dữ liệu thật đã ẩn danh: chatlog VLearn tutor + 6 transcript bài giảng + 2 bộ slide bản hackathon — dùng để tìm bằng chứng và xây golden set |
| `tham-khao/` | JTBD Playbook (PDF) + worksheet JTBD đầy đủ — đọc khi muốn đào sâu |

## Lịch — 6 mốc

| Mốc | Khoá 3 | Khoá 4 |
|---|---|---|
| Khai mạc + phát đề | 09:00 ngày 1 | 14:00 ngày 1 |
| CP1 · Chốt Canvas | 10:00 ngày 1 | 15:00 ngày 1 |
| CP2 · Show được thứ bấm được | 12:00 ngày 1 | 17:00 ngày 1 |
| CP3 · AI chạy thật + đo lượt đầu | 16:00 ngày 1 | 10:30 ngày 2 |
| CP4 · Chốt tiến độ — spec nộp hạn cứng **23:59 ngày 1** | 17:30 ngày 1 | 12:00 ngày 2 |
| CP5 · Xác minh + validation + dry run | 09:00 ngày 2 | 14:00 ngày 2 |
| CP6 · Demo | 10:00 ngày 2 | 15:00 ngày 2 |

Mỗi mốc cần show gì và được xác minh thế nào: xem bảng trong `04-rubric.md`.

## Nộp bài

Một repo nhóm, cấu trúc như sau. Spec chốt lúc 23:59 ngày 1; bản hoàn chỉnh trước CP6.

```
repo/
├── README.md          ← thành viên (mã HV + tên) + phân công có tên từng phần
├── spec.md            ← AI Spec theo 03-template-ai-spec.md
├── demo-slides.pdf    ← slide 6 trang theo 02-guide.md §5.1
├── codebase/          ← prototype (ghi rõ phần nào mock)
├── eval/              ← golden set + bảng kết quả các lượt chạy
├── validation/        ← feedback log từ vòng user test
└── reflection/        ← mỗi người 1 file
```

## Chấm điểm

Tổng **100 điểm = 25 điểm nộp checkpoint + 75 điểm chấm bài nộp**. Chi tiết từng ý điểm: `04-rubric.md`.

**25 điểm nộp — mỗi checkpoint 5 điểm (CP1-CP5):** nộp đúng hạn → 5 điểm · nộp muộn → 0 điểm cho mốc đó. Mỗi thành viên nộp riêng, cả nhóm dùng chung một link repo.

**75 điểm chấm — trên artifact trong repo, mỗi con điểm trỏ về một file:**

| Khối | Điểm | Chấm trên file nào |
|---|---|---|
| R1 · Bằng chứng & impact | 15 | `spec.md` §1-§2 + log khảo sát/mining |
| R2 · Lát cắt & thiết kế | 15 | `spec.md` §4 |
| R3 · Chỗ khó & kịch bản rủi ro | 11 | `spec.md` §5-§6 |
| R4 · Kiểm thử | 15 | `spec.md` §7 + `eval/` |
| R5 · Prototype chạy được | 8 | `codebase/` + demo |
| R6 · Validation với user | 8 | `validation/` |
| R7 · Quy trình & repo | 3 | cấu trúc repo |

Ba điều nên biết trước khi làm:

- Điểm dựa trên **chuỗi quyết định và bằng chứng**, không dựa trên mức độ hoành tráng của sản phẩm.
- Kết quả đo **ghi nhận trung thực** — kể cả khi không đạt mục tiêu nhóm tự đặt — vẫn được tính đủ điểm. Số liệu bị chỉnh sửa hoặc che giấu sẽ không được tính.
- Reflection cá nhân chấm riêng theo rubric của khoá. Điểm vòng demo, chấm chéo trong zone và thưởng thêm (nếu có) theo thể lệ công bố lúc khai mạc.

## Luật chung

1. Prototype có 3 mức **Sketch / Mock / Working** — mức nào cũng bắt buộc **≥1 lời gọi AI chạy thật**.
2. **Vibe-coding rule:** dùng AI để build thoải mái, nhưng không giải thích được phần có tên mình thì phần đó 0 điểm (kiểm tra tại CP5).
3. **Quality bar** chốt tại spec.md 23:59 ngày 1 và giữ nguyên sau đó.
4. Chỉ dùng dữ liệu trong `data/` hoặc dữ liệu giả tự sinh — không dùng dữ liệu thật của người thật. Không commit API key.
5. Tuân thủ **quy định bảo mật dữ liệu** bên dưới — đây là điều kiện để được cấp data.

## Bảo mật dữ liệu được cung cấp

Dữ liệu trong `data/` là dữ liệu thật của khoá học (đã ẩn danh), cấp riêng cho hackathon này. Khi nhận data, nhóm cam kết:

1. **Chỉ dùng trong phạm vi hackathon** — cho việc tìm bằng chứng, xây golden set và build prototype. Không dùng cho mục đích khác.
2. **Không chia sẻ ra ngoài khoá học** — không đăng lên mạng xã hội, không gửi cho người ngoài, không đưa vào bất kỳ dataset hay repo công khai nào.
3. **Không commit data pack vào repo nộp bài** — repo nhóm chỉ chứa trích dẫn ngắn để minh hoạ (vài dòng); golden set trích từ data ghi rõ mã đoạn/mã hội thoại thay vì dán nguyên văn dài.
4. **Cẩn trọng khi đưa data vào công cụ ngoài** — chỉ đưa phần tối thiểu cần cho việc đang làm; lưu ý API/công cụ free tier có thể dùng dữ liệu để huấn luyện (xem `02-guide.md` §3.4).
5. **Không cố suy ngược danh tính** từ dữ liệu đã ẩn danh ([học viên], mã U/C/T/M).
6. Sau sự kiện, **xoá các bản sao data pack** khỏi máy cá nhân và các công cụ đã upload nếu ban tổ chức yêu cầu.

Vi phạm được xử lý theo quy định của khoá và có thể ảnh hưởng trực tiếp đến điểm của nhóm.
