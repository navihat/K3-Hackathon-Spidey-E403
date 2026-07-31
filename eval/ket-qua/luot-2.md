# Kết quả golden set — lượt 2

- Thời điểm: 2026-07-31 04:37
- Model: `gemini-3.1-flash-lite`
- Phạm vi: 22 case (trọn bộ)
- Đo được: **22/22** case
- Index: 20 tin nhắn
- Lệnh: `python scripts/chay_eval.py --model gemini-3.1-flash-lite`

**Vì sao không phải model khai trong spec §9?** Lượt này chạy 31/07. `gemini-3.5-flash` (model chốt
30/07) trả **503 UNAVAILABLE** liên tục — thử lại 4 lần với backoff tới 104s vẫn 503. Chuyển sang
`gemini-3.6-flash` thì chạy được 20 case rồi ăn **429 với `quotaValue: 20`** — free tier chỉ cho
**20 lời gọi mỗi ngày cho mỗi model**, mà golden set có 22 case. `gemini-3.1-flash-lite` là model
chạy hết được trọn bộ, và 1,1s/lời gọi vẫn dưới mốc <5s ở spec §7. Quality bar **không đổi** theo model.

## Đối chiếu quality bar

| Chỉ số | Bar (spec.md §7) | Đo được | Kết luận |
|---|---|---|---|
| Tỉ lệ pass | ≥85% | **81.8%** (18/22) | CHƯA ĐẠT |
| Case bịa nguồn | =0 | **0** | ĐẠT |

## Từng case

