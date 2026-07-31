# AI SPEC — Trợ lý tìm thông tin Discord · Nhóm [Spidey] · Zone X
Hướng: [ ] A — VLearn  [X] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [X] Tính năng mới

## §1. User & Job
- **Job executor**: Học viên đang theo học khoá AI Thực Chiến, sử dụng Discord làm kênh giao tiếp chính.

- **Workflow hiện tại**: Khi cần xem lại link slide/tài liệu/deadline → nhớ mơ hồ nó ở kênh nào → scroll/chuyển qua 2-3 kênh → không thấy → hỏi bạn/LabCoach/tag trong channel chung → chờ reply hoặc bỏ cuộc.

- **Core JTBD** (không tên sản phẩm/AI): *"Khi cần xem lại tài liệu, deadline hoặc câu trả lời LabCoach đã gửi trong Discord, tôi muốn tìm được ngay mà không phải scroll nhiều kênh, để không mất thời gian và không bỏ lỡ thông tin quan trọng."*

- **Problem statement** (KHÔNG chữ AI):
  > Học viên cần tìm lại thông tin (slide, deadline, link, câu trả lời LabCoach) đã được gửi trong Discord khoá. Họ chỉ nhớ mơ hồ thông tin đó nằm ở kênh nào, phải check 2-3 kênh, mất 1-15 phút mỗi lần. 77% cảm thấy khó chịu, 23% bỏ cuộc hoặc lỡ deadline vì không tìm được.

- **Evidence** (chuẩn A — khảo sát 36 người ngoài nhóm, log đầy đủ tại [`data/khao-sat-log.csv`](data/khao-sat-log.csv) + [`data/khao-sat-log.md`](data/khao-sat-log.md)):
  - **31/36 (86%)** từng không tìm được thông tin trong Discord 7 ngày qua
  - **26/31 (84%)** cần tìm **slide/tài liệu buổi học**
  - **18/31 (58%)** cần **check deadline/lịch nộp bài**
  - **16/31 (52%)** cần **link VLearn/Phoenix/aithucchien/codelabs**
  - **7/31 (23%)** cần **link/QR checkin**
  - **26/31 (84%)** *chỉ nhớ mơ hồ → phải check 2-3 kênh*
  - **15/31 (48%)** mất **5-15 phút** để tìm; **13/31 (42%)** mất **1-5 phút**
  - **24/31 (77%)** cảm thấy khó chịu (17 "hơi bực" + 7 "khá khó chịu")
  - Hành động khi không tìm được: 68% hỏi riêng bạn, 45% tag mọi người trong channel chung, 35% hỏi Lab Coach, 23% bỏ qua dùng tài liệu khác, 16% không tìm nữa — lỡ luôn
  - **29/31 (94%)** sẽ dùng bot trả lời câu hỏi tự nhiên (12 "chắc chắn dùng", 17 "có thể dùng")

## §2. Impact & quyết định chọn

### Bảng impact ≥3 ứng viên

| Ứng viên | Số người gặp | Tần suất | Tốn gì mỗi lần | Build nổi? | Chọn? |
|---|---|---|---|---|---|
| **A. Tìm slide/tài liệu buổi học** | 26/31 (84%) | ~1-2 lần/tuần (mỗi buổi học) | 1-15 phút | Có | **Chọn** |
| **B. Check deadline/lịch nộp bài** | 18/31 (58%) | ~1 lần/tuần | 1-15 phút | Có | Loại |
| **C. Xem lại câu trả lời TA cho bạn khác** | 21/31 (68% muốn dùng bot) | ~1-2 lần/tháng | 5-15 phút | Có | Loại |
| **D. Tìm link VLearn/Phoenix/codelabs** | 16/31 (52%) | ~1-2 lần/tuần | 1-15 phút | Có | Loại |

### Ứng viên ĐÃ LOẠI + vì sao
- **B (Check deadline)**: Tần suất thấp hơn (~1/tuần so với 1-2/tuần) và evidence yếu hơn (58% vs 84%). Deadline thường xuất hiện trong tin nhắn thông báo/slide/hình ảnh nên thông tin cần index vượt ngoài phạm vi hackathon 1.5 ngày.
- **C (Xem lại câu trả lời TA)**: Tần suất thấp (~1-2/tháng). Khó xác định nguồn sự thật vì câu trả lời Lab Coach không có cấu trúc chuẩn.
- **D (Tìm link VLearn)**: 52% gặp, thường đi cùng với nhu cầu tìm slide (combo). Có thể gom vào ứng viên A sau này.

