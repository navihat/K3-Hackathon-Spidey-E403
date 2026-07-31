"""Lớp ③ — 4 lớp chỗ khó + 4 đường đi trải nghiệm.

Không gọi API thật: mỗi test truyền một `goi_llm` giả trả về đúng cái ta muốn
kiểm. Nhờ vậy test chạy trong ~1 giây, không cần API key, không tốn token, và
CHẠY ĐƯỢC KỂ CẢ KHI LLM đang bịa — đó chính là thứ cần test.
"""

import datetime as dt

from timlai import index, render, tra_cuu
from timlai.tra_cuu import KetQua


def _kq(**ghi_de) -> KetQua:
    mac_dinh = dict(
        tim_thay=True, ngoai_pham_vi=False, cau_tra_loi="ok",
        message_ids=[], do_tin_cay="cao", can_lam_ro=None,
    )
    return KetQua(**{**mac_dinh, **ghi_de})


def _gia(kq: KetQua):
    return lambda cau_hoi, ung_vien: kq


# ─────────────────────────────────────────────────────────────
# ① Nguồn sự thật — chỗ khó quan trọng nhất. Quality bar: 0 case bịa.
# ─────────────────────────────────────────────────────────────

def test_lop1_bo_id_bia_dat(tin_mau):
    """LLM trả 1 id thật + 1 id bịa -> chỉ giữ id thật, đếm id bịa.

    Câu hỏi nói rõ "lý thuyết" để `lam_ro_loai()` không xen vào: câu chung chung
    ("slide buổi 5") giờ bị ép hỏi lại loại tài liệu, và test này đang kiểm neo()
    chứ không kiểm đường hỏi lại (xem test_thoi_gian_va_loai.py).
    """
    kq, bo_di = tra_cuu.tra_cuu(
        "link slide lý thuyết buổi 5", tin_mau,
        goi_llm=_gia(_kq(message_ids=["1001", "id_khong_ton_tai"])),
    )
    assert kq.message_ids == ["1001"]
    assert bo_di == ["id_khong_ton_tai"], "id bịa phải được ĐẾM, không bỏ im lặng"


def test_lop1_bia_toan_bo_thi_ha_xuong_khong_tim_thay(tin_mau):
    """LLM khai tìm thấy nhưng mọi id đều bịa -> code hạ xuống không tìm thấy.
    Đây là chống bịa bằng CODE, không tin prompt."""
    kq, bo_di = tra_cuu.tra_cuu(
        "link slide buổi 10", tin_mau,
        goi_llm=_gia(_kq(cau_tra_loi="Đây là link slide buổi 10", message_ids=["bia_1", "bia_2"])),
    )
    assert kq.tim_thay is False
    assert kq.message_ids == []
    assert kq.do_tin_cay == "thap"
    assert len(bo_di) == 2


def test_lop1_khong_co_ung_vien_thi_khong_goi_ai(tin_mau):
    """FTS5 không ra ứng viên -> khỏi tốn 1 lời gọi AI."""
    def no_goi(cau_hoi, ung_vien):
        raise AssertionError("không được gọi AI khi danh sách ứng viên rỗng")

    kq, bo_di = tra_cuu.tra_cuu("xyz", [], goi_llm=no_goi)
    assert kq.tim_thay is False and bo_di == []


# ─────────────────────────────────────────────────────────────
# ② Mơ hồ / thiếu thông tin — hỏi lại thay vì đoán
# ─────────────────────────────────────────────────────────────

def test_lop2_giu_cau_hoi_lai(tin_mau):
    kq, _ = tra_cuu.tra_cuu(
        "link slide", tin_mau,
        goi_llm=_gia(_kq(
            do_tin_cay="thap", can_lam_ro="Bạn cần slide buổi mấy?",
            message_ids=["1001", "1002"],
        )),
    )
    assert kq.can_lam_ro == "Bạn cần slide buổi mấy?"
    assert kq.do_tin_cay == "thap"
    assert len(kq.message_ids) == 2, "mơ hồ thì liệt kê các lựa chọn, không tự chọn 1"


