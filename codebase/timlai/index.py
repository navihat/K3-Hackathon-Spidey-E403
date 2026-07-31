"""Lớp ② — Retrieval.

Discord KHÔNG cho bot dùng API search (`/messages/search` là endpoint của user
account; bot token trả 403). Nên bot phải tự dựng index.

Chọn SQLite FTS5 + BM25 thay vì vector DB: có sẵn trong stdlib, không phụ thuộc
mạng, và giải thích được trước giám khảo — mỗi kết quả truy ra được vì sao khớp.
"""

from __future__ import annotations

import datetime as dt
import re
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path

from . import config


_URL = re.compile(r"https?://[^\s<>\"'`]+")
_RAC_CUOI = ".,;:!?)]}>*_”’"      # dấu câu dính vào đuôi URL khi người ta gõ


def boc_url(van_ban: str) -> list[str]:
    """Bóc mọi URL ra khỏi một đoạn text, bỏ dấu câu dính ở đuôi. KHÔNG trùng lặp.

    Đây là NGUỒN SỰ THẬT DUY NHẤT cho link mà bot trả về: link phải bóc ra từ nội
    dung tin nhắn có thật trong index, không bao giờ lấy từ chữ mà model viết ra.

    Bỏ trùng là bắt buộc chứ không phải cho đẹp: `tu_discord()` ghép `m.content`
    với `embed.url`, mà Discord tự sinh embed preview cho chính link trong content
    -> mỗi URL vào index hai lần, và bot trả ra hai dòng y hệt nhau.
    """
    return list(dict.fromkeys(u.rstrip(_RAC_CUOI) for u in _URL.findall(van_ban)))


@dataclass
class TinNhan:
    """Một tin nhắn Discord đã chuẩn hoá. Không phụ thuộc thư viện discord."""

    id: str           # message_id — neo chống bịa, phải là id thật
    kenh: str
    tac_gia: str
    thoi_diem: str    # ISO 8601
    url: str          # message.jump_url
    noi_dung: str     # content + tên file đính kèm + text trong embed

    def dong_prompt(self) -> str:
        return f"[{self.id}] #{self.kenh} · {self.tac_gia} · {self.thoi_diem}\n{self.noi_dung}"

    def cac_link(self) -> list[str]:
        """Link tài liệu thật trong tin này (không tính jump_url của chính tin nhắn)."""
        return boc_url(self.noi_dung)

    def ngay_ngan(self) -> str:
        """dd/mm để hiện cho người đọc. Hỏng định dạng thì trả chuỗi rỗng, đừng ném."""
        try:
            return dt.datetime.fromisoformat(self.thoi_diem).strftime("%d/%m")
        except ValueError:
            return ""


SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS tin_nhan USING fts5(
    id UNINDEXED,
    kenh UNINDEXED,
    tac_gia UNINDEXED,
    thoi_diem UNINDEXED,
    url UNINDEXED,
    noi_dung,
    tokenize = "unicode61 remove_diacritics 2"
);
"""
# remove_diacritics 2 → "buoi" khớp "buổi". Học viên gõ không dấu rất nhiều
# (khảo sát: "slie buoi 5"), nên đây không phải tối ưu thừa.


def mo_db(duong_dan: Path | str | None = None) -> sqlite3.Connection:
    """Mở (và tạo nếu chưa có) index. Truyền ':memory:' khi test."""
    db = sqlite3.connect(duong_dan or config.DB_PATH)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db


def them(db: sqlite3.Connection, tin: TinNhan) -> None:
    """Ghi 1 tin nhắn. Ghi đè nếu id đã có (backfill chạy lại không nhân bản)."""
    db.execute("DELETE FROM tin_nhan WHERE id = ?", (tin.id,))
    db.execute(
        "INSERT INTO tin_nhan (id, kenh, tac_gia, thoi_diem, url, noi_dung)"
        " VALUES (:id, :kenh, :tac_gia, :thoi_diem, :url, :noi_dung)",
        asdict(tin),
    )


def them_nhieu(db: sqlite3.Connection, dsach: list[TinNhan]) -> int:
    for tin in dsach:
        them(db, tin)
    db.commit()
    return len(dsach)


def dem(db: sqlite3.Connection) -> int:
    return db.execute("SELECT count(*) FROM tin_nhan").fetchone()[0]


_TU = re.compile(r"[0-9A-Za-zÀ-ỹ]+")
_CHU_SO = re.compile(r"^(.*[A-Za-zÀ-ỹ])(\d+)$")     # "cp5" -> ("cp", "5")

# Người viết tin và người đi hỏi dùng hai lối viết khác nhau cho cùng một thứ:
# thông báo ghi "CP5", học viên gõ "checkpoint 5". unicode61 tách "CP5" thành MỘT
# token nên hai bên không bao giờ gặp nhau. Bảng này bắc cầu, chỉ cho vài từ thật
# sự hay gặp trong khoá — không phải từ điển đồng nghĩa tổng quát.
_VIET_TAT = {"checkpoint": "cp", "buoi": "b", "buổi": "b", "workshop": "ws"}


def _mo_rong(tu: list[str]) -> list[str]:
    """Sinh thêm biến thể cho từ khoá: tách 'cp5' và ghép 'checkpoint 5' -> 'cp5'."""
    them: list[str] = []
    for i, t in enumerate(tu):
        if m := _CHU_SO.fullmatch(t):
            them += [m.group(1), m.group(2)]        # "cp5"  -> "cp", "5"
        sau = tu[i + 1] if i + 1 < len(tu) else ""
        if sau.isdigit() and (viet_tat := _VIET_TAT.get(t.lower())):
            them.append(viet_tat + sau)             # "checkpoint 5" -> "cp5"
    return them


def _cau_truy_van(cau_hoi: str) -> str:
    """Biến câu hỏi tự nhiên thành biểu thức FTS5 an toàn.

    Input người dùng KHÔNG được nối thẳng vào MATCH: dấu " ( ) * : - là toán tử
    FTS5, nên "link slide buổi 5?" sẽ ném sqlite3.OperationalError.
    Cách xử lý: bóc từ, bọc mỗi từ trong ngoặc kép, nối bằng OR.
    """
    tu = _TU.findall(cau_hoi)
    tat_ca = dict.fromkeys(tu + _mo_rong(tu))       # giữ thứ tự, bỏ trùng
    return " OR ".join(f'"{t}"' for t in tat_ca)


def truy_xuat(
    db: sqlite3.Connection, cau_hoi: str, k: int | None = None
) -> list[TinNhan]:
    """Lọc thô: trả top-k tin nhắn khớp nhất, TIN MỚI NHẤT ĐỨNG ĐẦU.

    Hai tầng, và thứ tự giữa chúng quan trọng:
      1. BM25 (`rank`) lo RECALL — quyết định ứng viên nào sống sót qua LIMIT.
      2. `thoi_diem DESC` lo THỨ TỰ — tin mới nằm đầu prompt.

    Không gộp thành `ORDER BY rank, thoi_diem DESC`: BM25 gần như không bao giờ
    bằng nhau (nó thiên vị document ngắn), nên thoi_diem sẽ không bao giờ được
    dùng và tin CŨ có thể đứng trên tin mới — đúng rủi ro ④ trả link đã bị thay.

    Đây chỉ là bước LỌC, không phải bước TRẢ LỜI — LLM ở lớp ③ chọn tiếp.
    """
    mach = _cau_truy_van(cau_hoi)
    if not mach:
        return []
    rows = db.execute(
        "SELECT id, kenh, tac_gia, thoi_diem, url, noi_dung FROM ("
        "  SELECT id, kenh, tac_gia, thoi_diem, url, noi_dung FROM tin_nhan"
        "  WHERE tin_nhan MATCH ? ORDER BY rank LIMIT ?"
        ") ORDER BY thoi_diem DESC",
        (mach, k or config.SO_UNG_VIEN),
    ).fetchall()
    return [TinNhan(**dict(r)) for r in rows]