### Ứng viên CHỌN + vì sao (bằng số)
**Chọn A — Tìm slide/tài liệu buổi học.**
- Evidence mạnh nhất: **84%** (26/31) học viên gặp — vượt xa các ứng viên khác.
- Tần suất cao nhất: ~1-2 lần/tuần, gắn với mỗi buổi học.
- Mức độ khó chịu cao: **77%** khó chịu, trong khi deadline/link thường ít gây bực hơn.
- Hệ luỵ: 23% bỏ cuộc → bỏ lỡ nội dung buổi học.
- Build nổi: prototype có thể dùng RAG đơn giản: index tin nhắn Discord → user hỏi tự nhiên → trả lời kèm link gốc.

## §3. Giải pháp tương tự đã nghiên cứu

- **ChatGPT (chia sẻ link chat)**: Flow: user nhắn "link slide buổi 5" → ChatGPT reply. Đáng học: trả lời tự nhiên. Đáng né: không có nguồn chính thức, dễ bịa link. Mình khác: chỉ trả lời từ tin nhắn Discord thật + kèm link trỏ đến tin nhắn gốc.
- **Discord Search (built-in)**: Flow: Ctrl+K → gõ từ khoá → xem kết quả. Đáng học: ai cũng có sẵn. Đáng né: search yếu, không hiểu ngữ nghĩa ("link slide buổi 5" vs "slide b5"), dễ miss. Mình khác: hiểu câu hỏi tự nhiên, trả lời chính xác.
- **Notion AI Q&A**: Flow: hỏi tự nhiên → AI tìm trong workspace → trả lời kèm source. Đáng học: cite nguồn rõ ràng. Đáng né: license phí, không phải ai trong lớp cũng có. Mình khác: chạy ngay trong Discord, free, dùng data thật từ chính server.

## §4. Thiết kế

- **Lát cắt MỘT CÂU**:
  > *Một học viên gõ câu hỏi tự nhiên (VD: "link slide hackathon", "link lý thuyết buổi 3", "link lab 2") trong Discord → AI tìm trong tin nhắn 5 kênh chỉ định → trả về chính xác link tài liệu kèm tên người gửi và link trỏ đến tin nhắn gốc — nếu không có thì trả lời "Mình không tìm thấy link này."*

- **Phạm vi dữ liệu index** (chỉ 5 kênh):
  1. Kênh #Build/Thông báo #Build (Link zoom, Link ngân hàng đề)
  2. Kênh Build/Tài nguyên (Link Hướng dẫn onboarding, GitHub Org, Link Tài liệu Workshop)
  3. Kênh Lớp học Khoá 3/Thông báo chung (Link codelabs, Link slide hackathon, Link repo, Link Checkpoint)
  4. Kênh lý thuyết — Lớp học Khoá 3 (Link tài liệu tham khảo)
  5. Kênh thực hành lab — Lớp học Khoá 3 (Link repo, Link chấm điểm, Link checkpoint)

- **Non-goals** (≥3 thứ KHÔNG build):
  1. Không trả lời câu hỏi kiến thức chuyên môn (học thuật) — chỉ trả link tài liệu.
  2. Không tự động gửi tin nhắn chủ động (push) — chỉ phản hồi khi được hỏi.
  3. Không hỗ trợ tiếng Anh hoặc ngôn ngữ khác ngoài tiếng Việt.
  4. Không index ngoài 5 kênh đã định (kênh chat chung, kênh hỏi bài, v.v.).

- **Mức prototype nhắm tới**: [ ] Sketch [] Mock [X] Working
  - AI thật ở lõi (RAG trên data Discord mẫu từ 5 kênh)
  - Giao diện chat trên discord trong server thật

- **Automation**: [ ] augment [X] conditional [ ] automate
  - **Lý do theo cost-of-error**: Sai link tài liệu gây hậu quả trực tiếp — học viên vào sai tài liệu, học sai nội dung, bỏ lỡ bài lab. Do đó: AI **chỉ trả link khi có căn cứ rõ ràng** trong tin nhắn (≥1 match khớp). Khi không tìm thấy → "Mình không tìm thấy link này trong các kênh." — tuyệt đối không bịa link.

