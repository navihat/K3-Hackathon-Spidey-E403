# CLAUDE.md — Bối cảnh & luật chơi khi phát triển ý tưởng

File này để Claude (và người) **xây dựng / mở rộng / phản biện ý tưởng** cho repo hackathon
này mà không đi chệch spec đã chốt. Nguồn sự thật của sản phẩm là [`spec.md`](spec.md);
file này là bản rút gọn + quy trình làm việc quanh nó.

## 1. Sản phẩm — một câu

> Một học viên gõ câu hỏi tự nhiên trong Discord ("link slide buổi 5") → AI tìm trong tin nhắn
> của **5 kênh chỉ định** → trả về link tài liệu kèm tên người gửi + link tới tin nhắn gốc;
> không có căn cứ thì nói **"Mình không tìm thấy"**, tuyệt đối không bịa link.

- **JTBD**: tìm lại tài liệu/deadline/câu trả lời LabCoach đã gửi trong Discord mà không phải scroll nhiều kênh.
- **Evidence** (khảo sát 36 người ngoài nhóm, log tại [`data/khao-sat-log.csv`](data/khao-sat-log.csv)):
  86% từng không tìm được thông tin trong 7 ngày qua · 84% cần slide/tài liệu · 84% phải check 2-3 kênh ·
  48% mất 5-15 phút · 77% khó chịu · 23% bỏ cuộc.
- **Automation**: `conditional` — chỉ trả link khi có ≥1 match neo được vào tin nhắn thật.
- **Mức prototype khai báo**: **Working** (AI thật ở lõi + chạy trong Discord server test).

## 2. Bốn ràng buộc bất biến

Mọi ý tưởng mới phải đi qua bốn cửa này trước khi được đề xuất:

1. **Quality bar đã đông cứng** (spec §7, chốt 23:59 ngày 1): *≥85% pass golden set và **0 case bịa nguồn** (lớp ①)*.
   Không sửa con số này — kể cả khi đo ra thấp. Rubric cho điểm cho số liệu **trung thực**, trừ điểm cho số liệu bị che.
2. **Non-goals** (spec §4) — không trả lời câu hỏi kiến thức · không push chủ động · chỉ tiếng Việt ·
   không index ngoài 5 kênh. Ý tưởng vi phạm non-goal thì hoặc bỏ, hoặc sửa non-goal **và** ghi vào changelog §9 kèm lý do.
3. **Data**: chỉ dùng `data/` hoặc data giả tự sinh ([`codebase/scripts/seed_gia.py`](codebase/scripts/seed_gia.py)).
   Không copy tin nhắn thật của người thật vào repo. `index.db` và `.env` bị `.gitignore` chặn — giữ nguyên.
4. **Lát cắt là MỘT câu**: 1 user · 1 việc · 1 quyết định AI · 1 kết quả. Ý tưởng nào làm câu này dài ra
   hoặc thêm quyết định AI thứ hai thì để dành cho phần "mở rộng sau", không nhét vào prototype.

## 3. Quy trình đề xuất một ý tưởng mới

Khi được hỏi "nên làm thêm gì / cải thiện gì", trả lời theo đúng bộ khung này — đây cũng là thứ rubric chấm:

1. **Pain**: ai — đang làm gì — vướng đâu — hậu quả gì. Không được dừng ở "mọi người thấy bất tiện".
2. **Bằng chứng**: trỏ về con số có thật trong [`data/khao-sat-log.md`](data/khao-sat-log.md) hoặc `data/vlearn-pack/`.
   Không có số → nói thẳng là **giả định chưa có bằng chứng**, đừng bịa tỉ lệ.
3. **Impact**: bao nhiêu người × tần suất × tốn gì mỗi lần × build nổi trong thời gian còn lại không.
4. **Đối chiếu 4 ràng buộc §2** ở trên.
5. **Chỗ khó**: ý tưởng này đẻ thêm case nào ở lớp ① bịa · ② mơ hồ · ③ ngoài phạm vi · ④ đặc thù domain?
6. **Đo thế nào**: thêm case nào vào [`eval/golden-set.yaml`](eval/golden-set.yaml), pass/fail định nghĩa ra sao.
7. **Chi phí lan toả**: dùng bảng §4 dưới đây để liệt kê hết file phải sửa.

Ý tưởng nào không qua được bước 2 hoặc bước 6 thì xếp vào mục "ý tưởng để dành", đừng code.

## 4. Sửa một chỗ thì phải sửa những chỗ nào

Spec, code, eval và README **phải khớp nhau** — rubric chấm chéo giữa chúng, lệch một chỗ là mất điểm ở cả hai đầu.

