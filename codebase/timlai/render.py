"""Trình bày kết quả. Tách khỏi tra_cuu.py để test được text mà không cần Discord.

Năm đường đi trải nghiệm (rubric R3) nằm hết ở đây, mỗi đường một màu:
    happy          xanh   — tìm thấy, do_tin_cay=cao
    low-confidence vàng   — ② mơ hồ, kèm câu hỏi lại
    failure        xám    — ① không căn cứ
    ngoài phạm vi  đỏ nhạt— ③ user đòi thứ bot không làm
    giới thiệu     tím    — user hỏi về chính bot

KHÔNG dùng tiêu đề embed. Trước đây mỗi đường có một câu tiêu đề ("Không tìm thấy",
"Tìm thấy rồi"…) nằm ngay trên phần mô tả vốn đã nói y hệt như vậy — người đọc phải
đọc cùng một câu hai lần, và câu "Không tìm thấy" in đậm là thứ đập vào mắt trước
tiên dù phần dưới mới là câu trả lời thật. Màu viền đã đủ để phân biệt năm đường.
"""

from __future__ import annotations

from typing import Sequence

from . import config
from .index import TinNhan
from .tra_cuu import KetQua, LinkChon, canh_bao_cu

MAU = {
    "happy": 0x2ECC71,
    "thap": 0xF1C40F,
    "fail": 0x9E9E9E,
    "ngoai": 0xE74C3C,
    "gioi_thieu": 0x5865F2,
}


KHONG_CO_LINK = "⚠️ Tin này không chứa link nào — chỉ có nội dung. Mở tin gốc để xem."
TOI_DA_LINK = 3          # một tin dán 10 link thì cắt bớt, đừng vỡ field 1024 ký tự


def _dong_nguon(tin: TinNhan, da_chon: Sequence[LinkChon] = ()) -> str:
    """Một tin nguồn -> một khối: từng link CÓ NHÃN, rồi tới dòng tin gốc.

    Link bóc từ `noi_dung` đã lưu trong index (`TinNhan.cac_link`), không phải từ
    chữ model viết ra — đó là điều kiện để cái link này đáng tin. Vẫn kèm jump_url
    để học viên tự mở tin gốc mà kiểm (nguyên tắc G11 ở spec §4b).

    Nhãn là thứ quyết định output có đọc được không. Một tin liệt kê link chấm chéo
    cho K3 và K4 mà in ra hai URL trần thì user không biết bấm cái nào — mà hai URL
    đó dài 90 ký tự và chỉ khác nhau ở giữa. Nên: nhãn trước, link sau, mỗi link
    một khối.
    """
    tat_ca = tin.cac_link()
    cua_tin_nay = [lc for lc in da_chon if lc.url in tat_ca]

    if cua_tin_nay:
        phan = [f"**{lc.nhan}**\n{lc.url}" for lc in cua_tin_nay]
        con = len(tat_ca) - len(cua_tin_nay)
        if con:
            # Vẫn nói cho user biết tin gốc còn link khác — nhỡ bot chọn nhầm cái.
            phan.append(f"_(tin gốc còn {con} link khác)_")
    elif tat_ca:
        # Model không chọn được link nào -> đổ ra, nhưng có trần để khỏi vỡ field.
        phan = [f"🔗 {u}" for u in tat_ca[:TOI_DA_LINK]]
        if len(tat_ca) > TOI_DA_LINK:
            phan.append(f"…và {len(tat_ca) - TOI_DA_LINK} link nữa trong tin gốc")
    else:
        # G4: tin được chọn nhưng không có link nào. Nói thẳng, đừng để học viên
        # tưởng bot đưa link rồi bấm vào tên kênh.
        phan = [KHONG_CO_LINK]

    ngay = tin.ngay_ngan()
    phan.append(f"↪ [#{tin.kenh} · {tin.tac_gia}{' · ' + ngay if ngay else ''}]({tin.url})")
    if (cb := canh_bao_cu(tin)) :
        phan.append(f"⚠️ {cb}")
    return "\n".join(phan)


VLEARN = (
    "📚 **Slide lý thuyết nằm trên VLearn**, không đăng trong Discord:\n"
    f"{config.LINK_VLEARN}\n"
    "_(link cố định của khoá — không phải kết quả tìm trong tin nhắn)_"
)
"""Dòng chỉ đường sang VLearn. Nói rõ "link cố định" là bắt buộc, không phải cho đẹp:
mọi link khác trong câu trả lời đều được bóc ra từ một tin nhắn có thật và neo lại
được, còn link này thì không — nó là hằng số trong `config.py`. Hai loại link đó phải
phân biệt được bằng mắt, nếu không thì lời hứa "mọi link đều truy được về tin gốc"
là lời hứa suông."""


