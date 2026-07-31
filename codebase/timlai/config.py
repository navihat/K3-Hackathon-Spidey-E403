"""Cấu hình — đọc từ .env, không hardcode secret ở bất cứ đâu."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Console Windows mặc định là cp1252 -> mọi print() có dấu tiếng Việt sẽ ném
# UnicodeEncodeError. Sửa ở đây một lần vì mọi entry point đều import config,
# thay vì bắt bạn set PYTHONIOENCODING mỗi lần chạy.
for _luong in (sys.stdout, sys.stderr):
    if hasattr(_luong, "reconfigure"):
        try:
            _luong.reconfigure(encoding="utf-8")
        except (ValueError, OSError):
            pass

# codebase/timlai/config.py -> codebase/
CODEBASE = Path(__file__).resolve().parent.parent
REPO = CODEBASE.parent

load_dotenv(CODEBASE / ".env")

DB_PATH = CODEBASE / "index.db"          # .gitignore đã chặn — chứa tin nhắn thật
GOLDEN_SET = REPO / "eval" / "golden-set.yaml"
KET_QUA_DIR = REPO / "eval" / "ket-qua"

# Slide lý thuyết KHÔNG được đăng trong Discord — nơi chính thức của nó là VLearn.
# Đây là hằng số do người viết ra, không phải link model sinh: nó không đi qua neo()
# nên phải nằm trong code, phải hiện kèm nhãn "link cố định", và phải khác hẳn về mặt
# hình thức với các link bóc từ tin nhắn thật (render.py, mục "Slide lý thuyết").
LINK_VLEARN = "https://vlearn.dev/course/comp2010/study-overview"

# Đo tay 30/07 trên đúng shape request của _goi_gemini (xem §4.3 codebase/README.md):
#   gemini-3.6-flash      4.6s — sát mốc <5s ở spec §7, và KHÔNG tắt được thinking
#   gemini-3.5-flash      3.6s — chọn đúng bản slide mới nhất  <- chọn lúc đầu
#   gemini-2.5-flash      404  — Google ngừng cấp cho key mới
#
# Đo lại 31/07 vì 3.5-flash trả 503 UNAVAILABLE liên tục (~4 phút backoff vẫn 503,
# hỏng cả lượt eval ngay từ case đầu). Cùng một câu hỏi, cùng shape request:
#   gemini-3.5-flash      503  — "model is currently experiencing high demand"
#   gemini-3.6-flash      3.7s — tim_thay=True, neo đúng 1 message_id  <- đổi sang cái này
#   gemini-flash-latest   4.8s — sát mốc <5s quá
#   gemini-3.1-flash-lite 1.1s — nhanh nhất  <- CHỐT dùng cái này
# Chốt 3.1-flash-lite sau khi nó là model DUY NHẤT chạy hết được trọn bộ 22 case
# (eval/ket-qua/luot-2.md: 81.8% pass, 0 case bịa nguồn). Model chạy trong Discord
# phải đúng bằng model đã đo, nếu không thì con số ở luot-2.md không nói gì về bot
# đang chạy — và 3.6-flash thì đã cạn 20 lời gọi/ngày ngay trong lượt đo đó.
# Quality bar ở spec §7 KHÔNG đổi theo — bar đã chốt 23:59 N1, model chỉ là phương tiện.
MODEL = "gemini-3.1-flash-lite"          # free tier của Google AI Studio
MAX_TOKENS = 8000
SO_UNG_VIEN = 30                         # FTS5 trả top-N cho LLM chọn

# Free tier Gemini giới hạn theo SỐ LỜI GỌI MỖI PHÚT, không theo token. chay_eval.py
# gọi 22 lần liên tiếp nên phải tự giãn nhịp, nếu không sẽ ăn 429 giữa lượt đo và
# bảng kết quả R4 bị dở dang. 6.5s ≈ 9 lời gọi/phút, nằm dưới hạn 10/phút.
GIAN_CACH_GOI = 6.5                      # giây, giữa hai lời gọi LIỀN NHAU
# Số lần thử lại khi gặp lỗi tạm thời (429 hết hạn mức, 503 model quá tải).
# Backoff = GIAN_CACH_GOI * 2^lần → 13s, 26s, 52s, 104s. Để 5 chứ không phải 3 vì
# 30/07 gặp đợt 503 kéo dài của gemini-3.5-flash: thử 3 lần là bỏ cuộc và hỏng cả
# lượt eval 22 case ngay từ case đầu, phải chạy lại từ đầu.
SO_LAN_THU = 5


def _env(ten: str, mac_dinh: str = "") -> str:
    return os.environ.get(ten, mac_dinh).strip()


DISCORD_TOKEN = _env("DISCORD_TOKEN")
GUILD_ID = _env("GUILD_ID")

# Danh sách kênh được index. Rỗng = mọi kênh bot đọc được.
KENH_INDEX: list[str] = [k.strip() for k in _env("KENH_INDEX").split(",") if k.strip()]

# Kênh mà MỌI tin nhắn của người đều được coi là câu hỏi cho bot (không cần @mention).
# Rỗng = tắt. Đừng đưa 5 kênh ở KENH_INDEX vào đây: đó là kênh thông báo/tài nguyên,
# bật lên thì bot trả lời cả thông báo của LabCoach và đốt hết 20 lời gọi/ngày.
KENH_TU_DONG: list[str] = [k.strip() for k in _env("KENH_TU_DONG").split(",") if k.strip()]


def can_discord() -> str:
    """Gọi ở đầu script cần Discord. Báo lỗi rõ ràng thay vì KeyError."""
    if not DISCORD_TOKEN:
        raise SystemExit(
            "Thiếu DISCORD_TOKEN.\n"
            "  1. cp .env.example .env   (PowerShell: Copy-Item .env.example .env)\n"
            "  2. Điền token từ Developer Portal → tab Bot → Reset Token"
        )
    return DISCORD_TOKEN


def can_gemini() -> str:
    """Gọi ở đầu script cần AI."""
    key = _env("GEMINI_API_KEY")
    if not key:
        raise SystemExit(
            "Thiếu GEMINI_API_KEY trong .env\n"
            "  Lấy key free tại https://aistudio.google.com/apikey"
        )
    return key
