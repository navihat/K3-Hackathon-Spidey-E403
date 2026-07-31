"""Ba luật do CODE quyết định, không do prompt: thời gian · loại tài liệu · VLearn.

Cả ba đều là chỗ model sai LẶNG LẼ nếu để nó tự lo:
  - thời gian: model không biết hôm nay là ngày mấy, "hôm qua" của nó là ngày trong
    dữ liệu huấn luyện;
  - loại tài liệu: model chọn tin khớp nhất rồi khai do_tin_cay="cao", trong khi
    "slide buổi 5" có thể là slide lý thuyết, workshop hay lab;
  - VLearn: link cố định của khoá, không nằm trong tin nhắn nào nên không thể để
    model tự viết ra (neo() sẽ gỡ đúng như mọi URL bịa khác).
"""

import datetime as dt

import pytest

from timlai import config, index, render, tra_cuu
from timlai.tra_cuu import KetQua

HOM_NAY = dt.date(2026, 7, 31)          # thứ Sáu


def _kq(**doi) -> KetQua:
    mac_dinh = dict(
        tim_thay=True, ngoai_pham_vi=False, cau_tra_loi="đây rồi",
        message_ids=[], do_tin_cay="cao", can_lam_ro=None,
    )
    return KetQua(**{**mac_dinh, **doi})


def _gia(kq: KetQua):
    return lambda cau_hoi, ung_vien: kq


def _tin(id_, kenh, noi_dung, truoc_may_ngay) -> index.TinNhan:
    ngay = dt.datetime(2026, 7, 31, 9, 0) - dt.timedelta(days=truoc_may_ngay)
    return index.TinNhan(
        id=id_, kenh=kenh, tac_gia="LabCoach", thoi_diem=ngay.isoformat(),
        url=f"https://discord.com/channels/1/2/{id_}", noi_dung=noi_dung,
    )


# Ba loại tài liệu cho CÙNG một buổi — đúng tình huống "slide buổi 5 là slide gì?"
BUOI_5 = [
    _tin("5001", "ly-thuyet-k3", "Slide buổi 5 — AI Agent: https://drive.google.com/file/d/b5", 1),
    _tin("5002", "tai-nguyen", "Slide workshop buổi 5 (build): https://github.com/x/ws5", 3),
    _tin("5003", "lab-k3", "Bài lab buổi 5: https://codelabs.aithucchien.vn/lab5", 10),
]


# ── Thời gian: "hôm qua" là ngày nào? ─────────────────────────────────


@pytest.mark.parametrize(
    "cau, tu, den",
    [
        ("slide hôm nay", dt.date(2026, 7, 31), dt.date(2026, 7, 31)),
        ("slide workshop hôm qua", dt.date(2026, 7, 30), dt.date(2026, 7, 30)),
        ("link hôm kia", dt.date(2026, 7, 29), dt.date(2026, 7, 29)),
        ("link 3 ngày trước", dt.date(2026, 7, 28), dt.date(2026, 7, 28)),
        ("slide tuần này", dt.date(2026, 7, 27), dt.date(2026, 7, 31)),      # thứ Hai → nay
        ("slide tuần trước", dt.date(2026, 7, 20), dt.date(2026, 7, 26)),
        ("link tháng này", dt.date(2026, 7, 1), dt.date(2026, 7, 31)),
        ("link tháng trước", dt.date(2026, 6, 1), dt.date(2026, 6, 30)),
        ("slide ngày 24/07", dt.date(2026, 7, 24), dt.date(2026, 7, 24)),
        ("slide 24-07-2026", dt.date(2026, 7, 24), dt.date(2026, 7, 24)),
    ],
)
def test_quy_doi_moc_thoi_gian(cau, tu, den):
    moc = tra_cuu.moc_thoi_gian(cau, HOM_NAY)
    assert moc is not None, "phải nhận ra được mốc thời gian"
    assert (moc[0], moc[1]) == (tu, den)


@pytest.mark.parametrize("cau", ["link slide buổi 5", "link lab 2", "link nộp cp5", "slide 32/13"])
def test_cau_khong_co_moc_thoi_gian(cau):
    """"buổi 5", "lab 2", "cp5" KHÔNG được hiểu thành ngày tháng."""
    assert tra_cuu.moc_thoi_gian(cau, HOM_NAY) is None


