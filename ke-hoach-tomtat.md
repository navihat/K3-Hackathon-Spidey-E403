# Kế hoạch — Tóm tắt thảo luận nhóm, phân biệt đã chốt / đã bỏ / đang treo

**Trạng thái: CHỜ DUYỆT.** Chưa viết dòng code nào. Mục §12 liệt kê những chỗ cần bạn gật trước khi tôi bắt đầu.

## 1. Lát cắt một câu

> Một thành viên gõ `/tomtat` trong `#thao-luan-nhom` → AI đọc tin nhắn 24h gần nhất → trả về bản tóm tắt chia
> **ba khối đã chốt / đã bỏ / đang treo**, mỗi ý kèm link tới tin nhắn gốc — ý nào không đủ căn cứ thì **luôn**
> rơi về "đang treo" kèm lý do, không bao giờ tự nâng lên "đã chốt".

Điểm đặc biệt không nằm ở chỗ tóm tắt được — mọi LLM đều tóm tắt được. Nó nằm ở chỗ **"đã chốt" là một
tuyên bố cần bằng chứng**, và bằng chứng đó do code kiểm chứ không do model tự nhận.

## 2. Quyết định đã chốt với bạn

| # | Chốt gì |
|---|---|
| 1 | Đây là **tính năng thứ 2**, khai rõ là mở rộng. Lát cắt §4 của `spec.md` giữ nguyên cho phần chấm R2/R5 |
| 2 | Kích hoạt bằng **cả** `/tomtat` **lẫn** bản tự động 22:00 |
| 3 | Tự động chỉ chạy khi có **≥10 tin mới**, đăng ngay trong `#thao-luan-nhom` |
| 4 | Phạm vi mặc định **24h gần nhất, trần 200 tin** |
| 5 | Căn cứ phân loại: **lai** — LLM đề xuất, code neo `message_id`, cộng tín hiệu tường minh (reaction, từ khoá) |
| 6 | Không đủ căn cứ → **mặc định "đang treo"** kèm lý do |
| 7 | Trình bày **nhóm theo trạng thái**, ba khối |
| 8 | Đo bằng **golden set riêng**, nhãn do người gán |
| 9 | Bot chạy tay, tắt bật thất thường → cần cơ chế **đăng bù** |

## 3. Quan hệ với spec đang chấm

Tính năng này **vi phạm 2 điều** trong `spec.md` nếu không khai báo:

| Điều | Hiện tại | Xử lý |
|---|---|---|
| Non-goal 4 — không index ngoài 5 kênh | `#thao-luan-nhom` nằm ngoài `KENH_INDEX` | Ghi §9: mở rộng có chủ đích, chỉ cho tính năng tóm tắt. `KENH_INDEX` **không đổi** — tin thảo luận đọc trực tiếp từ Discord lúc tóm tắt, **không** nạp vào `index.db` |
| Non-goal 2 — không push chủ động | Bản 22:00 là bot tự đăng | Ghi §9: nới thành *"không nhắn riêng cho cá nhân; bản tin định kỳ trong kênh chung thì có"* |

Lát cắt §4, quality bar §7 và golden set 22 case **giữ nguyên tuyệt đối**. Tính năng này có bar riêng (§9 dưới).

## 4. Kiến trúc

Bám đúng cách chia lớp đang có: quyết định AI nằm trong module **không import discord**, để chạy eval ngoài Discord.

```
codebase/timlai/
├── tom_tat.py     ← MỚI · lớp ③ thứ hai: schema + tín hiệu + prompt + neo. KHÔNG import discord
├── render.py      ← thêm embed_tom_tat()
├── bot.py         ← thêm /tomtat, đọc history, scheduler 22:00, đăng bù
└── config.py      ← KENH_THAO_LUAN, GIO_TOM_TAT, NGUONG_TIN, TRAN_TIN

codebase/scripts/
├── seed_thao_luan.py    ← MỚI · sinh 4 cuộc thảo luận giả có gài bẫy
└── chay_eval_tomtat.py  ← MỚI · runner riêng, ghi eval/ket-qua-tomtat/

eval/
├── golden-set-tomtat.md    ← MỚI · bản người đọc + cách gán nhãn
└── golden-set-tomtat.yaml  ← MỚI · nhãn vàng do người gán

codebase/tests/test_tom_tat.py   ← MỚI
codebase/.da_tom_tat.json        ← MỚI · mốc đã đăng, chống đăng trùng (gitignore)
```