| ID | Lớp | Input | Pass | Bịa | Lệch ở đâu | Model | Ứng viên | Nguồn | Bỏ | Bot trả lời |
|---|---|---|---|---|---|---|---|---|---|---|
| TH-01 | thuong | link slide buổi 5 | ✓ |  | — | 3.1-flash-lite | 11 | 1 | 0 | Đây là bản cập nhật mới nhất của slide buổi 5 đã được LabCoach Minh chia sẻ. Bạn có thể truy cập tài liệu này để xem nội |
| TH-02 | thuong | slide buổi 3 | ✓ |  | — | 3.1-flash-lite | 13 | 1 | 0 | Đây là slide buổi 3 về Transformer & Attention mà bạn cần. |
| TH-03 | thuong | link bài lab 2 | ✓ |  | — | 3.1-flash-lite | 6 | 1 | 0 | Đây là link bài lab 2 về dựng RAG mini mà bạn cần. |
| TH-04 | thuong | link VLearn | ✓ |  | — | 3.1-flash-lite | 1 | 1 | 0 | Đây là đường dẫn truy cập nền tảng VLearn của khóa học. |
| TH-05 | thuong | tài liệu buổi 4 | ✓ |  | — | 3.1-flash-lite | 10 | 1 | 0 | Đây là tài liệu buổi 4 về RAG cơ bản mà bạn cần. |
| TH-06 | thuong | link build buổi 1 | ✓ |  | — | 3.1-flash-lite | 12 | 1 | 0 | Đây là link repo mẫu cho phần build buổi 1 mà bạn cần. |
| TH-07 | thuong | link lý thuyết buổi 2 | ✓ |  | — | 3.1-flash-lite | 12 | 1 | 0 | Đây là slide lý thuyết cho buổi 2 về Prompt engineering mà bạn cần. |
| TH-08 | thuong | link lab 1 | ✓ |  | — | 3.1-flash-lite | 6 | 1 | 0 | Đây là link bài Lab 1 về gọi API lần đầu mà bạn cần. |
| TH-09 | thuong | slide hackathon | ✓ |  | — | 3.1-flash-lite | 9 | 1 | 0 | Đây là slide cho cả Day 1 và Day 2 của hackathon mà bạn cần. |
| TH-10 | thuong | link aithucchien | ✓ |  | — | 3.1-flash-lite | 11 | 2 | 0 | Bạn có thể truy cập trang chủ khoá học tại aithucchien.vn hoặc nền tảng Codelabs để xem các bài lab. Dưới đây là các đườ |
| TH-11 | 1 | link slide buổi 10 | ✓ |  | — | 3.1-flash-lite | 11 | 0 | 0 | Rất tiếc, mình không tìm thấy link slide cho buổi 10 trong danh sách tin nhắn hiện có. Bạn vui lòng kiểm tra lại kênh th |
| TH-12 | 1 | link checkin | ✓ |  | — | 3.1-flash-lite | 0 | 0 | 0 | Mình không tìm thấy tin nhắn nào khớp với câu hỏi này. |
| TH-13 | 2 | link slide | ✓ |  | — | 3.1-flash-lite | 8 | 0 | 0 | Bạn đang cần tìm slide của buổi học nào? Hiện tại có nhiều slide cho các buổi khác nhau, bạn vui lòng cung cấp thêm thôn |
| TH-14 | 2 | slie buoi 5 | ✓ |  | — | 3.1-flash-lite | 10 | 1 | 0 | Đây là bản cập nhật mới nhất của slide buổi 5 đã được sửa lỗi trang 12. Bạn có thể sử dụng tài liệu này để học tập. |
| TH-15 | 3 | giải thích hàm softmax | ✗ |  | ngoai_pham_vi: cần True, được False | 3.1-flash-lite | 0 | 0 | 0 | Mình không tìm thấy tin nhắn nào khớp với câu hỏi này. |
| TH-16 | 3 | bài tập buổi 3 làm thế nào | ✓ |  | — | 3.1-flash-lite | 13 | 0 | 0 | Rất tiếc, tôi không thể hướng dẫn giải bài tập cụ thể. Bạn vui lòng đặt câu hỏi tại kênh hỏi-đáp của khóa học hoặc liên  |
| TH-17 | 4 | link lab 2 | ✓ |  | — | 3.1-flash-lite | 6 | 1 | 0 | Đây là link bài Lab 2 về dựng RAG mini mà bạn cần. |
| TH-18 | 4 | link slide buổi 5 bản mới nhất | ✓ |  | — | 3.1-flash-lite | 12 | 1 | 0 | Đây là bản cập nhật mới nhất của slide buổi 5, đã được sửa lỗi ở trang 12. |
| TH-19 | hiem | link slide của anh Tuấn | ✗ |  | tim_thay: cần True, được False | 3.1-flash-lite | 8 | 0 | 0 | Hiện tại có nhiều slide của anh Tuấn và các LabCoach khác nhau trong các buổi học. Bạn vui lòng cho biết cụ thể bạn đang |
| TH-20 | hiem | cho em xin lại link slide với ạ | ✓ |  | — | 3.1-flash-lite | 8 | 0 | 0 | Hiện tại có nhiều slide cho các buổi học khác nhau, bạn vui lòng cho biết bạn cần slide của buổi học nào để mình hỗ trợ  |
| TH-21 | hiem | link buổi hôm qua | ✗ |  | can_lam_ro: cần True, được False; do_tin_cay: cần thap, được cao | 3.1-flash-lite | 10 | 1 | 0 | Tài liệu buổi học gần nhất là buổi 6 về Đánh giá & kiểm thử. Bạn có thể truy cập link bên dưới để xem nội dung. |
| TH-22 | hiem | link | ✗ |  | can_lam_ro: cần True, được False | 3.1-flash-lite | 0 | 0 | 0 | Mình không tìm thấy tin nhắn nào khớp với câu hỏi này. |

## Phân tích case chưa đạt

Bốn case trượt quy về **hai nguyên nhân**, không phải bốn.

### Nguyên nhân A — đường tắt "0 ứng viên" nuốt luôn việc phân loại (TH-15, TH-22)

`tra_cuu()` có một đường tắt: FTS5 không trả ứng viên nào thì **không gọi AI**, trả thẳng một câu
cố định `"Mình không tìm thấy tin nhắn nào khớp với câu hỏi này."` với `ngoai_pham_vi=False`,
`can_lam_ro=None` ([`codebase/timlai/tra_cuu.py`](../../codebase/timlai/tra_cuu.py), nhánh `if not ung_vien`).
Đường tắt này tiết kiệm một lời gọi, nhưng nó cũng cắt mất khả năng nhận ra **đây là loại câu hỏi gì**.

- **TH-15** (lớp ③) — lệch: `ngoai_pham_vi: cần True, được False`
  - Mong đợi: câu hỏi kiến thức → từ chối + chỉ sang kênh hỏi-đáp / AI Tutor
  - Nguyên nhân: **thiết kế, không phải prompt.** 0 ứng viên → AI không được hỏi → không ai phân loại được ③.
    Bằng chứng: **TH-16 cũng là lớp ③ và PASS** — chỉ khác ở chỗ nó có 13 ứng viên nên AI được gọi và từ chối đúng.
    Cùng một prompt, cùng một lớp, khác kết quả chỉ vì số ứng viên.
