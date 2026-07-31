"""Dựng index từ lịch sử Discord.

    python scripts/backfill.py            # 3000 tin/kênh
    python scripts/backfill.py 500        # giới hạn khác
    python scripts/backfill.py --sach     # XOÁ index.db rồi dựng lại từ đầu

Chạy 1 lần. Sau đó bot tự cập nhật tin mới qua on_message.
Bot đọc được cả tin đăng TRƯỚC khi bot vào server.

CHÚ Ý — mặc định KHÔNG xoá gì. `index.them()` chỉ `DELETE` đúng dòng trùng `id`
(để chạy lại không nhân bản), nên tin cũ trong index vẫn nằm nguyên đó. Chạy
backfill lên một index đang có 20 tin giả của seed_gia.py thì kết quả là 20 tin
giả + N tin thật lẫn lộn, và bot có thể trả về link chết `channels/111/222/...`
ngay giữa lúc demo. Muốn index chỉ còn tin thật thì dùng `--sach`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import discord  # noqa: E402

from timlai import config, index  # noqa: E402
from timlai.bot import tu_discord  # noqa: E402

intents = discord.Intents.default()
intents.message_content = True

SACH = "--sach" in sys.argv
_so = [a for a in sys.argv[1:] if a.isdigit()]     # tách số ra khỏi cờ
MOI_KENH = int(_so[0]) if _so else 3000


class Backfill(discord.Client):
    async def on_ready(self) -> None:
        db = index.mo_db()
        tong = 0
        for guild in self.guilds:
            print(f"SERVER: {guild.name}")
            for ch in guild.text_channels:
                if config.KENH_INDEX and ch.name not in config.KENH_INDEX:
                    continue
                if not ch.permissions_for(guild.me).read_message_history:
                    print(f"  #{ch.name:<22} bỏ qua (thiếu quyền)")
                    continue
                dsach = [
                    tu_discord(m)
                    async for m in ch.history(limit=MOI_KENH)
                    if not m.author.bot and (m.content or m.attachments or m.embeds)
                ]
                n = index.them_nhieu(db, dsach)
                tong += n
                print(f"  #{ch.name:<22} +{n}")
        print(f"\nindex.db: {index.dem(db)} tin nhắn (vừa ghi {tong})")
        if config.KENH_INDEX:
            print(f"Kênh được index: {', '.join(config.KENH_INDEX)}")
        await self.close()


if __name__ == "__main__":
    if SACH and config.DB_PATH.exists():
        # Xoá TRƯỚC khi mở kết nối — mo_db() giữ file, xoá giữa chừng là hỏng.
        config.DB_PATH.unlink()
        print(f"--sach: đã xoá {config.DB_PATH.name}, dựng lại từ đầu\n")
    Backfill(intents=intents).run(config.can_discord())
