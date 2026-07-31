# validation/ — vòng đo bằng người

> **Trạng thái: CHƯA CHẠY.** [`feedback-log.md`](feedback-log.md) hiện là bảng trống.
> Không được điền phỏng đoán vào đó — rubric chấm quote **nguyên văn** kèm tên/vai;
> số liệu bịa hoặc chỉnh sửa thì không được tính điểm.

Chấm cho rubric **R6 · 8 điểm**:

| Điều kiện | Điểm | Đạt khi |
|---|---|---|
| Feedback log ≥5 mẩu từ ≥5 người **ngoài nhóm**, có ≥2 willing user đã khai từ CP1, quote nguyên văn + tên/vai | 4 | 5 dòng trong `feedback-log.md` được điền đủ |
| ≥1 thay đổi từ feedback ghi trong Changelog `spec.md` §9 — hoặc giữ nguyên **có lý do căn cứ** | 4 | Mục "Đã quyết" ở cuối `feedback-log.md` + dòng tương ứng trong §9 |

## Một phiên 10 phút/người

**① Giao task thật rồi im lặng quan sát.** Không thuyết minh, không gợi ý. Ghi họ gõ gì, kẹt ở đâu, mất bao lâu.

Ba task xếp theo độ khó — giao ít nhất task 1 và task 3 cho mỗi người. Nếu chỉ giao task 1
thì phiên test sẽ toàn lời khen và **không tính là đạt** (02-guide.md §4.2).

| # | Task giao cho người thử (đọc nguyên văn) | Đang thử chỗ khó nào |
|---|---|---|
| 1 | "Bạn cần xem lại slide buổi 5. Dùng cái này tìm giúp mình." | happy path |
| 2 | "Bạn không nhớ là buổi mấy, chỉ nhớ có slide. Tìm thử xem." | ② mơ hồ — bot phải hỏi lại, không được tự đoán |
| 3 | "Tìm giúp mình link slide buổi 10." | ① không căn cứ — buổi 10 **không tồn tại**; bot bịa link là fail quality bar |

Task 3 là task quan trọng nhất: nó kiểm chính xác thứ `spec.md` §7 cam kết (0 case bịa nguồn),
và kiểm luôn việc người dùng **có nhận ra** bot đang từ chối hay tưởng bot hỏng.

**② Hỏi đúng 3 câu, không thêm bớt:**

1. "Điều gì khó hiểu hoặc khó chịu nhất?"
2. "Kết quả này bạn có tin không — vì sao?"
3. "Bạn có dùng thật không — vì sao / vì sao chưa?"

**③ Log nguyên văn** vào `feedback-log.md` — chép đúng chữ họ nói, kể cả nói cụt hoặc chê.
Đừng diễn giải lại cho hay hơn.

## Chọn người thử

≥5 người **ngoài nhóm**, trong đó ≥2 là willing user đã khai ở CP1 (`spec.md` §8 — hiện vẫn là
placeholder, phải điền tên thật trước khi chạy phiên). Đổi chéo với nhóm khác trong zone là
nhanh nhất, và ai trong khoá cũng là user thật của sản phẩm này.

## Sau khi chạy xong

1. Điền đủ 5 dòng bảng + 4 dòng tổng hợp trong `feedback-log.md`.
2. Chọn **1-2 thay đổi** làm trước demo → ghi vào `spec.md` §9 Changelog kèm lý do.
3. Thứ quyết định **giữ nguyên** cũng phải ghi lý do — rubric chấp nhận "giữ nguyên có căn cứ",
   nhưng không chấp nhận im lặng.
4. Phần chưa xử lý → slide 6 "Nếu có thêm 1 tuần".