def test_loc_ung_vien_theo_dung_ngay():
    giu = tra_cuu.loc_theo_ngay(BUOI_5, dt.date(2026, 7, 30), dt.date(2026, 7, 30))
    assert [t.id for t in giu] == ["5001"], "chỉ tin của đúng ngày 30/07 được giữ"


def test_hom_qua_khong_co_tin_thi_noi_ro_ngay_khong_goi_ai():
    """Không có tin nào trong ngày -> trả lời luôn, không tốn lời gọi AI, và PHẢI
    nói ra mình đã hiểu "hôm qua" là ngày nào để user sửa được nếu bot hiểu sai."""

    def no_goi(cau_hoi, ung_vien):
        raise AssertionError("hết ứng viên sau khi lọc ngày thì đừng gọi AI")

    # BUOI_5 không có tin nào của ngày 29/07 (hôm kia)
    kq, _ = tra_cuu.tra_cuu("slide hôm kia", BUOI_5, goi_llm=no_goi, hom_nay=HOM_NAY)
    assert kq.tim_thay is False
    assert "29/07/2026" in kq.moc_ngay and "Thứ Tư" in kq.moc_ngay


def test_chi_dua_tin_dung_ngay_cho_llm():
    """Model chỉ được nhìn thấy ứng viên của đúng ngày đó — lọc bằng code, không
    nhờ model tự đọc timestamp rồi so sánh."""
    thay: dict = {}

    def ghi_lai(cau_hoi, ung_vien):
        thay["ids"] = [t.id for t in ung_vien]
        return _kq(message_ids=["5001"])

    tra_cuu.tra_cuu("slide workshop hôm qua", BUOI_5, goi_llm=ghi_lai, hom_nay=HOM_NAY)
    assert thay["ids"] == ["5001"]


def test_moc_ngay_hien_ra_cho_nguoi_dung():
    kq, _ = tra_cuu.tra_cuu(
        "slide hôm qua", BUOI_5, goi_llm=_gia(_kq(message_ids=["5001"])), hom_nay=HOM_NAY
    )
    assert "🗓" in render.thanh_text(kq, [])
    assert "30/07/2026" in render.thanh_text(kq, [])


def test_model_khong_tu_khai_duoc_moc_ngay():
    kq, _ = tra_cuu.neo(_kq(message_ids=["5001"], moc_ngay="hôm qua là 01/01/1970"), BUOI_5)
    assert kq.moc_ngay is None, "ngày tháng là việc của code, model khai gì cũng bỏ"


# ── Loại tài liệu: "slide buổi 5" là slide gì? ────────────────────────


def test_nhan_ra_loai_cua_tin_nhan():
    # Tin thứ 2 nằm ở #tai-nguyen nhưng nội dung ghi "workshop" -> nhãn cụ thể thắng.
    assert [tra_cuu.loai_cua(t) for t in BUOI_5] == ["lý thuyết", "workshop", "lab"]


def test_hoi_chung_chung_thi_hoi_lai_loai_nao():
    """Bug người dùng báo 31/07: "cho tôi slide buổi 5" — model chọn đại slide lý
    thuyết và khai do_tin_cay="cao", trong khi buổi 5 còn có workshop và lab."""
    kq, _ = tra_cuu.tra_cuu(
        "cho tôi slide buổi 5", BUOI_5,
        goi_llm=_gia(_kq(message_ids=["5001"], do_tin_cay="cao")), hom_nay=HOM_NAY,
    )
    assert kq.do_tin_cay == "thap"
    assert kq.can_lam_ro and "lý thuyết" in kq.can_lam_ro and "lab" in kq.can_lam_ro
    assert len(kq.message_ids) == 3, "mỗi loại một tin mới nhất làm lựa chọn"


def test_hoi_lai_thi_bo_link_da_chon():
    # Đang hỏi "loại nào?" mà vẫn chìa ra link của MỘT loại là tự trả lời hộ user.
    kq, _ = tra_cuu.tra_cuu(
        "cho tôi slide buổi 5", BUOI_5,
        goi_llm=_gia(_kq(
            message_ids=["5001"],
            link_chon=[tra_cuu.LinkChon(nhan="Slide buổi 5", url="https://drive.google.com/file/d/b5")],
        )),
        hom_nay=HOM_NAY,
    )
    assert kq.link_chon == []