- **§4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR)**:

  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | **G10 — Thu hẹp phạm vi khi nghi ngờ** | Không tìm thấy match → không đoán. Trả lời: "Mình không tìm thấy link này trong các kênh. Bạn thử gõ lại với từ khoá khác nhé." |
  | **G2 — Làm rõ nó làm tốt đến đâu** | Hỏi bot về chính nó ("bạn giúp được gì", `/gioithieu`, @mention trống) → `tra_cuu.GIOI_THIEU`: nói cả **làm được gì** lẫn **không làm gì** (không giải thích kiến thức, không tìm ngoài 5 kênh, không đoán link), kèm 3 cách hỏi và 4 câu hỏi mẫu. Footer hiện số tin đang theo dõi + tên model. Nhận diện ở `tra_cuu.la_hoi_ve_bot()`, không tốn lời gọi AI |
  | **G11 — Giải thích vì sao** | Mỗi câu trả lời kèm link dẫn đến tin nhắn gốc + tên người gửi — user tự kiểm tra được. |
  | **G9 — Sửa dễ dàng** | Reply thẳng vào tin của bot rồi gõ câu khác — `Bot.cau_hoi_cho_bot()` nhận đó là câu hỏi mới. Không phải gõ lại lệnh, không reset flow. |
  | **G8 — Gạt bỏ dễ dàng** | Nếu bot trả lời sai link, user ignore và tự scroll kênh — không block flow. |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)

| # | Tình huống | Lớp | Hành vi mong muốn | Nguyên tắc |
|---|---|---|---|---|
| 1 | User hỏi "link slide buổi 5" — có 2 link khác nhau từ 2 kênh (lý thuyết + tài nguyên) | ② Mơ hồ | Trả về cả 2 kèm tên kênh + link gốc, để user tự chọn | G11 |
| 2 | User hỏi "link slide buổi 10" — chưa có buổi 10 trong các kênh | ① Không căn cứ | "Mình không tìm thấy link slide buổi 10 trong các kênh. Có thể bạn nhầm buổi hoặc slide chưa được đăng." | G10 |
| 3 | User hỏi "giải thích hàm softmax giúp mình" (câu hỏi kiến thức) | ③ Ngoài phạm vi | "Mình chỉ tìm link tài liệu từ các kênh thôi. Bạn hỏi bài trong kênh hỏi-đáp hoặc tag Lab Coach nhé." | G2 |
| 4 | User hỏi "link lab 2" — link đã hết hạn (hết thời gian làm lab) | ④ Đặc thù domain | Trả link kèm lưu ý: "Link lab 2 đã hết hạn (dd/mm). Nếu cần gia hạn bạn liên hệ Lab Coach." | G11 |
| 5 | User hỏi "link slide" — quá chung chung, không rõ buổi nào | ② Mơ hồ | "Mình tìm thấy N link slide trong các kênh. Bạn nói rõ buổi mấy để mình tìm chính xác?" | G10 |
| 6 | User gõ sai chính tả: "slie buoi 5" | ② Mơ hồ | Dùng fuzzy match, tìm đúng "slide buổi 5" → trả link | G11 |
| 7 | User hỏi "link checkin" — QR checkin không nằm trong 5 kênh được index | ① Không căn cứ | "Mình không tìm thấy link này trong phạm vi các kênh mình quản lý." | G10 |
| 8 | User hỏi "link VLearn" — có link VLearn trong kênh thông báo | — | Trả link VLearn kèm tên người gửi + link gốc | G11 |
| 9 | User hỏi "link bài 3 của Tuấn" — có link nhưng không rõ "bài 3" là bài nào | ② Mơ hồ | "Mình tìm thấy 1 link có từ 'bài 3' trong kênh lab: [link]. Đây có phải bạn cần không?" | G10 |
| 10 | User hỏi "link slide hôm qua" — "hôm qua" là khái niệm tương đối | ② Mơ hồ | Cần mapping "hôm qua" → ngày cụ thể dựa trên thời điểm hỏi, rồi tìm link. Nếu không xác định được: "Bạn nói rõ buổi mấy hoặc ngày tháng nhé." | G10 |
| 11 | User chào bot / hỏi "bạn giúp mình được những gì" — không hỏi tài liệu nào | — (về chính bot) | Trả phần giới thiệu: làm được gì, KHÔNG làm gì, 3 cách hỏi, 4 câu hỏi mẫu. Không được trả "Mình không tìm thấy" | G2 |
| 12 | User hỏi "link hướng dẫn onboarding" — có chữ "hướng dẫn" như câu hỏi về bot | — | Vẫn phải đi đường tra cứu tài liệu. `la_hoi_ve_bot()` bỏ qua mọi câu có từ chỉ tài liệu (`link`, `slide`, `buổi N`, `onboarding`…) trước khi xét các mẫu còn lại | G10 |

