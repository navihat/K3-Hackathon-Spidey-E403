# Reflection — Trương Văn Thái (2A202601801)

> Khung 4 mục theo rubric reflection. **Phần trả lời phải tự viết bằng lời của mình** —
> CP5/CP6 hỏi ngẫu nhiên "phần này hoạt động thế nào?", không giải thích được thì phần đó 0 điểm.
> Các bảng "để tra khi viết" bên dưới là dữ kiện có thật trong repo, không phải câu trả lời.

## 1. Vai trò

_(viết)_ — Phân công trong `spec.md` §8: **Code prototype + Demo**.

## 2. Phần mình làm

_(viết: mình đã dựng gì, quyết định kỹ thuật nào là của mình, chỗ nào nhờ AI sinh rồi mình sửa)_

**Để tra khi viết** — những chỗ mang tên mình trong repo:

| Thành phần | File | Quyết định đằng sau nó |
|---|---|---|
| Retrieval | [`codebase/timlai/index.py`](../codebase/timlai/index.py) | Chọn SQLite FTS5 + BM25 thay vì vector DB · `remove_diacritics 2` để "buoi" khớp "buổi" · tách `ORDER BY rank` khỏi `ORDER BY thoi_diem DESC` |
| Quyết định AI | [`codebase/timlai/tra_cuu.py`](../codebase/timlai/tra_cuu.py) | `neo()` chống bịa bằng code chứ không bằng prompt · `canh_bao_cu()` tính ngày bằng code · không import discord để eval chạy được ngoài Discord |
| Trình bày | [`codebase/timlai/render.py`](../codebase/timlai/render.py) | 4 đường đi trải nghiệm = 4 màu embed · hiện số kết luận bị bỏ ra footer thay vì giấu |
| Discord | [`codebase/timlai/bot.py`](../codebase/timlai/bot.py) | `defer()` vì lời gọi AI >3s · index cả tên file đính kèm vì slide thường là PDF |
| Đo | [`codebase/scripts/chay_eval.py`](../codebase/scripts/chay_eval.py) | Chế độ `--gia` kiểm runner trước khi tốn token |

## 3. AI hỗ trợ thế nào

_(viết: dùng AI ở khâu nào, chỗ nào AI làm sai mà mình phải sửa, chỗ nào mình không dùng AI và vì sao)_

## 4. Một bài học từ case fail của chính nhóm

_(viết — chọn MỘT case cụ thể, không nói chung chung)_

**Để tra khi viết** — các case fail có thật đã ghi lại:

- Lượt eval bằng LLM giả ([`eval/ket-qua/luot-1.md`](../eval/ket-qua/luot-1.md)): 19/22 case bịa nguồn — đúng bằng thiết kế, vì `neo()` bắt được id giả. Nó chứng minh cái gì về chỗ đặt hàng rào an toàn?
- Đợt `503 UNAVAILABLE` khi chạy lượt eval thật: retry cũ chỉ bắt 429 nên một cú 503 giết cả lượt 22 case. Sửa ở `_LOI_TAM_THOI` trong `tra_cuu.py` + `SO_LAN_THU` trong `config.py`.
- Đo tay model 30/07: tắt `thinking` thì model trả 2 message_id cho "slide buổi 5" thay vì chọn bản mới nhất — hỏng luật 5 trong `SYSTEM`, đúng rủi ro lớp ④.

## Bộ câu hỏi hay bị vặn ở CP5/CP6 — tự trả lời trước

1. "Bot chống bịa link bằng cách nào?" → nói được tại sao **không** đặt hàng rào ở prompt.
2. "Vì sao FTS5 chứ không phải embedding?" → nói được cái mình đánh đổi.
3. "Vì sao `tra_cuu.py` không được import discord?"
4. "Case nào nguy hiểm nhất nếu bot sai?" → lớp ① và lớp ④, và vì sao ④ nguy hiểm hơn người ta tưởng.
5. "Con số 0 case bịa nguồn đo bằng gì?" → cột `Bỏ` trong bảng `eval/ket-qua/`.
