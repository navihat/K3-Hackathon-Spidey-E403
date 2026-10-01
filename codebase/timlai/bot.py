"""Lớp ① — Discord.

    python -m timlai.bot

Chỉ làm 3 việc: nhận câu hỏi, gọi lớp ② rồi lớp ③, render kết quả.
Mọi logic quyết định nằm ở tra_cuu.py — nhờ vậy test được ngoài Discord.

HAI ĐƯỜNG VÀO, cùng một hàm xử lý (`hoi`):
  1. @mention bot             — gõ tự nhiên trong kênh, không cần nhớ lệnh
  2. reply vào tin của bot    — đường "correction" ở spec §6, hỏi lại không cần gõ lệnh
Thêm chế độ opt-in: mọi tin trong kênh thuộc KENH_TU_DONG đều được coi là câu hỏi.

Câu trả lời hiện **công khai** (ai trong kênh cũng thấy), không còn ephemeral.
"""

from __future__ import annotations

import asyncio
import re

import discord

from . import config, index, render, tra_cuu

intents = discord.Intents.default()
intents.message_content = True   # ★ phải bật CẢ ở đây VÀ ở Developer Portal


class Bot(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=intents)
        self.db = index.mo_db()

    async def on_ready(self) -> None:
        print(f"online: {self.user} · index có {index.dem(self.db)} tin nhắn")

    async def on_message(self, msg: discord.Message) -> None:
        """Hai việc: nạp tin mới vào index, và trả lời nếu tin đó là câu hỏi cho bot.

        Bỏ qua mọi tin của bot (kể cả của chính mình) ngay từ dòng đầu — đó là thứ
        duy nhất chặn vòng lặp bot trả lời bot.
        """
        if msg.guild is None or msg.author.bot:
            return

        # ① Nạp index. Tin mới có mặt ngay, khỏi chạy lại backfill.
        if not config.KENH_INDEX or msg.channel.name in config.KENH_INDEX:
            index.them_nhieu(self.db, [tu_discord(msg)])

        # ② Trả lời nếu được hỏi. Câu trả lời của bot là tin của bot nên không
        #    quay lại vòng này, và cũng không lọt vào index.
        cau_hoi = self.cau_hoi_cho_bot(msg)
        if cau_hoi is None:
            return
        async with msg.channel.typing():
            embed = await hoi(self.db, cau_hoi)
        await msg.reply(embed=embed, mention_author=False, allowed_mentions=KHONG_PING)

    def cau_hoi_cho_bot(self, msg: discord.Message) -> str | None:
        """Tin này có phải câu hỏi gửi cho bot không? Trả câu hỏi đã làm sạch, hoặc None.

        Ba cửa, xếp theo mức độ chắc chắn user đang nói với bot:
          1. @mention bot          — chắc chắn nhất
          2. reply vào tin của bot — đường correction ở spec §6
          3. kênh trong KENH_TU_DONG — mọi tin đều là câu hỏi (opt-in, mặc định TẮT)

        Cửa 3 mặc định tắt là có lý do: 5 kênh được index là kênh thông báo và tài
        nguyên. Bật nó ở đó thì bot trả lời cả thông báo của LabCoach — vừa nhiễu,
        vừa đốt hạn mức (free tier chỉ 20 lời gọi/ngày/model).
        """
        if self.user in msg.mentions:
            # Trả cả chuỗi RỖNG (mention trống, "@Spidey" một mình): trước đây bot
            # im lặng, mà im lặng thì người mới không biết bot còn sống hay không.
            # Chuỗi rỗng đi tiếp và ra phần giới thiệu — vẫn không tốn lời gọi AI.
            return _bo_mention(msg.content, self.user.id)

        tra_loi_cho = msg.reference.resolved if msg.reference else None
        if isinstance(tra_loi_cho, discord.Message) and tra_loi_cho.author.id == self.user.id:
            return msg.content.strip() or None

        if msg.channel.name in config.KENH_TU_DONG:
            noi_dung = msg.content.strip()
            if tra_cuu.la_hoi_ve_bot(noi_dung) and noi_dung:
                return noi_dung          # "hi", "help" — trả lời được mà không tốn AI
            # Chặn "ok", "vâng", ":D"... — mỗi tin lọt qua đây là một lời gọi AI.
            return noi_dung if len(noi_dung) >= 5 else None

        return None


_MENTION = re.compile(r"<@!?(\d+)>")


def _bo_mention(noi_dung: str, uid: int) -> str:
    """Bỏ phần @mention bot khỏi câu hỏi.

    Hàm thuần, không đụng discord -> test được offline. Discord gửi mention dưới
    hai dạng `<@id>` và `<@!id>` (dạng có dấu ! là nickname), phải bắt cả hai.
    """
    return _MENTION.sub(lambda m: "" if m.group(1) == str(uid) else m.group(0), noi_dung).strip()


KHONG_PING = discord.AllowedMentions.none()
"""G6 — nội dung tin nhắn trong index là do người khác viết và có thể chứa
`@everyone`. Bot echo lại nội dung đó, nên nếu không chặn thì một tin cũ có thể
biến câu trả lời của bot thành cú ping toàn server."""


async def hoi(db, cau_hoi: str) -> discord.Embed:
    """Một câu hỏi -> một embed. Điểm chung của cả ba đường vào.

    Chia việc theo đúng thứ chậm: truy xuất FTS5 chạy NGAY trên event loop (query
    SQLite local, micro giây), chỉ lời gọi Gemini (1-4s) mới đẩy sang thread khác.

    Đừng gộp cả hàm vào asyncio.to_thread: sqlite3 chỉ cho dùng connection trong
    đúng thread đã tạo ra nó, gộp vào là ném ProgrammingError ngay ở câu hỏi đầu
    tiên ("SQLite objects created in a thread can only be used in that same thread").
    """
    ung_vien = index.truy_xuat(db, cau_hoi)
    try:
        kq, bo_di = await asyncio.to_thread(tra_cuu.tra_cuu, cau_hoi, ung_vien)
    except Exception as e:                      # G7: hết hạn mức / mạng chết
        print(f"[loi] {type(e).__name__}: {e}")
        return render.embed_loi(e)
    # dem() chỉ chạy khi thật sự cần in ra — nó quét cả bảng FTS5.
    so_tin = index.dem(db) if kq.gioi_thieu else None
    return render.thanh_embed(kq, render.chon_nguon(kq, ung_vien), bo_di, so_tin=so_tin)


bot = Bot()


def tu_discord(m: discord.Message) -> index.TinNhan:
    """Message của discord.py -> TinNhan của mình.

    Gộp cả tên file đính kèm: 84% người khảo sát tìm SLIDE, mà slide thường là
    file .pdf đính kèm chứ không phải URL trong text. Không index tên file là
    mất phần lớn kết quả.
    """
    them = [a.filename for a in m.attachments]
    them += [e.title or "" for e in m.embeds]
    them += [e.url or "" for e in m.embeds]
    return index.TinNhan(
        id=str(m.id),
        kenh=getattr(m.channel, "name", "?"),
        tac_gia=m.author.display_name,
        thoi_diem=m.created_at.isoformat(),
        url=m.jump_url,
        noi_dung=" ".join([m.content, *filter(None, them)]).strip(),
    )


if __name__ == "__main__":
    bot.run(config.can_discord())
