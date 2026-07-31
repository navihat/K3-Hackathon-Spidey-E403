# Kết quả các lượt chạy golden set

Mỗi lượt `python codebase/scripts/chay_eval.py` ghi ra một file `luot-N.md` ở đây.
Commit **cả** lượt chưa đạt — rubric R4 chấm trên bảng đủ mọi case, kể cả case fail.

| Lượt | Ngày | Model | Độ phủ | Pass | Bịa nguồn | Ghi chú |
|---|---|---|---|---|---|---|
| [luot-1](luot-1.md) | 30/07 | — | 22/22 | 72.7% | 19 | ⚠️ **LLM giả** (`--gia`) — không phải kết quả thật. Chạy để kiểm runner: con số 19 chứng minh `neo()` bắt được id bịa |
| [luot-2](luot-2.md) | 31/07 | `gemini-3.1-flash-lite` | 22/22 | **81.8%** | **0** | Lượt đo thật đầu tiên. Chưa đạt bar 85%, đạt bar 0 bịa nguồn |

**Bar (spec.md §7, chốt 23:59 N1)**: ≥85% pass **và** 0 case bịa nguồn.

## Đọc bảng thế nào

- Cột **Bịa** ⚠️ = lời gọi đó trả về message_id không tồn tại (bị `neo()` bỏ), hoặc case lớp ①
  mà bot vẫn khai tìm thấy. Đây là số đo hallucination, không phải lỗi hiển thị.
- Cột **Bỏ** = số kết luận bị `neo()` gỡ ra. Bằng 0 ở mọi dòng nghĩa là model không bịa id lần nào.
- Dòng ghi `CHƯA ĐO — hết hạn mức` = lượt đó dừng giữa chừng vì free tier. Chạy lại cùng lệnh sẽ
  đo tiếp từ case còn thiếu (kết quả đã đo nằm trong `.cache-eval.json`, không phải gọi lại).

## Hạn mức free tier — đọc trước khi chạy

Google AI Studio free tier giới hạn **20 lời gọi/ngày cho mỗi model** (đo được 31/07 trên
`gemini-3.6-flash`), ngoài giới hạn theo phút. Golden set 22 case **không chạy hết được trong một
ngày trên một model**. Hai cách đi tiếp:

```powershell
python scripts/chay_eval.py --model gemini-3.1-flash-lite   # model có hạn mức rộng hơn
python scripts/chay_eval.py                                  # chạy lại: đo tiếp phần còn thiếu
```