## §6. Bốn đường đi của trải nghiệm

- **Happy path**: User: "link slide buổi 5" → Bot: "Link slide buổi 5 do LabCoach [Tên] gửi trong kênh 📘lý-thuyết-k3: [link]. [Link gốc]"
- **Low-confidence (②)**: User: "slide buổi 5" → Bot tìm thấy 2 link → "Mình thấy 2 link liên quan: [link 1] trong 📘lý-thuyết-k3 · [link 2] trong 🛠tài-nguyên. Bạn xem cái nào đúng? [Link gốc 1] [Link gốc 2]"
- **Failure/không căn cứ (①)**: User: "link slide buổi 10" → Bot: "Mình không tìm thấy link slide buổi 10 trong các kênh. Bạn thử gõ 'link slide buổi 9' nhé?"
- **Correction (user sửa)**: User: "link lab 2" → Bot: "Link lab 2 trong 🧪lab-k3: [link]" → User: "ý mình bài 2 của build" → Bot: "Link bài 2 trong 🛠tài-nguyên: [link]"
- **Khi bị đòi ngoài phạm vi (③)**: User: "giải thích hàm softmax" → Bot: "Mình chỉ tìm link tài liệu từ 5 kênh thôi (thông báo, tài nguyên, thông báo chung, lý thuyết, lab). Bạn hỏi bài trong kênh hỏi-đáp hoặc hỏi AI Tutor trên VLearn nhé."
- **Case đặc thù domain (④)**: User: "link lab 2" → Bot tìm link kèm: "Link lab 2 trong 🧪lab-k3: [link]. Lưu ý: deadline lab 2 đã qua (20/07). Liên hệ Lab Coach nếu cần gia hạn."

## §7. Kiểm thử

- **Chiều chất lượng + định nghĩa kiểm chứng được**:
  | Chiều | Định nghĩa | Pass/Fail |
  |---|---|---|
  | Đúng link | Link trong câu trả lời khớp với tin nhắn gốc trong data | Pass |
  | Đúng nội dung | Nội dung tóm tắt đúng với tin nhắn gốc | Pass |
  | Có căn cứ | Mỗi câu trả lời đều kèm link trỏ đến tin nhắn gốc | Pass |
  | An toàn (không bịa) | Khi không có data → từ chối rõ ràng, không đoán | Pass |
  | Thời gian phản hồi | < 5 giây | Pass |

- **Golden set** — 22 case, bản người đọc tại [`eval/golden-set.md`](eval/golden-set.md), bản máy chạy tại
  [`eval/golden-set.yaml`](eval/golden-set.yaml):

  | Nhóm case | Số lượng | Bắt nguồn từ đâu |
  |---|---|---|
  | Thường (TH-01…TH-10) | 10 | Bốn loại thông tin học viên khai trong khảo sát: slide/tài liệu (84%), link VLearn/codelabs (52%), lab, thông báo chung |
  | ① Không căn cứ (TH-11, TH-12) | 2 | Hai thứ **cố tình không** có trong index: slide buổi 10 và QR checkin (7/31 người từng tìm QR checkin — nằm ngoài 5 kênh) |
  | ② Mơ hồ (TH-13, TH-14) | 2 | 84% "chỉ nhớ mơ hồ" + thói quen gõ không dấu/sai chính tả |
  | ③ Ngoài phạm vi (TH-15, TH-16) | 2 | Câu hỏi kiến thức — thứ non-goal 1 nói rõ là không làm |
  | ④ Đặc thù domain (TH-17, TH-18) | 2 | Link lab đã quá hạn · slide có 2 phiên bản ở 2 thời điểm |
  | Hiếm (TH-19…TH-22) | 4 | Lọc theo người gửi · câu dài lịch sự · thời gian tương đối · input cụt |

- **Quality bar** (chốt từ 23:59, giữ nguyên sau đó):
  > "Đạt khi **≥85%** qua bộ golden set, và **0 case bịa nguồn** (lớp ①)."

  Bar này **không đổi** kể cả khi đo ra thấp hơn, và không đổi khi đổi model. Kết quả từng lượt
  chạy — đủ mọi case, kể cả case chưa đạt — nằm ở [`eval/ket-qua/`](eval/ket-qua/).

## §8. Phân công & kế hoạch

