"""Sinh index bằng DATA GIẢ — chạy được toàn bộ pipeline mà chưa cần server Discord.

    python scripts/seed_gia.py                # nạp thẳng vào index.db
    python scripts/seed_gia.py --in-discord   # in ra để DÁN TAY vào server test

Đề bài ràng buộc 3 cho phép rõ: "Chỉ dùng data trong data/ hoặc **data giả tự
sinh**". Dùng data giả cũng tránh sạch rủi ro commit tin nhắn thật vào repo.

Bộ này được thiết kế để phủ đúng 22 case trong eval/golden-set.yaml, kèm 4 cái
bẫy cố ý:
    - KHÔNG có slide buổi 10        -> TH-11 phải trả "không tìm thấy"
    - KHÔNG có link QR checkin      -> TH-12
    - slide buổi 5 có 2 phiên bản   -> TH-18 phải chọn bản mới nhất
    - lab 2 đã quá deadline         -> TH-17 phải kèm cảnh báo thời điểm
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from timlai import config, index  # noqa: E402

HOM_NAY = dt.date.today()


def _ngay(truoc: int) -> str:
    return (dt.datetime.now() - dt.timedelta(days=truoc)).isoformat()


# (kênh, người gửi, số ngày trước, nội dung)
TIN = [
    ("thong-bao", "BTC", 30, "Chào mừng K3! Nền tảng học: https://vlearn.aithucchien.vn"),
    ("thong-bao", "BTC", 30, "Trang khoá học chính thức: https://aithucchien.vn/k3"),
    ("thong-bao", "BTC", 29, "Codelabs: https://codelabs.aithucchien.vn — đăng nhập bằng email đăng ký"),
    ("thong-bao", "BTC", 28, "Phoenix dashboard theo dõi tiến độ: https://phoenix.aithucchien.vn"),
    ("thong-bao-chung", "BTC", 3, "Slide hackathon Day 1 + Day 2: https://drive.google.com/file/d/hackathon-slides"),
    ("thong-bao-chung", "BTC", 2, "Nhắc: hackathon bắt đầu 09:00 mai, có mặt trước 15 phút"),

    ("ly-thuyet-k3", "LabCoach Minh", 21, "Slide buổi 1 — Giới thiệu LLM: https://drive.google.com/file/d/slide-b1"),
    ("ly-thuyet-k3", "LabCoach Minh", 18, "Slide buổi 2 — Prompt engineering: https://drive.google.com/file/d/slide-b2"),
    ("ly-thuyet-k3", "anh Tuấn", 14, "Slide buổi 3 — Transformer & Attention: https://drive.google.com/file/d/slide-b3"),
    ("ly-thuyet-k3", "LabCoach Minh", 11, "Tài liệu buổi 4 — RAG cơ bản: https://drive.google.com/file/d/tailieu-b4"),
    # TH-18: hai phiên bản slide buổi 5, phải chọn bản mới
    ("ly-thuyet-k3", "LabCoach Minh", 8, "Slide buổi 5 — AI Agent: https://drive.google.com/file/d/slide-b5-v1"),
    ("ly-thuyet-k3", "LabCoach Minh", 6, "Slide buổi 5 BẢN CẬP NHẬT (sửa lỗi trang 12): https://drive.google.com/file/d/slide-b5-v2"),
    ("ly-thuyet-k3", "LabCoach Minh", 4, "Slide buổi 6 — Đánh giá & kiểm thử: https://drive.google.com/file/d/slide-b6"),

    ("lab-k3", "LabCoach Hà", 17, "Bài lab 1 — gọi API lần đầu: https://codelabs.aithucchien.vn/lab1"),
    # TH-17: lab 2 đã quá deadline
    ("lab-k3", "LabCoach Hà", 12, "Bài lab 2 — dựng RAG mini: https://codelabs.aithucchien.vn/lab2 (deadline 23:59 sau 3 ngày)"),
    ("lab-k3", "LabCoach Hà", 5, "Bài lab 3 — agent có tool: https://codelabs.aithucchien.vn/lab3"),

    ("tai-nguyen", "LabCoach Minh", 20, "Build buổi 1 — repo mẫu: https://github.com/aithucchien/build-b1"),
    ("tai-nguyen", "LabCoach Minh", 13, "Build buổi 2 — template FastAPI: https://github.com/aithucchien/build-b2"),
    ("tai-nguyen", "LabCoach Hà", 9, "Hướng dẫn setup môi trường: https://github.com/aithucchien/setup-guide"),
    ("tai-nguyen", "LabCoach Minh", 7, "Slide buổi 5 mình có mirror ở đây nữa: https://github.com/aithucchien/slide-b5"),
]

DINH_KEM = {
    # id tin nhắn -> tên file, mô phỏng slide đăng dạng file PDF chứ không phải URL
    7: "day01-slide-blue-v1.pdf",
    11: "day05-agent-v1.pdf",
    12: "day05-agent-v2-final.pdf",
}


def in_de_dan() -> None:
    """In 20 tin nhắn theo từng kênh để dán tay vào server Discord test.

    Dán TAY bằng tài khoản người, không dùng webhook/bot: backfill.py bỏ qua
    `m.author.bot`, dán bằng bot thì index sẽ rỗng.

    Dán ĐÚNG THỨ TỰ trong mỗi kênh — TH-18 đòi bot chọn bản slide buổi 5 mới nhất,
    mà "mới nhất" tính theo thời điểm đăng.
    """
    theo_kenh: dict[str, list[tuple[int, str]]] = {}
    for kenh, _tac_gia, truoc, noi_dung in TIN:
        theo_kenh.setdefault(kenh, []).append((truoc, noi_dung))

    for kenh, dsach in theo_kenh.items():
        print(f"\n{'='*70}\n#{kenh}   ({len(dsach)} tin — dán lần lượt từ trên xuống)\n{'='*70}")
        for truoc, noi_dung in dsach:
            print(f"\n{noi_dung}")
            print(f"    ^ bản gốc lùi {truoc} ngày — Discord sẽ đóng dấu HÔM NAY")

    print(f"\n{'='*70}")
    print("LƯU Ý: dán vào Discord thì mọi tin đều mang thời điểm hôm nay, nên")
    print("canh_bao_cu() không kích hoạt và case ④ (TH-17) sẽ không tái hiện được.")
    print("Vì vậy: lượt eval R4 chạy trên seed_gia (có lùi ngày), Discord thật để")
    print("demo end-to-end. Cả hai đều là data giả — đúng ràng buộc 3 của đề bài.")


def main() -> None:
    if "--in-discord" in sys.argv:
        in_de_dan()
        return

    db = index.mo_db()
    db.execute("DELETE FROM tin_nhan")

    dsach = []
    for i, (kenh, tac_gia, truoc, noi_dung) in enumerate(TIN, start=1):
        them = DINH_KEM.get(i, "")
        dsach.append(
            index.TinNhan(
                id=f"{1_000_000_000_000_000 + i}",     # giống snowflake id của Discord
                kenh=kenh,
                tac_gia=tac_gia,
                thoi_diem=_ngay(truoc),
                url=f"https://discord.com/channels/111/222/{1_000_000_000_000_000 + i}",
                noi_dung=f"{noi_dung} {them}".strip(),
            )
        )

    index.them_nhieu(db, dsach)
    print(f"Đã seed {index.dem(db)} tin nhắn giả vào {config.DB_PATH.name}")
    print("\nBẫy cố ý (để golden set có case thất bại thật):")
    print("  - không có slide buổi 10   -> TH-11 phải trả 'không tìm thấy'")
    print("  - không có link QR checkin -> TH-12")
    print("  - slide buổi 5 có 2 bản    -> TH-18 phải chọn bản mới nhất")
    print("  - lab 2 đã quá deadline    -> TH-17 phải kèm cảnh báo")
    print("\nThử ngay:  python scripts/thu_hoi.py \"link slide buổi 5\"")


if __name__ == "__main__":
    main()
