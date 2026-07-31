"""Lớp ① — phần bóc câu hỏi ra khỏi tin nhắn Discord.

Chỉ test được phần THUẦN. Việc "tin này có phải hỏi bot không" phụ thuộc object
của discord.py nên để cho test tay (codebase/README.md §4.1).
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from timlai import bot as bot_mod  # noqa: E402
from timlai.bot import _bo_mention  # noqa: E402
from timlai.tra_cuu import KetQua  # noqa: E402

UID = 999


def test_bo_mention_dang_thuong():
    assert _bo_mention(f"<@{UID}> link slide buổi 5", UID) == "link slide buổi 5"


def test_bo_mention_dang_nickname():
    # Discord gửi <@!id> khi user có nickname trong server. Bỏ sót dạng này thì
    # câu hỏi lọt xuống FTS5 kèm chuỗi "<@!999>" và làm lệch kết quả tìm kiếm.
    assert _bo_mention(f"<@!{UID}> link lab 2", UID) == "link lab 2"


def test_bo_mention_o_cuoi_cau():
    assert _bo_mention(f"link slide buổi 3 <@{UID}>", UID) == "link slide buổi 3"


def test_giu_nguyen_mention_cua_nguoi_khac():
    # Chỉ bỏ mention CỦA BOT. Tag người khác là một phần câu hỏi ("link của <@123>").
    assert _bo_mention(f"<@{UID}> link slide của <@123>", UID) == "link slide của <@123>"


def test_chi_mention_khong_co_chu_nao():
    # "@bot" trống -> chuỗi rỗng. Nó KHÔNG bị chặn ở cau_hoi_cho_bot() nữa: chuỗi
    # rỗng đi tiếp và ra phần giới thiệu (test_gioi_thieu.py), vẫn không gọi AI.
    assert _bo_mention(f"<@{UID}>", UID) == ""


def test_hoi_khong_dung_sqlite_o_thread_khac(db, monkeypatch):
    """Regression 31/07: gộp cả hoi() vào asyncio.to_thread làm sqlite ném
    ProgrammingError ngay câu hỏi đầu tiên — connection tạo ở thread này, dùng ở
    thread kia. Chỉ lời gọi Gemini mới được đẩy sang thread khác.
    """
    def llm_gia(cau_hoi, ung_vien):
        return KetQua(
            tim_thay=True, ngoai_pham_vi=False, cau_tra_loi="đây rồi",
            message_ids=[ung_vien[0].id], do_tin_cay="cao", can_lam_ro=None,
        ), []

    monkeypatch.setattr(bot_mod.tra_cuu, "tra_cuu", llm_gia)
    embed = asyncio.run(bot_mod.hoi(db, "link slide buổi 5"))
    assert embed.description == "đây rồi"