def test_lop2_cau_hoi_lai_hien_ra_cho_nguoi_dung(tin_mau):
    kq = _kq(do_tin_cay="thap", can_lam_ro="Buổi mấy?", message_ids=["1001"])
    text = render.thanh_text(kq, render.chon_nguon(kq, tin_mau))
    assert "Buổi mấy?" in text


# ─────────────────────────────────────────────────────────────
# ③ Ngoài phạm vi / thẩm quyền — từ chối nhưng vẫn hữu ích
# ─────────────────────────────────────────────────────────────

def test_lop3_tu_choi_cau_hoi_kien_thuc(tin_mau):
    kq, _ = tra_cuu.tra_cuu(
        "giải thích hàm softmax", tin_mau,
        goi_llm=_gia(_kq(
            tim_thay=False, ngoai_pham_vi=True, message_ids=[],
            cau_tra_loi="Mình chỉ tìm link tài liệu. Bạn hỏi trong kênh hỏi-đáp nhé.",
        )),
    )
    assert kq.ngoai_pham_vi is True
    assert kq.tim_thay is False
    assert "hỏi-đáp" in kq.cau_tra_loi, "từ chối phải kèm chỗ đi tiếp"


# ─────────────────────────────────────────────────────────────
# ④ Đặc thù domain — link cũ đã bị thay nguy hiểm hơn không trả lời
# ─────────────────────────────────────────────────────────────

def test_lop4_canh_bao_tin_cu():
    tin = index.TinNhan(
        id="9", kenh="lab-k3", tac_gia="Hà",
        thoi_diem=(dt.datetime.now() - dt.timedelta(days=30)).isoformat(),
        url="u", noi_dung="Bài lab 2",
    )
    assert "30 ngày trước" in tra_cuu.canh_bao_cu(tin)


def test_lop4_khong_canh_bao_tin_moi():
    tin = index.TinNhan(
        id="9", kenh="lab-k3", tac_gia="Hà",
        thoi_diem=dt.datetime.now().isoformat(), url="u", noi_dung="Bài lab 3",
    )
    assert tra_cuu.canh_bao_cu(tin) is None


def test_lop4_thoi_diem_sai_dinh_dang_khong_lam_sap():
    tin = index.TinNhan(id="9", kenh="k", tac_gia="a", thoi_diem="rác", url="u", noi_dung="x")
    assert tra_cuu.canh_bao_cu(tin) is None


def test_lop4_canh_bao_hien_ra_cho_nguoi_dung():
    tin = index.TinNhan(
        id="9", kenh="lab-k3", tac_gia="Hà",
        thoi_diem=(dt.datetime.now() - dt.timedelta(days=30)).isoformat(),
        url="u", noi_dung="Bài lab 2",
    )
    text = render.thanh_text(_kq(message_ids=["9"]), [tin])
    assert "⚠️" in text


# ─────────────────────────────────────────────────────────────
# 4 đường đi trải nghiệm (rubric R3) — mỗi đường ra text khác nhau
# ─────────────────────────────────────────────────────────────

def test_bon_duong_di_khac_nhau(tin_mau):
    happy = render.thanh_text(_kq(cau_tra_loi="Đây rồi", message_ids=["1001"]),
                              [tin_mau[0]])
    thap = render.thanh_text(_kq(cau_tra_loi="Có 2 cái", do_tin_cay="thap",
                                 can_lam_ro="Buổi mấy?", message_ids=["1001"]),
                             [tin_mau[0]])
    fail = render.thanh_text(_kq(tim_thay=False, cau_tra_loi="Không tìm thấy",
                                 message_ids=[]), [])
    ngoai = render.thanh_text(_kq(tim_thay=False, ngoai_pham_vi=True,
                                  cau_tra_loi="Ngoài phạm vi", message_ids=[]), [])
    assert len({happy, thap, fail, ngoai}) == 4
    assert "discord.com" in happy, "happy path phải có link tin nhắn gốc"
    assert "discord.com" not in fail, "đường failure không được kèm link nào"