- **Phân công có tên**:
  - Spec + evidence: Trương Thảo Nguyên
  - Prompt + golden set: Đinh Quốc Trung
  - Code prototype: Trương Văn Thái
  - Demo: Trương Văn Thái

- **Willing users** (≥3 tên) — ⚠️ **chưa điền tên thật, phải chốt trước khi chạy vòng validation**:
  1. _(tên · lớp/zone)_
  2. _(tên · lớp/zone)_
  3. _(tên · lớp/zone)_

  *Kế hoạch validation CP5*: giao task thật, im lặng quan sát, hỏi đúng 3 câu (① Điều gì khó hiểu hoặc khó chịu nhất? ② Kết quả này bạn có tin không — vì sao? ③ Bạn có dùng thật không — vì sao/vì sao chưa?), log nguyên văn.
  Giao thức đầy đủ + 3 task xếp theo độ khó: [`validation/README.md`](validation/README.md). Log: [`validation/feedback-log.md`](validation/feedback-log.md).

- **Multi-prototype** (nếu làm): không làm — dồn thời gian vào một prototype mức Working.

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 30/07 | Tạo spec lần đầu | — |
| 30/07 | Mức prototype: Mock → **Working** | Đã dựng được server Discord test thật, bot chạy end-to-end trong Discord chứ không chỉ trong terminal |
| 30/07 | Danh sách 5 kênh §4 viết lại theo đúng tên kênh trên server | Tên trong spec phải khớp `KENH_INDEX`: `backfill.py` lọc theo tên kênh, lệch một dấu là kênh bị bỏ qua |
| 30/07 | Kênh `build` → `tai-nguyen` ở §4b, §5, §6 | Đồng bộ với tên kênh thật + `seed_gia.py` + `ghi_chu` TH-06 — tránh spec ghi một tên mà demo hiện tên khác |
| 30/07 | Model lõi: Claude → **Gemini 3.5 Flash** | Chỉ có API key Gemini free tier. Chọn 3.5-flash sau khi đo tay: 3.6-flash mất 4.6s (sát mốc <5s ở §7), 2.5-flash bị Google ngừng cấp cho key mới. Quality bar §7 **không đổi** — vẫn ≥85% và 0 case bịa nguồn |
| 31/07 | **Lượt đo thật đầu tiên**: 18/22 = **81.8%** pass, **0 case bịa nguồn** → [`eval/ket-qua/luot-2.md`](eval/ket-qua/luot-2.md) | Trước đó mới chỉ có lượt LLM giả. Chưa đạt bar pass (thiếu đúng 1 case), đạt bar bịa nguồn. Ghi nguyên trạng theo rubric R4: kết quả thấp vẫn tính điểm nếu trung thực |
| 31/07 | Model đo: 3.5-flash → **`gemini-3.1-flash-lite`** | 3.5-flash trả 503 liên tục (backoff tới 104s vẫn 503); 3.6-flash chạy được 20 case rồi ăn 429 vì free tier chỉ cho **20 lời gọi/ngày/model** mà golden set có 22 case. flash-lite chạy hết trọn bộ, 1,1s/lời gọi — vẫn dưới mốc <5s. **Bar §7 không đổi** |
| 31/07 | `_goi_gemini` thử lại cả **500/503**, không chỉ 429; `SO_LAN_THU` 3 → 5 | Một cú 503 giết cả lượt eval 22 case ở case đầu tiên |
| 31/07 | `chay_eval.py` **chạy tiếp được**: cache từng case + vẫn ghi bảng khi dừng giữa chừng | Hạn 20 lời gọi/ngày/model làm mất trắng 20 lời gọi đã tốn. Giờ hết hạn mức thì bảng vẫn ra, chạy lại chỉ đo phần còn thiếu |
| 31/07 | Thêm `README.md` (thành viên + phân công), `validation/`, `reflection/`, `demo-slides` | R6, R7 và checklist nộp cuối `02-guide.md` §5.2 đang trống |
| 31/07 | §8: bỏ dòng "nhóm 1 người" (mâu thuẫn với 3 tên phân công); willing users đánh dấu rõ **chưa điền** | Không khai "đã xác nhận" khi chưa có tên thật |
| 31/07 | §7: golden set ghi rõ từng nhóm case truy về bằng chứng nào | Rubric R4 đòi case có gốc từ dữ liệu thật — 16/22 case truy được về khảo sát hoặc nội dung quan sát trong kênh |
| 31/07 | Câu trả lời của bot: riêng tư (`ephemeral`) → **công khai** | Một người hỏi thì cả kênh cùng thấy, đỡ 3 người hỏi lại cùng một link — đúng pain "45% tag cả channel chung để hỏi" ở §1. Đánh đổi đã nhận: bot sai thì sai công khai, nên footer "đã bỏ N kết luận không neo được" cũng để công khai luôn |
| 31/07 | Thêm 2 đường vào: **@mention bot** và **reply vào tin của bot** | Học viên không phải nhớ tên lệnh; reply chính là đường *correction* §6 vốn mới chỉ có trên giấy. Cả ba đường dùng chung `bot.hoi()` nên hành vi không lệch nhau |
| 31/07 | Thêm `KENH_TU_DONG` (opt-in, **mặc định tắt**): mọi tin trong kênh đó là câu hỏi | Non-goal 2 "không push chủ động" **vẫn giữ** — bot chỉ phản hồi tin của người, không tự nhắn trước. Mặc định tắt vì bật ở 5 kênh thông báo sẽ khiến bot trả lời cả thông báo của LabCoach và đốt hết 20 lời gọi/ngày |
| 31/07 | Lời gọi AI chạy trong `asyncio.to_thread` | Trước đó `tra_cuu()` chặn event loop 1-4s: một người hỏi là cả bot đứng hình với mọi người khác. Với 3 đường vào thì chuyện này xảy ra thường xuyên hơn |
| 31/07 | `backfill.py` thêm cờ `--sach` (xoá `index.db` rồi dựng lại) | Backfill mặc định **không xoá** tin cũ — `them()` chỉ `DELETE` dòng trùng `id`, mà id tin giả (`1000000000000001`) không bao giờ trùng id thật (snowflake). Đo lúc 05:0x: index đang có **20 tin giả + 36 tin thật lẫn nhau**, bot có thể trả link chết `channels/111/222/…` giữa lúc demo |
| 31/07 | ⚠️ Ghi nhận: lượt eval `luot-2.md` đo trên index **chỉ có 20 tin giả** | Index hiện tại đã khác (56 tin). Muốn tái lập số 81.8%: `Remove-Item index.db; python scripts/seed_gia.py` rồi chạy lại. Không sửa số đã ghi |
| 31/07 | **Sửa lỗi**: `sqlite3.ProgrammingError` ở mọi câu hỏi trong Discord | Việc bọc cả `hoi()` vào `asyncio.to_thread` (thêm cùng ngày) làm connection SQLite tạo ở main thread bị dùng ở worker thread — sqlite3 cấm. Sửa: truy xuất FTS5 chạy trên event loop (query local, micro giây), **chỉ** lời gọi Gemini đẩy sang thread khác. Thêm test hồi quy `test_hoi_khong_dung_sqlite_o_thread_khac` — 24 test pass |