Luồng: `bot` đọc `channel.history(after=24h, limit=200)` → chuẩn hoá thành `TinThaoLuan` → `tom_tat.tom_tat()`
→ `render.embed_tom_tat()` → đăng. Tin thảo luận **không** đi vào `index.db`.

## 5. Hợp đồng dữ liệu

```python
class YKien(BaseModel):
    noi_dung: str              # tóm tắt ý, 1 câu
    trang_thai: Literal["chot", "bo", "treo"]
    id_neu: str                # message_id nơi ý được nêu ra          — BẮT BUỘC neo
    id_can_cu: list[str]       # message_id chứng minh trạng thái      — BẮT BUỘC khi chot/bo
    ly_do_treo: str | None     # vì sao chưa kết luận được

class BanTomTat(BaseModel):
    y_kien: list[YKien]
    khong_co_gi: bool          # kênh chỉ có chit-chat, không có ý kiến nào đáng ghi
```

## 6. Cơ chế phân loại — ba tầng

**Tầng 1 · Tín hiệu tường minh, code tự tính, không hỏi LLM**

| Tín hiệu | Nghĩa |
|---|---|
| Reaction ✅ ☑️ 👍 trên tin | phiếu thuận cho ý trong tin đó |
| Reaction ❌ 👎 | phiếu chống |
| Từ khoá: chốt, thống nhất, đồng ý, ok luôn, done | ứng viên "đã chốt" |
| Từ khoá: bỏ, thôi, không làm, dẹp, huỷ | ứng viên "đã bỏ" |
| Từ khoá: để sau, tạm gác, tính sau, chưa quyết | ứng viên "đang treo" |

**Tầng 2 · LLM đọc hội thoại** và xuất `list[YKien]`, mỗi ý phải chỉ ra tin nào nêu ý, tin nào là căn cứ.

**Tầng 3 · `neo_tom_tat()` — code kiểm, đây là chỗ quyết định**

1. `id_neu` không có trong danh sách tin đã nạp → **bỏ cả ý kiến**, đếm vào số đo bịa.
2. `id_can_cu` nào không có thật → gỡ khỏi danh sách, đếm vào số đo bịa.
3. `trang_thai` là `chot` hoặc `bo` mà **không còn căn cứ nào** → **hạ xuống `treo`**, `ly_do_treo` = *"model không chỉ được tin nhắn nào xác nhận"*.
4. **Luật người khác**: `chot` chỉ đứng vững khi có ≥1 căn cứ **do người KHÁC người nêu ý** viết, hoặc ≥1 reaction ✅ từ người khác. Tự chốt ý của chính mình → hạ xuống `treo`, lý do *"mới có người đề xuất nói, chưa ai khác xác nhận"*.
5. Một ý bị lật lại về sau → lấy trạng thái theo **căn cứ mới nhất** (cùng nguyên tắc "ưu tiên tin mới nhất" đang dùng ở `truy_xuat`).

Luật 3 và 4 là hiện thực hoá quyết định "mơ hồ thì mặc định treo". Cost-of-error: bot nói nhầm "đã chốt" thì
cả nhóm hành động theo một quyết định chưa từng có; xếp nhầm vào "treo" thì tệ nhất là ai đó phải xác nhận lại.

## 7. Bốn lớp chỗ khó

| Lớp | Tình huống | Hành vi mong muốn |
|---|---|---|
| ① Nguồn sự thật | Model bịa một quyết định chưa ai nói, hoặc gán "đã chốt" khi chưa ai xác nhận | Neo `id_neu` bắt buộc; luật người khác ở §6. **0 case là bar** |
| ② Mơ hồ | "ừ" / "ok" trả lời cái gì? Nói đùa? Mỉa mai? | Không suy diễn → `treo` + `ly_do_treo` nói rõ chỗ mơ hồ |
| ③ Ngoài phạm vi | User hỏi *"vậy nên chọn cái nào?"* | Từ chối: bot tóm tắt, **không ra quyết định thay nhóm** |
| ④ Đặc thù domain | Quyết định bị lật lại: *"thôi quay lại phương án A"* | Lấy trạng thái theo căn cứ mới nhất, nêu rõ *"đã đổi so với trước đó"* |

