"""Hỏi 1 câu ngoài Discord — vòng lặp dev nhanh nhất.

    python scripts/thu_hoi.py "link slide buổi 5"
    python scripts/thu_hoi.py "link slide buổi 5" --chi-loc    # chỉ xem FTS5, không gọi AI

`--chi-loc` là công cụ chẩn đoán quan trọng nhất: nếu FTS5 không trả ra tin
nhắn đúng thì lỗi ở lớp ② (retrieval), sửa prompt vô ích.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from timlai import index, render, tra_cuu  # noqa: E402


def main() -> None:
    doi = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not doi:
        raise SystemExit('Dùng: python scripts/thu_hoi.py "link slide buổi 5"')
    cau_hoi = " ".join(doi)
    chi_loc = "--chi-loc" in sys.argv

    db = index.mo_db()
    if index.dem(db) == 0:
        raise SystemExit("index.db trống — chạy `python scripts/seed_gia.py` trước.")

    ung_vien = index.truy_xuat(db, cau_hoi)
    print(f'CÂU HỎI: "{cau_hoi}"')
    print(f"\n── Lớp ② FTS5 trả {len(ung_vien)} ứng viên " + "─" * 30)
    for t in ung_vien[:10]:
        print(f"  [{t.id}] #{t.kenh:<18} {t.thoi_diem[:10]}  {t.noi_dung[:70]}")
    if chi_loc:
        return

    kq, bo_di = tra_cuu.tra_cuu(cau_hoi, ung_vien)
    nguon = render.chon_nguon(kq, ung_vien)

    print(f"\n── Lớp ③ AI quyết định " + "─" * 38)
    print(f"  tim_thay      = {kq.tim_thay}")
    print(f"  ngoai_pham_vi = {kq.ngoai_pham_vi}")
    print(f"  do_tin_cay    = {kq.do_tin_cay}")
    print(f"  bỏ (bịa)      = {len(bo_di)} {bo_di}")
    # Ba cờ do CODE đặt — in ra để phân biệt "model trả lời thế" với "code ép thế".
    print(f"  [code] giới thiệu={kq.gioi_thieu} · vlearn={kq.goi_y_vlearn} · mốc={kq.moc_ngay}")
    print(f"\n── Người dùng thấy " + "─" * 42)
    print(render.thanh_text(kq, nguon))


if __name__ == "__main__":
    main()