def thanh_text(kq: KetQua, nguon: list[TinNhan]) -> str:
    """Bản text thuần — dùng cho test và cho scripts/chay_eval.py."""
    phan = [kq.cau_tra_loi]
    if kq.moc_ngay:
        phan.append(f"🗓 {kq.moc_ngay}")
    if kq.can_lam_ro:
        phan.append(f"❓ {kq.can_lam_ro}")
    if kq.goi_y_vlearn:
        phan.append(VLEARN)
    for tin in nguon:
        phan.append(_dong_nguon(tin, kq.link_chon))
    return "\n\n".join(phan)


def chon_nguon(kq: KetQua, ung_vien: list[TinNhan]) -> list[TinNhan]:
    """Lấy đúng các TinNhan mà AI đã neo, giữ nguyên thứ tự AI chọn.

    G3 — từ chối thì không được trích nguồn. Một câu trả lời "mình không tìm thấy"
    hoặc "ngoài phạm vi" mà bên dưới vẫn liệt kê link là tự mâu thuẫn: học viên
    đọc lướt sẽ bấm vào link và tưởng đó là câu trả lời. Ngoại lệ duy nhất là khi
    bot đang HỎI LẠI (can_lam_ro) — lúc đó danh sách link chính là các lựa chọn.

    Phần giới thiệu cũng không trích nguồn: nó nói về bot, không trả lời câu hỏi
    tài liệu nào, nên mọi link kèm theo đều là link lạc.
    """
    if kq.gioi_thieu or kq.ngoai_pham_vi or (not kq.tim_thay and not kq.can_lam_ro):
        return []
    theo_id = {t.id: t for t in ung_vien}
    return [theo_id[i] for i in kq.message_ids if i in theo_id]


def embed_loi(loi: Exception):
    """G7 — gọi AI hỏng thì nói cho user biết, đừng im lặng.

    Hay gặp nhất là 429 hết hạn mức free tier (20 lời gọi/ngày/model). Không im
    lặng, cũng không đổ nguyên traceback ra kênh chung — chỉ tên lỗi + một dòng.
    """
    import discord

    return discord.Embed(
        description=(
            "Mình đang không trả lời được — lời gọi AI thất bại, có thể hết hạn mức "
            "trong ngày hoặc mạng lỗi. Bạn thử lại sau vài phút nhé.\n"
            f"`{type(loi).__name__}: {str(loi)[:150]}`"
        ),
        color=MAU["fail"],
    )


def _mau(kq: KetQua) -> int:
    """Một đường đi -> một màu viền. Đây là thứ DUY NHẤT phân biệt các đường sau khi
    bỏ tiêu đề, nên đừng để hai đường dùng chung một màu."""
    if kq.gioi_thieu:
        return MAU["gioi_thieu"]
    if kq.ngoai_pham_vi:
        return MAU["ngoai"]
    if not kq.tim_thay:
        return MAU["fail"]
    return MAU["thap"] if kq.do_tin_cay == "thap" else MAU["happy"]


def thanh_embed(kq: KetQua, nguon: list[TinNhan], bo_di: list[str], so_tin: int | None = None):
    """Embed Discord. Import discord trong hàm -> test không cần discord.py.

    `so_tin` = số tin nhắn đang có trong index, chỉ dùng cho phần giới thiệu: bot nói
    về mình thì phải nói được nó đang theo dõi bao nhiêu tin và chạy model nào
    (G2 — làm rõ nó làm tốt đến đâu). Đường khác truyền None và không hiện gì.
    """
    import discord

    # Không set title: câu tiêu đề chỉ lặp lại đúng thứ mô tả bên dưới đã nói.
    e = discord.Embed(description=kq.cau_tra_loi[:4000], color=_mau(kq))

    if kq.moc_ngay:
        # G11 — nói ra bot đã hiểu "hôm qua" thành ngày nào. Hiểu sai mà im thì user
        # chỉ thấy "không tìm thấy" và tưởng tài liệu chưa được đăng.
        e.add_field(name="🗓 Mốc thời gian", value=kq.moc_ngay[:1024], inline=False)

    if kq.can_lam_ro:
        e.add_field(name="❓ Cho mình hỏi lại", value=kq.can_lam_ro[:1024], inline=False)

    if kq.goi_y_vlearn:
        e.add_field(name="Slide lý thuyết", value=VLEARN[:1024], inline=False)

    if nguon:
        e.add_field(
            # Tên field KHÔNG mở đầu bằng 🔗: mỗi dòng link bên dưới cũng bắt đầu
            # bằng emoji thì user đọc lướt tưởng tên field cũng là một cái link.
            name="Link tài liệu",
            value="\n\n".join(_dong_nguon(t, kq.link_chon) for t in nguon)[:1024],
            inline=False,
        )

    if bo_di:
        # Không che số đo hallucination — hiện luôn cho người dùng và cho giám khảo.
        e.set_footer(text=f"Đã bỏ {len(bo_di)} kết luận không neo được vào tin nhắn thật.")
    elif kq.gioi_thieu and so_tin is not None:
        e.set_footer(text=f"Đang theo dõi {so_tin} tin nhắn · model {config.MODEL}")
    return e
