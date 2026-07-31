# Reflection — Trương Thảo Nguyên

> Khung 4 mục theo rubric reflection. **Phần trả lời phải tự viết bằng lời của mình** —
> CP5/CP6 hỏi ngẫu nhiên "phần này hoạt động thế nào?", không giải thích được thì phần đó 0 điểm.

## 1. Vai trò

_(viết)_ — Phân công trong `spec.md` §8: **Spec + evidence**.

## 2. Phần mình làm

_(viết: thiết kế khảo sát thế nào, thu 36 phản hồi ra sao, từ số liệu đi tới quyết định chọn ứng viên A bằng đường nào)_

**Để tra khi viết** — artifact mang tên mình:

| Phần | File | Nội dung |
|---|---|---|
| Log khảo sát | [`data/khao-sat-log.csv`](../data/khao-sat-log.csv) · [`.md`](../data/khao-sat-log.md) | 36 phản hồi, đủ câu hỏi + từng câu trả lời |
| Evidence & JTBD | [`spec.md`](../spec.md) §1 | 86% từng không tìm được · 84% cần slide · 84% phải check 2-3 kênh · 77% khó chịu |
| Bảng impact | [`spec.md`](../spec.md) §2 | 4 ứng viên A/B/C/D + lý do loại B, C, D bằng số |
| Giải pháp tương tự | [`spec.md`](../spec.md) §3 | ChatGPT · Discord Search · Notion AI — đáng học gì, đáng né gì |

## 3. AI hỗ trợ thế nào

_(viết: dùng AI ở khâu nào — soạn câu hỏi khảo sát? tổng hợp CSV? — và chỗ nào mình phải tự kiểm lại vì AI đếm sai)_

## 4. Một bài học từ case fail của chính nhóm

_(viết — chọn MỘT case cụ thể)_

**Để tra khi viết** — vài chỗ evidence suýt dẫn sai:

- Ứng viên D (link VLearn, 52%) gần như luôn đi kèm nhu cầu tìm slide. Nếu tách thành tính năng riêng thì đếm trùng người. Phát hiện ra lúc nào, bằng cách nào?
- 5/36 người trả lời "Không" ở câu đầu → mẫu số thật là 31 chứ không phải 36. Lấy nhầm mẫu số thì mọi tỉ lệ trong spec sai theo.
- Câu hỏi "Bạn sẽ dùng bot trong tình huống nào?" cho phép chọn nhiều đáp án → không cộng ra 100% được. Chỗ này dễ báo cáo sai nhất.

## Bộ câu hỏi hay bị vặn ở CP5/CP6 — tự trả lời trước

1. "31/36 là 31 trên tổng bao nhiêu người được hỏi, và ai bị loại khỏi mẫu?"
2. "Vì sao chọn A chứ không phải B khi B cũng 58%?" → trả lời bằng số, không bằng cảm tính.
3. "Khảo sát này có bị dẫn dắt câu trả lời không?" → chỉ ra một câu hỏi mình đã cân nhắc sửa.
4. "Con số 23% bỏ cuộc lấy từ cột nào trong CSV?"