@pytest.mark.parametrize(
    "cau",
    [
        "slide lý thuyết buổi 5",      # đã nói rõ loại
        "slide workshop buổi 5",
        "link lab buổi 5",
        "link slide của anh Tuấn",     # đã có neo khác: tên người gửi
    ],
)
def test_da_ro_thi_khong_hoi_lai(cau):
    assert tra_cuu.can_hoi_ro_loai(cau, BUOI_5) == []


def test_chi_mot_loai_thi_khong_hoi_lai():
    # Hỏi "loại nào?" khi chỉ có đúng một loại là hỏi thừa.
    assert tra_cuu.can_hoi_ro_loai("slide buổi 5", BUOI_5[:1]) == []


def test_khong_tim_thay_thi_khong_hoi_loai(tin_mau):
    """Lớp ① phải giữ nguyên: model nói không tìm thấy thì đừng biến nó thành câu
    hỏi lại — hỏi "loại nào?" cho một thứ không tồn tại chỉ dẫn user đi vòng."""
    kq, _ = tra_cuu.tra_cuu(
        "slide buổi 10", BUOI_5,
        goi_llm=_gia(_kq(tim_thay=False, message_ids=[], cau_tra_loi="Mình không tìm thấy")),
        hom_nay=HOM_NAY,
    )
    assert kq.tim_thay is False and kq.can_lam_ro is None


# ── VLearn: link cố định cho slide lý thuyết ──────────────────────────


def test_hoi_ly_thuyet_thi_chi_sang_vlearn():
    kq, _ = tra_cuu.tra_cuu(
        "slide lý thuyết buổi 5", BUOI_5,
        goi_llm=_gia(_kq(message_ids=["5001"])), hom_nay=HOM_NAY,
    )
    assert kq.goi_y_vlearn is True
    assert config.LINK_VLEARN in render.thanh_text(kq, [])


def test_hoi_lai_loai_cung_kem_vlearn():
    # "lý thuyết" là một trong các lựa chọn -> nói luôn nó nằm ở VLearn.
    kq, _ = tra_cuu.tra_cuu(
        "cho tôi slide buổi 5", BUOI_5,
        goi_llm=_gia(_kq(message_ids=["5001"])), hom_nay=HOM_NAY,
    )
    assert kq.goi_y_vlearn is True


def test_hoi_lab_thi_khong_gan_vlearn():
    kq, _ = tra_cuu.tra_cuu(
        "link lab buổi 5", BUOI_5,
        goi_llm=_gia(_kq(message_ids=["5003"])), hom_nay=HOM_NAY,
    )
    assert kq.goi_y_vlearn is False
    assert config.LINK_VLEARN not in render.thanh_text(kq, [])


def test_link_vlearn_hien_kem_nhan_link_co_dinh():
    """VLearn không nằm trong tin nhắn nào nên KHÔNG neo được. Nó phải nhìn khác hẳn
    các link bóc từ tin gốc, nếu không thì lời hứa "mọi link đều truy được về tin
    nhắn thật" là lời hứa suông."""
    assert "link cố định" in render.VLEARN


def test_model_khong_tu_khai_duoc_vlearn(tin_mau):
    kq, _ = tra_cuu.neo(_kq(message_ids=["1001"], goi_y_vlearn=True), tin_mau)
    assert kq.goi_y_vlearn is False


def test_model_van_khong_duoc_tu_go_link_vlearn(tin_mau):
    """Cờ goi_y_vlearn do code bật, còn URL thì vẫn phải đi qua neo() như mọi URL
    khác: model gõ thẳng link VLearn vào câu trả lời là bị gỡ và bị ĐẾM."""
    kq, bo_di = tra_cuu.neo(
        _kq(message_ids=["1001"], cau_tra_loi=f"Xem ở {config.LINK_VLEARN} nhé"), tin_mau
    )
    assert config.LINK_VLEARN not in kq.cau_tra_loi
    assert config.LINK_VLEARN in bo_di