## 8. Định dạng đầu ra

```
📋 Tóm tắt #thao-luan-nhom · 24h qua · 47 tin · 5 người

✅ ĐÃ CHỐT (2)
• Dùng SQLite FTS5 thay vì vector DB
  ↪ Thái 14:03 · xác nhận: Nguyên 14:11, Trung ✅
• Deadline nộp spec: 23:59 hôm nay
  ↪ Nguyên 15:20 · xác nhận: Thái 15:22

❌ ĐÃ BỎ (1)
• Bot trả lời câu hỏi kiến thức
  ↪ Trung 14:40 · căn cứ: Thái 14:44 "thôi bỏ, ngoài phạm vi"

⏳ ĐANG TREO (3)
• Có nên index thêm #hoi-dap?
  ↪ Thái 16:02 — chưa ai phản hồi
• Đổi model sang flash-lite
  ↪ Nguyên 16:30 — mới người đề xuất nói, chưa ai khác xác nhận

Đã bỏ 1 kết luận không neo được vào tin nhắn thật.
```

Mỗi dòng `↪` là link tới tin gốc — người đọc tự kiểm được, đúng nguyên tắc G11 đang áp.

## 9. Kiểm thử

**Unit test** (`test_tom_tat.py`, không cần API key) — mỗi luật ở §6 một test:
tự chốt ý mình → treo · căn cứ bịa → gỡ và đếm · `id_neu` bịa → bỏ cả ý · quyết định bị lật → lấy cái mới ·
reaction ✅ từ chính người nêu → không tính · hội thoại chỉ chit-chat → `khong_co_gi=True`.

**Golden set riêng** — `seed_thao_luan.py` sinh **4 cuộc thảo luận giả** (data giả tự sinh, đúng ràng buộc 3),
mỗi cuộc 20-40 tin, cố tình gài:

| Cuộc | Gài bẫy gì |
|---|---|
| 1 | Chốt sạch sẽ, có reaction ✅ — happy path |
| 2 | Có người tự chốt ý mình, không ai phản hồi → phải ra `treo` |
| 3 | Quyết định bị lật lại ở cuối → phải lấy trạng thái mới |
| 4 | Toàn chit-chat lạc đề + một câu đùa nghe như chốt → phải ra `khong_co_gi` hoặc `treo` |

Người gán nhãn vàng vào `golden-set-tomtat.yaml` (~25-35 ý kiến có nhãn), rồi `chay_eval_tomtat.py` đo độ khớp.

**Quality bar đề xuất — cần bạn duyệt:**

> Đạt khi **≥80%** ý kiến được xếp đúng trạng thái so với nhãn người gán, **0 case gán nhầm thành "đã chốt"**,
> và **0 ý kiến bịa** (không neo được vào `message_id` có thật). Thời gian phản hồi **<15 giây** cho 200 tin.

Bar này thấp hơn 85% của tính năng tìm link vì phân loại trạng thái khó hơn nhiều so với tìm link, nhưng
**hai chỉ số an toàn thì vẫn là 0** — đó mới là chỗ không được nhân nhượng.

## 10. Scheduler và đăng bù

Bot chạy tay nên không thể tin vào việc nó sống lúc 22:00:

- `discord.ext.tasks` chạy vòng lặp mỗi 30 phút.
- Mỗi lần tỉnh: đọc `.da_tom_tat.json` → nếu **hôm nay chưa đăng** và **đã qua 22:00** và **có ≥10 tin mới** → đăng rồi ghi mốc.
- Bot bật lúc 23:30 vẫn đăng bù cho hôm đó. Bật lúc 08:00 hôm sau thì **không** đăng bù cho hôm qua (bản tin đã hết hạn dùng).
- `.da_tom_tat.json` vào `.gitignore`.

