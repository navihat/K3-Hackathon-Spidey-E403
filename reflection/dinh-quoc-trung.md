# Reflection — Đinh Quốc Trung

> Khung 4 mục theo rubric reflection. **Phần trả lời phải tự viết bằng lời của mình** —
> CP5/CP6 hỏi ngẫu nhiên "phần này hoạt động thế nào?", không giải thích được thì phần đó 0 điểm.

## 1. Vai trò

_(viết)_ — Phân công trong `spec.md` §8: **Prompt + golden set**.

## 2. Phần mình làm

_(viết: 6 luật trong SYSTEM ra đời thế nào, vì sao golden set chia 10/8/4, case nào mình cố tình đặt bẫy)_

**Để tra khi viết** — artifact mang tên mình:

| Phần | File | Nội dung |
|---|---|---|
| Prompt lõi | `SYSTEM` trong [`codebase/timlai/tra_cuu.py`](../codebase/timlai/tra_cuu.py) | 6 luật: chỉ dùng ứng viên · copy nguyên id · mơ hồ thì hỏi lại · câu hỏi kiến thức thì từ chối · ưu tiên tin mới nhất · trả lời ≤3 câu |
| Golden set | [`eval/golden-set.md`](../eval/golden-set.md) · [`.yaml`](../eval/golden-set.yaml) | 22 case: 10 thường · 2/lớp ①②③④ · 4 hiếm |
| Chiều chất lượng | [`spec.md`](../spec.md) §7 | Đúng link · đúng nội dung · có căn cứ · an toàn · <5 giây |
| Kịch bản rủi ro | [`spec.md`](../spec.md) §5-§6 | 10 kịch bản + 4 đường đi trải nghiệm |

## 3. AI hỗ trợ thế nào

_(viết: dùng AI sinh case hay tự nghĩ? AI sinh ra case nào vô dụng mà mình phải bỏ?)_

## 4. Một bài học từ case fail của chính nhóm

_(viết — chọn MỘT case cụ thể)_

**Để tra khi viết** — các chỗ prompt/golden set đã lộ ra vấn đề:

- TH-11 ("link slide buổi 10") và TH-12 ("link checkin") chỉ có nghĩa khi seed **không** đăng slide buổi 10 và **không** đăng QR checkin. Bẫy nằm ở dữ liệu, không nằm ở câu hỏi. Nếu ai đó lỡ seed thêm hai thứ đó thì hai case này mất tác dụng mà bảng kết quả vẫn báo "pass".
- Lượt eval bằng LLM giả cho thấy: prompt bảo "không được bịa id" nhưng LLM vẫn bịa được — thứ chặn thật sự là `neo()` trong code. Bài học về chỗ nên đặt hàng rào an toàn.
- Luật 5 ("ưu tiên tin mới nhất") chỉ chạy đúng khi retrieval đưa tin mới lên đầu prompt. Prompt đúng mà thứ tự ứng viên sai thì vẫn ra kết quả sai — TH-18 là case bắt chuyện đó.

## Bộ câu hỏi hay bị vặn ở CP5/CP6 — tự trả lời trước

1. "Golden set có bao nhiêu case cho mỗi lớp chỗ khó, và vì sao chia như vậy?"
2. "Case nào trong golden set là khó nhất, vì sao?"
3. "Nếu bot fail TH-11 thì sửa ở prompt hay sửa ở đâu?" → câu trả lời **không phải** là prompt.
4. "Định nghĩa 'đúng link' kiểm chứng được thế nào — người ngoài nhóm chấm có ra cùng kết quả không?"
