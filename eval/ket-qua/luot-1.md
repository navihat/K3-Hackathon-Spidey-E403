# Kết quả golden set — lượt 1

- Thời điểm: 2026-07-30 17:13
- Model: `gemini-2.5-flash`  ⚠️ **LLM GIẢ — không phải kết quả thật**
- Phạm vi: 22 case (trọn bộ)
- Index: 20 tin nhắn

## Đối chiếu quality bar

| Chỉ số | Bar (spec.md §7) | Đo được | Kết luận |
|---|---|---|---|
| Tỉ lệ pass | ≥85% | **72.7%** (16/22) | CHƯA ĐẠT |
| Case bịa nguồn | =0 | **19** | CHƯA ĐẠT |

## Từng case

| ID | Lớp | Input | Pass | Bịa | Lệch ở đâu | Ứng viên | Nguồn | Bỏ | Bot trả lời |
|---|---|---|---|---|---|---|---|---|---|
| TH-01 | thuong | link slide buổi 5 | ✓ | ⚠️ | — | 11 | 1 | 1 | [GIẢ] 11 ứng viên cho: link slide buổi 5 |
| TH-02 | thuong | slide buổi 3 | ✓ | ⚠️ | — | 13 | 1 | 1 | [GIẢ] 13 ứng viên cho: slide buổi 3 |
| TH-03 | thuong | link bài lab 2 | ✓ | ⚠️ | — | 6 | 1 | 1 | [GIẢ] 6 ứng viên cho: link bài lab 2 |
| TH-04 | thuong | link VLearn | ✓ | ⚠️ | — | 1 | 1 | 1 | [GIẢ] 1 ứng viên cho: link VLearn |
| TH-05 | thuong | tài liệu buổi 4 | ✓ | ⚠️ | — | 10 | 1 | 1 | [GIẢ] 10 ứng viên cho: tài liệu buổi 4 |
| TH-06 | thuong | link build buổi 1 | ✓ | ⚠️ | — | 12 | 1 | 1 | [GIẢ] 12 ứng viên cho: link build buổi 1 |
| TH-07 | thuong | link lý thuyết buổi 2 | ✓ | ⚠️ | — | 12 | 1 | 1 | [GIẢ] 12 ứng viên cho: link lý thuyết buổi 2 |
| TH-08 | thuong | link lab 1 | ✓ | ⚠️ | — | 6 | 1 | 1 | [GIẢ] 6 ứng viên cho: link lab 1 |
| TH-09 | thuong | slide hackathon | ✓ | ⚠️ | — | 9 | 1 | 1 | [GIẢ] 9 ứng viên cho: slide hackathon |
| TH-10 | thuong | link aithucchien | ✓ | ⚠️ | — | 11 | 1 | 1 | [GIẢ] 11 ứng viên cho: link aithucchien |
| TH-11 | 1 | link slide buổi 10 | ✗ | ⚠️ | tim_thay: cần False, được True | 11 | 1 | 1 | [GIẢ] 11 ứng viên cho: link slide buổi 10 |
| TH-12 | 1 | link checkin | ✓ |  | — | 0 | 0 | 0 | Mình không tìm thấy tin nhắn nào khớp với câu hỏi này. |
| TH-13 | 2 | link slide | ✗ | ⚠️ | can_lam_ro: cần True, được False; do_tin_cay: cần thap, được cao | 8 | 1 | 1 | [GIẢ] 8 ứng viên cho: link slide |
| TH-14 | 2 | slie buoi 5 | ✓ | ⚠️ | — | 10 | 1 | 1 | [GIẢ] 10 ứng viên cho: slie buoi 5 |
| TH-15 | 3 | giải thích hàm softmax | ✗ |  | ngoai_pham_vi: cần True, được False | 0 | 0 | 0 | Mình không tìm thấy tin nhắn nào khớp với câu hỏi này. |
| TH-16 | 3 | bài tập buổi 3 làm thế nào | ✗ | ⚠️ | tim_thay: cần False, được True; ngoai_pham_vi: cần True, được False | 13 | 1 | 1 | [GIẢ] 13 ứng viên cho: bài tập buổi 3 làm thế nào |
| TH-17 | 4 | link lab 2 | ✓ | ⚠️ | — | 6 | 1 | 1 | [GIẢ] 6 ứng viên cho: link lab 2 |
| TH-18 | 4 | link slide buổi 5 bản mới nhất | ✓ | ⚠️ | — | 12 | 1 | 1 | [GIẢ] 12 ứng viên cho: link slide buổi 5 bản mới nhất |
| TH-19 | hiem | link slide của anh Tuấn | ✓ | ⚠️ | — | 8 | 1 | 1 | [GIẢ] 8 ứng viên cho: link slide của anh Tuấn |
| TH-20 | hiem | cho em xin lại link slide với ạ | ✓ | ⚠️ | — | 8 | 1 | 1 | [GIẢ] 8 ứng viên cho: cho em xin lại link slide với ạ |
| TH-21 | hiem | link buổi hôm qua | ✗ | ⚠️ | can_lam_ro: cần True, được False; do_tin_cay: cần thap, được cao | 10 | 1 | 1 | [GIẢ] 10 ứng viên cho: link buổi hôm qua |
| TH-22 | hiem | link | ✗ |  | can_lam_ro: cần True, được False | 0 | 0 | 0 | Mình không tìm thấy tin nhắn nào khớp với câu hỏi này. |

## Phân tích case chưa đạt

- **TH-11** (lớp 1) — lệch: tim_thay: cần False, được True
  - Mong đợi: Chưa có buổi 10 → phải nói không tìm thấy, KHÔNG được tạo link
  - Nguyên nhân: _(điền tay: retrieval trượt / prompt / schema / mong đợi sai)_
- **TH-13** (lớp 2) — lệch: can_lam_ro: cần True, được False; do_tin_cay: cần thap, được cao
  - Mong đợi: Không rõ buổi mấy → hỏi lại, liệt kê lựa chọn tìm được
  - Nguyên nhân: _(điền tay: retrieval trượt / prompt / schema / mong đợi sai)_
- **TH-15** (lớp 3) — lệch: ngoai_pham_vi: cần True, được False
  - Mong đợi: Câu hỏi kiến thức → từ chối + chỉ sang kênh hỏi-đáp / AI Tutor
  - Nguyên nhân: _(điền tay: retrieval trượt / prompt / schema / mong đợi sai)_
- **TH-16** (lớp 3) — lệch: tim_thay: cần False, được True; ngoai_pham_vi: cần True, được False
  - Mong đợi: Đòi hướng dẫn làm bài → từ chối, chỉ sang Lab Coach
  - Nguyên nhân: _(điền tay: retrieval trượt / prompt / schema / mong đợi sai)_
- **TH-21** (lớp hiem) — lệch: can_lam_ro: cần True, được False; do_tin_cay: cần thap, được cao
  - Mong đợi: Thời gian tương đối → hỏi lại, không tự đoán ngày
  - Nguyên nhân: _(điền tay: retrieval trượt / prompt / schema / mong đợi sai)_
- **TH-22** (lớp hiem) — lệch: can_lam_ro: cần True, được False
  - Mong đợi: Quá ngắn → hỏi lại kèm ví dụ câu hỏi tốt
  - Nguyên nhân: _(điền tay: retrieval trượt / prompt / schema / mong đợi sai)_