| Ý tưởng chạm vào | Kéo theo phải sửa |
|---|---|
| Đổi/thêm kênh được index | `spec.md` §4 · `codebase/.env.example` (`KENH_INDEX`) · bảng kênh ở `codebase/README.md` §3B · `ghi_chu` trong `eval/golden-set.yaml` |
| Thêm loại câu hỏi bot phải xử lý | luật trong `SYSTEM` ([`codebase/timlai/tra_cuu.py`](codebase/timlai/tra_cuu.py)) · kịch bản `spec.md` §5 · case mới trong `eval/golden-set.yaml` · test trong `codebase/tests/` |
| Đổi hành vi khi mơ hồ / từ chối | `SYSTEM` luật 3-4 · [`codebase/timlai/render.py`](codebase/timlai/render.py) · `spec.md` §6 (4 đường đi) |
| Đổi model hoặc tham số LLM | [`codebase/timlai/config.py`](codebase/timlai/config.py) (kèm số đo tay) · `spec.md` §9 changelog · đo lại mốc **< 5 giây** ở §7 |
| Thêm nguyên tắc HAX/PAIR | `spec.md` §4b — mỗi nguyên tắc **phải trỏ được vào một dòng code thật**, nếu không thì không tính điểm |
| Đổi cách chống bịa | `neo()` trong `tra_cuu.py` (**không** sửa bằng prompt) · `test_tra_cuu.py` · chạy lại `chay_eval.py --gia` |

## 5. Ranh giới — cái gì trong làn, cái gì ngoài

**Trong làn** (đã có evidence, chỉ là chưa build): gom tìm link VLearn/Phoenix/codelabs vào cùng luồng
(ứng viên D, 52%) · lọc theo người gửi · xử lý thời gian tương đối ("hôm qua", TH-21).

**Đã cân nhắc và loại** (spec §2) — đừng đề xuất lại trừ khi có số mới:
- **B · Check deadline** — 58%, tần suất ~1 lần/tuần, deadline thường được pin nên dễ tìm hơn slide.
- **C · Xem lại câu trả lời TA** — ~1-2 lần/tháng, không có nguồn sự thật chuẩn.
- **D · Tìm link VLearn** — 52%, đi kèm nhu cầu tìm slide, gom được vào A sau.

**Ngoài làn**: trả lời kiến thức chuyên môn · gửi tin chủ động · đa ngôn ngữ · index kênh ngoài 5 kênh.

## 6. Trạng thái hiện tại & khoảng trống đang mở

Đã có: 3 lớp code chạy end-to-end · 18 pytest · golden set 22 case · bot `/timlai` chạy trong server test ·
**lượt đo thật 22/22 case: 81.8% pass, 0 case bịa nguồn** ([`eval/ket-qua/luot-2.md`](eval/ket-qua/luot-2.md)) ·
README nhóm · khung `validation/` + `reflection/` · `demo-slides.pdf`.

Còn thiếu — cần **người thật** hoặc quyết định của nhóm, Claude không tự điền được:

| Khoảng trống | Rubric | Ghi chú |
|---|---|---|
| `validation/feedback-log.md` là bảng trống | R6 (8đ) | Chạy 5 phiên test theo [`validation/README.md`](validation/README.md). Không được suy đoán hộ người thử |
| Willing users `spec.md` §8 chưa có tên thật | R6 | Rubric đòi ≥2 willing user đã khai từ CP1 |
| Slide 5 của `demo-slides.html` là ô placeholder | demo | Điền ≥2 quote nguyên văn sau khi có validation, rồi in lại PDF |
| Mã HV của Trương Thảo Nguyên và Đinh Quốc Trung trong `README.md` | R7 (3đ) | |
| `reflection/*.md` mới là khung 4 mục | chấm riêng | Mỗi người tự viết — vibe-coding rule kiểm tại CP5 |
| Backup demo (screenshot/video) | `02-guide.md` §5.2 | Phòng khi live hỏng |

**Chưa đạt bar pass (81.8% < 85%), thiếu đúng 1 case.** Bốn case trượt quy về hai nguyên nhân, đã phân tích
trong `luot-2.md`; hướng sửa cho từng cái nằm ở slide 6. Nếu định sửa để đo lại: theo nhịp
`sửa MỘT thứ → chạy lại trọn bộ`, và nhớ **hạn 20 lời gọi/ngày/model** của free tier —
`chay_eval.py` chạy tiếp được nên hết hạn mức giữa chừng không mất kết quả đã đo.