### 31/07 · Bảy guardrail — đặt ở tầng code, test được offline

Trước đó chỉ có **một** hàng rào thật (`neo()` lọc `message_id`) và phần còn lại trông cậy vào prompt.
Bảy guardrail dưới đây đều nằm trong code, mỗi cái có test riêng (`codebase/tests/test_guardrail.py`);
tổng **35 test pass**, không cần API key.

| # | Chỗ hở | Guardrail | Nằm ở đâu |
|---|---|---|---|
| **G1** | Bot chỉ đưa jump_url tới tin gốc, học viên vẫn phải tự mở tin ra tìm link | Bóc URL thật từ `noi_dung` trong index (`TinNhan.cac_link`) rồi hiện link cụ thể **trước**, tin gốc + ngày gửi sau. Link luôn đến từ DB, không bao giờ từ chữ model viết | `index.py`, `render.py` |
| **G2** | `neo()` chỉ kiểm `message_id`; model neo đúng id rồi vẫn gõ thêm URL bịa vào giữa câu — và đó mới là link học viên copy đi | `neo()` quét cả `cau_tra_loi`, gỡ mọi URL không có trong tin ứng viên, **đếm vào số đo bịa** thay vì nuốt. So khớp chính xác, lệch một ký tự cũng gỡ (fail closed theo cost-of-error §4) | `tra_cuu.py` |
| **G3** | Embed tiêu đề "Không tìm thấy"/"Ngoài phạm vi" vẫn liệt kê link bên dưới — tự mâu thuẫn, đọc lướt là bấm nhầm | Từ chối thì không trích nguồn. Ngoại lệ: đang hỏi lại (`can_lam_ro`) thì danh sách link chính là các lựa chọn | `render.py` |
| **G4** | Tin được chọn nhưng không chứa link nào, vẫn hiện như thể có link | Nói thẳng "tin này không chứa link nào — mở tin gốc để xem" | `render.py` |
| **G5** | Tin nhắn trong kênh do người khác viết, có thể chèn câu ra lệnh cho model | Rào `<<<TIN_NHAN>>>` + luật 7 trong `SYSTEM`. Đây là hàng rào **yếu** (prompt-level) — thứ chặn thật vẫn là G2 và `neo()` | `tra_cuu.py` |
| **G6** | Nội dung index chứa `@everyone`; bot echo lại là ping cả server | `AllowedMentions.none()` ở cả hai đường gửi | `bot.py` |
| **G7** | Hết hạn mức 20 lời gọi/ngày → exception, bot im lặng, học viên tưởng bot hỏng | Bắt lỗi, trả embed nói rõ đang không gọi được AI; chỉ tên lỗi + 150 ký tự, không đổ traceback ra kênh chung | `render.py`, `bot.py` |

