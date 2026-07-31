"""Đường đi thứ 5 — bot tự giới thiệu, và embed không còn tiêu đề.

Đường này KHÔNG gọi LLM: nhận diện bằng regex, trả về một hằng số. Nên nó thuộc về
pytest chứ không thuộc về golden set — golden set đo chất lượng QUYẾT ĐỊNH CỦA AI,
nhét mấy case luôn-pass vào đó chỉ làm đẹp tỉ lệ pass (spec §7 cấm).

Rủi ro thật của tính năng này là NHẬN DIỆN NHẦM: một câu hỏi tài liệu bị nuốt thành
lời giới thiệu. `test_khong_case_nao_trong_golden_set_bi_nham` canh đúng chỗ đó, và
nó chạy trên chính 22 case của golden set.
"""

import asyncio

import pytest
import yaml

from timlai import bot as bot_mod
from timlai import config, index, render, tra_cuu
from timlai.tra_cuu import KetQua

# ── Nhận diện: cái gì LÀ câu hỏi về bot ───────────────────────────────

VE_BOT = [
    "Chào bạn, bạn có thể giúp mình những gì?",   # đúng câu trong ảnh chụp Discord
    "bạn là ai",
    "ban la ai",                                   # gõ không dấu
    "bot làm được gì",
    "bạn có những chức năng gì",
    "hướng dẫn sử dụng",
    "dùng bot như thế nào",
    "help",
    "chào bạn",
    "hi",
    "",                                            # @mention trống -> vẫn phải trả lời
    "spidey",
]


@pytest.mark.parametrize("cau", VE_BOT)
def test_nhan_ra_cau_hoi_ve_bot(cau):
    assert tra_cuu.la_hoi_ve_bot(cau) is True


# ── Nhận diện: cái gì KHÔNG PHẢI (chỗ nguy hiểm) ──────────────────────

KHONG_PHAI = [
    "bạn giúp mình tìm link slide buổi 5 với",    # có "giúp… gì"? vẫn là hỏi tài liệu
    "ai có slide buổi 5 không",
    "link hướng dẫn onboarding",                   # "hướng dẫn" là TÊN TÀI LIỆU thật
    "softmax là gì",                               # lớp ③ — phải để LLM từ chối
    "bài tập buổi 3 làm thế nào",                  # lớp ③
    "cho em xin lại link slide với ạ",
    "buổi 3 làm gì",
]


@pytest.mark.parametrize("cau", KHONG_PHAI)
def test_khong_nham_cau_hoi_tai_lieu(cau):
    assert tra_cuu.la_hoi_ve_bot(cau) is False


def test_khong_case_nao_trong_golden_set_bi_nham():
    """22 case golden set đều phải đi đường tra cứu bình thường.

    Nhận diện nhầm ở đây không chỉ làm hỏng một câu trả lời — nó khiến case đó không
    bao giờ tới được LLM, tức là bảng kết quả R4 đo một thứ khác với thứ nó ghi.
    """
    cases = yaml.safe_load(config.GOLDEN_SET.read_text(encoding="utf-8"))
    nham = [c["id"] for c in cases if tra_cuu.la_hoi_ve_bot(c["input"])]
    assert nham == [], f"case bị nuốt thành lời giới thiệu: {nham}"


# ── Nội dung câu giới thiệu ───────────────────────────────────────────


def test_gioi_thieu_khong_chua_url():
    """Phần giới thiệu KHÔNG đi qua neo(), nên một cái link ở đây là link không ai
    kiểm được — đúng thứ quality bar §7 cấm. Giữ nó là văn bản thuần."""
    assert index.boc_url(tra_cuu.GIOI_THIEU) == []


def test_gioi_thieu_noi_du_lam_duoc_gi_va_khong_lam_gi():
    txt = tra_cuu.GIOI_THIEU.lower()
    assert "5 kênh" in txt, "phải nói rõ phạm vi (G2)"
    assert "không" in txt, "phải nói cả thứ mình KHÔNG làm, không chỉ khoe"
    assert "/timlai" in txt and "reply" in txt, "phải chỉ cách hỏi"