## 7. Bản đồ code

Ba lớp, một chiều phụ thuộc: `bot.py → index.py → tra_cuu.py → render.py`.

- [`codebase/timlai/config.py`](codebase/timlai/config.py) — đọc `.env`, hằng số, ép UTF-8 cho console Windows.
- [`codebase/timlai/index.py`](codebase/timlai/index.py) — ② retrieval: SQLite FTS5 + BM25, `remove_diacritics 2` để khớp "buoi" ↔ "buổi"; `truy_xuat()` xếp tin **mới nhất lên đầu**.
- [`codebase/timlai/tra_cuu.py`](codebase/timlai/tra_cuu.py) — ③ quyết định AI. `SYSTEM` + `neo()` + `canh_bao_cu()`.
- [`codebase/timlai/render.py`](codebase/timlai/render.py) — 4 đường đi trải nghiệm, mỗi đường một màu embed.
- [`codebase/timlai/bot.py`](codebase/timlai/bot.py) — ① Discord client. Ba đường vào (`/timlai`, @mention, reply vào tin bot) đều gọi chung `hoi()`. Trả lời **công khai**. `KENH_TU_DONG` bật chế độ mọi-tin-là-câu-hỏi cho một kênh (mặc định tắt).
- `codebase/scripts/` — entry point chạy tay, **không chứa logic**. Logic cần test thì phải nằm trong `timlai/`.

**Ba quy tắc kiến trúc, đừng phá:**

1. `tra_cuu.py` **không import discord**. Đây là điều kiện để `chay_eval.py` chạy 22 case ngoài Discord (R4, 15 điểm).
2. **Chống bịa bằng code, không bằng prompt.** `neo()` bỏ mọi `message_id` không có trong danh sách ứng viên;
   khai `tim_thay=True` mà không neo được thì hạ xuống `False`. Số id bị bỏ là **số đo hallucination** — hiện lên footer, không nuốt im.
3. **Ngày tháng do code tính**, không hỏi LLM (`canh_bao_cu`).

## 8. Lệnh hay dùng

```powershell
cd codebase; .\.venv\Scripts\Activate.ps1

pytest tests -q                                    # ~0.2s, không cần API key — chạy sau mỗi lần sửa
python scripts/seed_gia.py                         # nạp 20 tin nhắn giả vào index.db
python scripts/thu_hoi.py "link slide buổi 5" --chi-loc   # chỉ xem FTS5, 0 token
python scripts/thu_hoi.py "link slide buổi 5"      # gọi AI thật, ~5s
python scripts/chay_eval.py --gia                  # kiểm runner bằng LLM giả — phải ra "bịa nguồn: 19"
python scripts/chay_eval.py --model <model>        # trọn bộ 22 case, ~2,5 phút → eval/ket-qua/
python scripts/chay_eval.py                        # chạy lại = đo tiếp phần còn thiếu (cache)
python -m timlai.bot                               # bot thật
```

**Hạn free tier: 20 lời gọi/ngày cho mỗi model** (đo 31/07 trên `gemini-3.6-flash`). Golden set 22 case
không chạy hết trong một ngày trên một model — đổi `--model` hoặc chạy lại hôm sau để đo nốt.

Chi tiết cài đặt, dựng server Discord, 9 case test tay và bảng lỗi thường gặp: [`codebase/README.md`](codebase/README.md).

## 9. Quy ước viết

- **Tiếng Việt** cho mọi thứ người đọc: tên hàm/biến (không dấu: `tra_cuu`, `ung_vien`, `do_tin_cay`),
  docstring, comment, tài liệu, câu trả lời của bot.
- Comment giải thích **vì sao**, không giải thích cái gì — và nếu là một quyết định đánh đổi thì kèm
  **số đo hoặc hậu quả cụ thể** (xem `config.py` dòng chọn model, `index.py` phần `ORDER BY`).
- Khi sửa spec: thêm một dòng vào **§9 Changelog** với thời điểm + đổi gì + **vì sao**.
- Ngày tháng trong tài liệu ghi tuyệt đối (`30/07`), không ghi "hôm qua".

## 10. Không được làm

- Sửa quality bar §7, hoặc làm đẹp số liệu eval.
- Commit `.env`, API key, `index.db`, hay data pack.
- Đưa tin nhắn thật của người thật vào seed/golden set.
- Sửa prompt để "chữa" một case fail của lớp ① — sửa ở `neo()` hoặc ở retrieval; prompt không phải hàng rào an toàn.
- Khai mức prototype cao hơn thực tế: mục nào mock thì ghi rõ là mock.