## 11. Hạn mức và chi phí

| Việc | Lời gọi |
|---|---|
| Một lệnh `/tomtat` | 1 |
| Bản tự động | 1/ngày |
| Một lượt đo trọn golden set | 4 (mỗi cuộc thảo luận 1) |

Rẻ hơn hẳn golden set 22 case của tính năng tìm link. Vẫn dùng chung hạn mức **20 lời gọi/ngày/model**, nên
tôi sẽ cho `chay_eval_tomtat.py` dùng lại cơ chế cache chạy-tiếp đã có.

## 12. Cần bạn duyệt trước khi tôi bắt đầu

1. **Quality bar ở §9** — ≥80% / 0 nhầm-chốt / 0 bịa / <15s. Con số 80% có hợp lý không?
2. **Luật người khác** (§6 luật 4) — tự chốt ý mình thì hạ xuống treo. Đây là luật gắt nhất, và cũng là thứ làm tính năng này khác một bản tóm tắt thường. Bạn đồng ý không?
3. **Dùng reaction làm tín hiệu** — cần bot đọc được reaction trên tin cũ. Không cần bật intent mới, nhưng nếu nhóm bạn không có thói quen thả ✅ thì tín hiệu này gần như vô dụng, và tôi sẽ dựa hẳn vào từ khoá + reply.
4. **Nới 2 non-goal** ở §3 và ghi vào `spec.md` §9.

## 13. Rủi ro tôi thấy trước, ghi ra để bạn cân

| Rủi ro | Mức | Ghi chú |
|---|---|---|
| `noi_dung` của mỗi ý là chữ do model sinh, code **không kiểm được** — model tóm tắt sai ý một câu nói | cao | Cùng loại rủi ro với `nhan` của link đã ghi ở `spec.md` §9. Giảm bằng cách luôn kèm link tin gốc, không loại bỏ được |
| Mỉa mai, nói đùa, tiếng lóng | trung bình | Cuộc thảo luận số 4 trong golden set để đo đúng chỗ này |
| Thread và reply lồng nhau | trung bình | **Không xử trong phiên bản này** — chỉ đọc tin ở kênh chính. Ghi làm non-goal |
| Tóm tắt hội thoại của người thật rồi đăng công khai | thấp | Đăng đúng trong kênh mà những người đó đang nói, không gửi ra ngoài |
| Free tier có thể dùng dữ liệu để huấn luyện | cần cân nhắc | Nội dung thảo luận nhóm sẽ được gửi lên Gemini. Nếu có gì nhạy cảm thì đừng bật tính năng này ở kênh đó |

## 14. Thứ tự thực thi sau khi duyệt

1. `config.py` + `.env.example`: `KENH_THAO_LUAN`, `GIO_TOM_TAT`, `NGUONG_TIN`, `TRAN_TIN`
2. `tom_tat.py`: schema → tín hiệu tường minh → `SYSTEM` → `neo_tom_tat()`
3. `test_tom_tat.py`: 6 test cho 6 luật, chạy offline
4. `render.embed_tom_tat()` + test định dạng
5. `bot.py`: `/tomtat`, đọc history, `AllowedMentions.none()`, bắt lỗi hết hạn mức
6. `seed_thao_luan.py`: 4 cuộc thảo luận có gài bẫy
7. `golden-set-tomtat.yaml`: gán nhãn vàng (**chỗ này cần bạn hoặc một người trong nhóm gán**, tôi gán thì nhãn và bài thi cùng một tác giả)
8. `chay_eval_tomtat.py` + chạy lượt đo đầu → `eval/ket-qua-tomtat/luot-1.md`
9. Scheduler + đăng bù
10. Ghi `spec.md` §9: nới 2 non-goal, khai tính năng mở rộng, bar riêng, kết quả đo

Bước 7 là chỗ duy nhất tôi không tự làm trọn được — nhãn vàng phải do người ngoài phần code gán, nếu không
thì con số đo được chỉ chứng minh tôi nhất quán với chính mình.