Luật 6 của `SYSTEM` đổi theo G2: cấm model tự viết URL vào `cau_tra_loi`, vì phần link đã do hệ thống
tự bóc từ tin gốc và render riêng.

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 31/07 | `config.MODEL`: `gemini-3.6-flash` → **`gemini-3.1-flash-lite`** | Lượt đo `luot-2.md` chạy trên flash-lite (qua cờ `--model`) nhưng bot trong Discord vẫn dùng 3.6-flash — con số đo được không nói gì về bot đang chạy. Mà 3.6-flash cũng đã cạn 20 lời gọi/ngày ngay trong chính lượt đo đó: hỏi thật một câu là ăn 429 |
| 31/07 | Kết quả kiểm tay sau khi thêm guardrail (`thu_hoi.py "link slide buổi 5"`) | Trả về đúng dạng mong muốn: `🔗 <link thật từ DB>` + `↪ #kênh · người gửi · ngày` + cảnh báo tin cũ, `bỏ (bịa) = 0`. Model không tự gõ URL nào vào văn bản |

### 31/07 · G8 — một tin nhiều link thì chỉ trả đúng link được hỏi

**Lỗi phát hiện khi dùng thật.** Tin nhắn trong `#ly-thuyet-k3` liệt kê 5 link nộp bài (CP1…CP5) trong
cùng một tin. User hỏi CP5: model nói đúng *"đây là link nộp Checkpoint 5"*, nhưng phần link lại đổ ra
**3 link đầu tiên** của tin rồi cắt — mất đúng link CP5 mà user cần. Bot vừa vô dụng vừa gây hiểu nhầm.

Nguyên nhân: model chọn link ở tầng **văn bản**, còn code chỉ biết "tin này có những link nào". Lựa chọn
đó không có đường nào đi xuống tầng render.

| Đổi gì | Vì sao |
|---|---|
| `KetQua` thêm trường `link_chon: list[str]` — model copy nguyên văn (những) link user cần | Model được quyền **chọn** link, không được quyền **tạo** link. Giữ đúng nguyên tắc G2 |
| `neo()` thêm bước `_loc_link_chon()`: chỉ giữ link có thật trong tin **đã neo**, link lệch bị gỡ và **đếm vào số đo bịa** | Link có thật nhưng thuộc tin khác cũng bị gỡ — neo phải chặt tới mức từng tin, không chỉ tới mức "có trong index" |
| `SYSTEM` thêm luật 6b, nêu thẳng ví dụ CP1…CP5 | Nói "chọn đúng link" chung chung thì model vẫn trả cả cụm |
| `render._dong_nguon()` nhận `da_chon`: có link đã chọn thì **chỉ hiện link đó**, kèm dòng *"tin gốc còn N link khác"* | Vẫn cho user biết tin gốc còn gì, phòng khi bot chọn nhầm |
| Field embed đổi tên `🔗 Tin nhắn gốc` → `🔗 Link` | Tên cũ sai từ khi G1 đưa link thật vào field này |

**Lỗ thứ hai lộ ra khi kiểm** (tầng ② retrieval, không phải render): thông báo viết `CP5`, học viên gõ
`checkpoint 5`. `unicode61` tách `CP5` thành **một** token nên nó không khớp cả `checkpoint` lẫn `5` —
tin chứa link không hề lọt vào danh sách ứng viên và bot trả "không tìm thấy" dù link nằm sẵn trong index.
Sửa: `_mo_rong()` trong `index.py` sinh thêm biến thể (`cp5` → `cp`, `5`; `checkpoint 5` → `cp5`), bảng
`_VIET_TAT` chỉ gồm vài từ hay gặp trong khoá chứ không phải từ điển đồng nghĩa tổng quát.