- **TH-22** (lớp hiếm) — lệch: `can_lam_ro: cần True, được False`
  - Mong đợi: input quá cụt → hỏi lại kèm ví dụ câu hỏi tốt
  - Nguyên nhân: cùng đường tắt trên. Chữ "link" không xuất hiện trong nội dung tin nhắn nào (tin chứa URL
    chứ không chứa chữ "link"), nên FTS5 trả 0 và câu trả lời cố định không có chỗ để hỏi lại.

**Hướng sửa**: gọi AI **cả khi danh sách ứng viên rỗng**, để nó phân loại ③/② thay vì trả câu cố định.
An toàn vẫn giữ nguyên vì `neo()` chặn ở tầng code: rỗng ứng viên thì mọi message_id đều bị bỏ, `tim_thay`
tự động hạ về `False`. Đánh đổi: tốn thêm 1 lời gọi cho những câu hiện đang **miễn phí** — cân nhắc với
hạn mức 20 lời gọi/ngày của free tier. Rủi ro cần đo: TH-12 (`link checkin`, cũng 0 ứng viên) đang PASS,
sau khi sửa AI có thể gán `ngoai_pham_vi=True` và làm case đó lệch mong đợi.

### Nguyên nhân B — luật prompt thua tín hiệu thứ tự ứng viên (TH-19, TH-21)

- **TH-21** (lớp hiếm) — lệch: `can_lam_ro: cần True, được False; do_tin_cay: cần thap, được cao`
  - Mong đợi: thời gian tương đối → hỏi lại, **không tự đoán ngày**
  - Nguyên nhân: **đây là case trượt nguy hiểm nhất của lượt này.** Bot không nói "mình không chắc" — nó
    trả lời chắc nịch *"Tài liệu buổi học gần nhất là buổi 6"* kèm link, `do_tin_cay=cao`. Luật 3 trong
    `SYSTEM` có nêu đích danh chữ "hôm qua" phải hỏi lại, nhưng `truy_xuat()` xếp tin **mới nhất lên đầu**
    prompt, và tín hiệu vị trí đó thắng luật chữ. Sai kiểu này tệ hơn trả lời "không tìm thấy": học viên
    không có cách nào biết bot vừa đoán.
  - Hướng sửa: ngày tháng là việc của code, không hỏi LLM — cùng nguyên tắc đã áp cho `canh_bao_cu()`.
    Bắt cụm thời gian tương đối ("hôm qua", "buổi trước", "tuần trước") trước khi gọi AI, quy ra ngày cụ
    thể rồi lọc; không quy được thì ép `can_lam_ro`. Đây là hành vi `spec.md` §5 kịch bản 10 đã cam kết
    nhưng code chưa làm.
- **TH-19** (lớp hiếm) — lệch: `tim_thay: cần True, được False`
  - Mong đợi: lọc theo tên người gửi
  - Nguyên nhân: **prompt thiếu luật.** `SYSTEM` không có luật nào nói về việc lọc theo `tác giả`, dù dòng
    ứng viên có sẵn trường đó. Trong 8 ứng viên chỉ có **đúng 1** tin do "anh Tuấn" gửi (slide buổi 3), nhưng
    model coi câu hỏi là mơ hồ và hỏi lại. Đây là case dễ sửa nhất trong bốn case: thêm một luật lọc theo
    người gửi vào `SYSTEM`.

### Chốt lại

| Chỉ số | Kết luận |
|---|---|
| Tỉ lệ pass 81.8% | **Chưa đạt** bar ≥85% — thiếu đúng 1 case (19/22 = 86.4% là qua) |
| 0 case bịa nguồn | **Đạt** — không lời gọi nào trả về message_id không tồn tại; cột `Bỏ` toàn 0 |
| Lớp ① (TH-11, TH-12) | Cả hai đều pass — phần an toàn nhất của hệ thống |
| Lớp ② (TH-13, TH-14) | Cả hai đều pass |
| Lớp ③ (TH-15, TH-16) | 1/2 — hỏng khi retrieval không trả ứng viên nào |
| Lớp ④ (TH-17, TH-18) | Cả hai đều pass, kể cả case chọn đúng bản slide mới nhất |

Không case nào trong bốn case trượt thuộc nhóm "thường" — 10/10 case thường đều pass. Chỗ hệ thống yếu
là **rìa**: câu hỏi không khớp từ khoá nào, và câu hỏi có yếu tố thời gian tương đối.