# ── Không tốn lời gọi AI, không kèm nguồn ─────────────────────────────


def test_khong_goi_ai_khi_hoi_ve_bot(tin_mau):
    """Free tier có 20 lời gọi/ngày/model — một lời chào không được ăn mất một cái."""

    def no_goi(cau_hoi, ung_vien):
        raise AssertionError("không được gọi AI cho câu hỏi về chính bot")

    kq, bo_di = tra_cuu.tra_cuu("bạn làm được gì", tin_mau, goi_llm=no_goi)
    assert kq.gioi_thieu is True
    assert kq.cau_tra_loi == tra_cuu.GIOI_THIEU
    assert bo_di == []


def test_gioi_thieu_khong_kem_nguon(tin_mau):
    # G3: đang nói về bản thân thì mọi link kèm theo đều là link lạc.
    assert render.chon_nguon(tra_cuu.ket_qua_gioi_thieu(), tin_mau) == []


def test_model_khong_tu_khai_duoc_gioi_thieu(tin_mau):
    """`gioi_thieu` nằm trong response_schema nên model nhìn thấy và có thể tự khai
    true — lúc đó một câu hỏi tài liệu sẽ bị trả lời bằng lời giới thiệu. Chỉ CODE
    được bật cờ này; neo() hạ mọi khai báo của model xuống."""
    kq, _ = tra_cuu.neo(
        KetQua(
            tim_thay=True, ngoai_pham_vi=False, cau_tra_loi="đây rồi",
            message_ids=["1001"], do_tin_cay="cao", can_lam_ro=None, gioi_thieu=True,
        ),
        tin_mau,
    )
    assert kq.gioi_thieu is False


def test_mention_trong_ra_gioi_thieu(db):
    """@mention trống đi hết đường bot.hoi() -> ra embed giới thiệu, không gọi AI."""
    embed = asyncio.run(bot_mod.hoi(db, ""))
    assert embed.description == tra_cuu.GIOI_THIEU
    assert "3 tin nhắn" in embed.footer.text     # bot biết mình đang theo dõi bao nhiêu


# ── Embed: đã bỏ tiêu đề, chỉ còn màu để phân biệt ────────────────────


def _kq(**doi) -> KetQua:
    mac_dinh = dict(
        tim_thay=True, ngoai_pham_vi=False, cau_tra_loi="ok",
        message_ids=[], do_tin_cay="cao", can_lam_ro=None,
    )
    return KetQua(**{**mac_dinh, **doi})


NAM_DUONG = [
    _kq(message_ids=["1001"]),                                        # happy
    _kq(do_tin_cay="thap", can_lam_ro="Buổi mấy?"),                   # ② mơ hồ
    _kq(tim_thay=False, cau_tra_loi="Mình không tìm thấy link này."),  # ① không căn cứ
    _kq(tim_thay=False, ngoai_pham_vi=True, cau_tra_loi="Ngoài phạm vi"),  # ③
    tra_cuu.ket_qua_gioi_thieu(),                                     # giới thiệu
]


@pytest.mark.parametrize("kq", NAM_DUONG)
def test_khong_con_tieu_de_o_moi_duong(kq):
    """Bỏ tiêu đề embed: câu "Không tìm thấy" in đậm phía trên là thứ đập vào mắt
    trước, trong khi phần mô tả ngay dưới đã nói y hệt như vậy."""
    assert render.thanh_embed(kq, [], []).title is None


def test_nam_duong_van_phan_biet_duoc_bang_mau():
    # Bỏ tiêu đề rồi thì màu là tín hiệu DUY NHẤT còn lại — không được trùng.
    assert len({render.thanh_embed(kq, [], []).color for kq in NAM_DUONG}) == 5


def test_embed_loi_van_noi_ro_dang_hong():
    # Bỏ tiêu đề không được làm mất thông tin: câu "đang không trả lời được" phải
    # chuyển xuống phần mô tả chứ không biến mất (G7).
    e = render.embed_loi(RuntimeError("429 RESOURCE_EXHAUSTED"))
    assert e.title is None
    assert "không trả lời được" in e.description