Kiểm tay sau khi sửa — `thu_hoi.py "link nộp checkpoint 5"`:

```
Link nộp Checkpoint 5 đã được cung cấp trong thông báo về các mốc checkpoint.
🔗 https://forms.gle/xoroSTFV9WtPG1CfA
_(tin gốc còn 4 link khác)_
↪ [#ly-thuyet-k3 · Văn Thái · 30/07](…/1532511876934668379)
bỏ (bịa) = 0
```

**44 test pass** (thêm 6 test cho G8 dựng đúng trên tin CP1…CP5 thật, 3 test cho phần bắc cầu viết tắt).

⚠️ `luot-2.md` (81.8%) đo **trước** những thay đổi này. Lượt đo tiếp theo sẽ khác — cần chạy lại trọn bộ
để biết G8 và `_mo_rong()` ảnh hưởng thế nào, đặc biệt với TH-11/TH-12 (lớp ①: mở rộng từ khoá làm
retrieval trả nhiều ứng viên hơn, có thể khiến bot bớt trả "không tìm thấy"). Không sửa số cũ.

### 31/07 · G9 — link phải có nhãn, và không được lặp

**Ba lỗi phát hiện khi dùng thật**, câu hỏi *"cho tôi các link chấm chéo theo zone của K3 và K4"*:

| Triệu chứng | Nguyên nhân thật |
|---|---|
| Mỗi link hiện **hai dòng y hệt nhau** | `tu_discord()` ghép `m.content` + `embed.url`, mà Discord tự sinh embed preview cho chính link nằm trong content → URL vào index hai lần. Sửa ở gốc: `boc_url()` bỏ trùng |
| Dòng `🔗 Link` nhìn như một cái link nữa | Đó là **tên field** của embed. Đổi thành `Link tài liệu`, bỏ emoji mở đầu để không đụng với các dòng link bên dưới |
| Hai URL trần dài 90 ký tự, chỉ khác nhau ở đoạn giữa — user không biết cái nào K3, cái nào K4 | `link_chon` chỉ mang URL, không mang chữ mô tả đứng cạnh link trong tin gốc |

Sửa lỗi thứ ba bằng cách đổi `link_chon: list[str]` → `list[LinkChon]` với `LinkChon(nhan, url)`:
`nhan` là chữ nên model được phép soạn (cắt ở 80 ký tự), `url` là dữ liệu nên vẫn bị `neo()` đối chiếu
nguyên văn với tin gốc. Render đổi theo: mỗi link một khối `**nhãn**` → URL, các khối cách nhau dòng trống.

Kiểm tay — cùng câu hỏi, sau khi sửa:

```
Dưới đây là các link chấm chéo Demo theo Zone cho khóa K3 và K4 mà bạn cần.

**Chấm chéo Demo theo Zone — K4**
https://docs.google.com/forms/d/e/1FAIpQLSdzCO…/viewform
↪ [#lab-k3 · Thao Nguyen | Vietnam · 30/07](…/1532327552297861183)

**Chấm chéo Demo theo Zone — K3**
https://docs.google.com/forms/d/e/1FAIpQLSfgkd…/viewform
↪ [#lab-k3 · Thao Nguyen | Vietnam · 30/07](…/1532327502175801364)

bỏ (bịa) = 0
```

Đã đối chiếu ngược lại nội dung hai tin gốc: nhãn K3/K4 khớp đúng (`Day 04 — Chấm chéo Demo theo Zone — K4`).

**48 test pass** (thêm 4 test cho nhãn/trùng lặp, dựng trên đúng hai tin nhắn thật này).

**Rủi ro còn lại, ghi nhận chứ chưa xử:** `nhan` là chữ do model sinh, code **không** đối chiếu được như
với `url`. Model gán nhầm nhãn (dán nhãn K3 lên link K4) thì hệ thống không phát hiện được — và loại sai
này nguy hiểm hơn không có nhãn, vì user tin nhãn rồi bấm nhầm. Hướng xử nếu cần: bắt buộc ≥1 từ khoá
phân biệt trong nhãn phải xuất hiện nguyên văn trong nội dung tin gốc.
