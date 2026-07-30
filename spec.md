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
  | **G2 — Làm rõ nó làm tốt đến đâu** | Câu đầu tiên của bot: "Mình có thể tìm link tài liệu (slide, bài lab, hướng dẫn) từ 5 kênh: thông báo, build, lý thuyết, lab. Ngoài ra mình không trả lời được." |
  | **G11 — Giải thích vì sao** | Mỗi câu trả lời kèm link dẫn đến tin nhắn gốc + tên người gửi — user tự kiểm tra được. |
  | **G9 — Sửa dễ dàng** | User có thể hỏi lại ngay bằng câu khác mà không cần reset flow. |
  | **G8 — Gạt bỏ dễ dàng** | Nếu bot trả lời sai link, user ignore và tự scroll kênh — không block flow. |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)

| # | Tình huống | Lớp | Hành vi mong muốn | Nguyên tắc |
|---|---|---|---|---|
| 1 | User hỏi "link slide buổi 5" — có 2 link khác nhau từ 2 kênh (lý thuyết + build) | ② Mơ hồ | Trả về cả 2 kèm tên kênh + link gốc, để user tự chọn | G11 |
| 2 | User hỏi "link slide buổi 10" — chưa có buổi 10 trong các kênh | ① Không căn cứ | "Mình không tìm thấy link slide buổi 10 trong các kênh. Có thể bạn nhầm buổi hoặc slide chưa được đăng." | G10 |
| 3 | User hỏi "giải thích hàm softmax giúp mình" (câu hỏi kiến thức) | ③ Ngoài phạm vi | "Mình chỉ tìm link tài liệu từ các kênh thôi. Bạn hỏi bài trong kênh hỏi-đáp hoặc tag Lab Coach nhé." | G2 |
| 4 | User hỏi "link lab 2" — link đã hết hạn (hết thời gian làm lab) | ④ Đặc thù domain | Trả link kèm lưu ý: "Link lab 2 đã hết hạn (dd/mm). Nếu cần gia hạn bạn liên hệ Lab Coach." | G11 |
| 5 | User hỏi "link slide" — quá chung chung, không rõ buổi nào | ② Mơ hồ | "Mình tìm thấy N link slide trong các kênh. Bạn nói rõ buổi mấy để mình tìm chính xác?" | G10 |
| 6 | User gõ sai chính tả: "slie buoi 5" | ② Mơ hồ | Dùng fuzzy match, tìm đúng "slide buổi 5" → trả link | G11 |
| 7 | User hỏi "link checkin" — QR checkin không nằm trong 5 kênh được index | ① Không căn cứ | "Mình không tìm thấy link này trong phạm vi các kênh mình quản lý." | G10 |
| 8 | User hỏi "link VLearn" — có link VLearn trong kênh thông báo | — | Trả link VLearn kèm tên người gửi + link gốc | G11 |
| 9 | User hỏi "link bài 3 của Tuấn" — có link nhưng không rõ "bài 3" là bài nào | ② Mơ hồ | "Mình tìm thấy 1 link có từ 'bài 3' trong kênh lab: [link]. Đây có phải bạn cần không?" | G10 |
| 10 | User hỏi "link slide hôm qua" — "hôm qua" là khái niệm tương đối | ② Mơ hồ | Cần mapping "hôm qua" → ngày cụ thể dựa trên thời điểm hỏi, rồi tìm link. Nếu không xác định được: "Bạn nói rõ buổi mấy hoặc ngày tháng nhé." | G10 |

## §6. Bốn đường đi của trải nghiệm

- **Happy path**: User: "link slide buổi 5" → Bot: "Link slide buổi 5 do LabCoach [Tên] gửi trong kênh 📘lý-thuyết-k3: [link]. [Link gốc]"
- **Low-confidence (②)**: User: "slide buổi 5" → Bot tìm thấy 2 link → "Mình thấy 2 link liên quan: [link 1] trong 📘lý-thuyết-k3 · [link 2] trong 🛠build. Bạn xem cái nào đúng? [Link gốc 1] [Link gốc 2]"
- **Failure/không căn cứ (①)**: User: "link slide buổi 10" → Bot: "Mình không tìm thấy link slide buổi 10 trong các kênh. Bạn thử gõ 'link slide buổi 9' nhé?"
- **Correction (user sửa)**: User: "link lab 2" → Bot: "Link lab 2 trong 🧪lab-k3: [link]" → User: "ý mình bài 2 của build" → Bot: "Link bài 2 trong 🛠build: [link]"
- **Khi bị đòi ngoài phạm vi (③)**: User: "giải thích hàm softmax" → Bot: "Mình chỉ tìm link tài liệu từ 5 kênh thôi (thông báo, build, lý thuyết, lab). Bạn hỏi bài trong kênh hỏi-đáp hoặc hỏi AI Tutor trên VLearn nhé."
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

- **Golden set** (≥20 case, file tại [`eval/golden-set.md`](eval/golden-set.md)):

- **Quality bar** (chốt từ 23:59, giữ nguyên sau đó):
  > "Đạt khi **≥85%** qua bộ golden set, và **0 case bịa nguồn** (lớp ①)."

## §8. Phân công & kế hoạch

- **Phân công có tên**:
  - Spec + evidence: Trương Thảo Nguyên
  - Prompt + golden set: Đinh Quốc Trung
  - Code prototype: Trương Văn Thái
  - Demo: Trương Văn Thái

- **Willing users** (≥3 tên):
  1. [Tên bạn học cùng lớp] — đã xác nhận
  2. [Tên bạn cùng zone] — đã xác nhận
  3. [Tên bạn khác] — đã xác nhận

  *Kế hoạch validation CP5*: Giao task thật ("tìm giúp mình slide buổi 2"), quan sát, hỏi 3 câu: ① Điều gì khó hiểu? ② Kết quả có tin không? ③ Có dùng thật không? Log vào `validation/`.

- **Multi-prototype** (nếu làm): Chưa thực hiện do nhóm 1 người.

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| [30/07] | Tạo spec lần đầu | — |
