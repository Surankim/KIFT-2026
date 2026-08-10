#!/usr/bin/env python3
"""KIFT 2026 - Daniel 8/8 email updates"""

print("Loading index.html...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
print(f"Loaded: {len(html):,} bytes")


def find_card_html(html, tpl_id):
    attr_pos = html.find(f'data-dc-tpl="{tpl_id}"')
    if attr_pos < 0: print(f"  ERROR: tpl={tpl_id} not found"); return None, None
    tag_start = html.rfind("<div", 0, attr_pos)
    if tag_start < 0: print(f"  ERROR: no <div for {tpl_id}"); return None, None
    pos = html.find(">", tag_start) + 1
    depth = 1
    while pos < len(html) and depth > 0:
        lt = html.find("<", pos)
        if lt < 0: break
        chunk = html[lt:lt+10]
        if chunk.startswith("<div") and (len(chunk) < 5 or chunk[4] in " \t\n\r>"):
            depth += 1; pos = html.find(">", lt) + 1
        elif chunk.startswith("</div"):
            depth -= 1
            if depth == 0:
                return tag_start, html.find(">", lt) + 1
            pos = html.find(">", lt) + 1
        else:
            pos = html.find(">", lt) + 1
        if pos <= 0: break
    print(f"  ERROR: no closing tag for tpl={tpl_id}"); return tag_start, None


def replace_leaf(html, tpl_id, val):
    """Replace content of a leaf div by finding tpl_id and replacing text between > and </div>"""
    marker = f'data-dc-tpl="{tpl_id}"'
    pos = html.find(marker)
    if pos < 0:
        print(f"  WARNING: tpl={tpl_id} not found in HTML")
        return html
    tag_end = html.find(">", pos) + 1
    close_pos = html.find("</div>", tag_end)
    if close_pos < 0:
        print(f"  WARNING: no </div> after tpl={tpl_id}")
        return html
    old_content = html[tag_end:close_pos]
    print(f"  tpl={tpl_id}: [{old_content[:30]}] -> [{val[:30]}]")
    return html[:tag_end] + val + html[close_pos:]


ROOT_S = "background: rgb(17, 18, 20); padding: 32px 24px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 16px;"
IMG_S  = "width: 200px; height: 200px;"
NAME_S = "font-family: Pretendard, sans-serif; font-weight: 500; font-size: 18px; line-height: 1.4; letter-spacing: 2px;"
TTL_S  = "font-family: Pretendard, sans-serif; font-weight: 300; font-size: 13px; letter-spacing: 2px; color: rgb(62, 115, 211); margin-top: 4px; line-height: 1.5;"
BIO_S  = "font-family: Pretendard, sans-serif; font-weight: 300; font-size: 13px; line-height: 1.7; color: rgb(168, 173, 178); margin-top: 12px; text-align: left;"
EN_S   = "display: inline;"
KR_S   = "display: none;"


def make_card(t0, sp_id, name, title_en, title_kr, bio_en, bio_kr):
    t = lambda n: t0 + n
    return (
        f'<div data-dc-tpl="{t(0)}" style="{ROOT_S}">'
        f'<image-slot data-dc-tpl="{t(1)}" id="{sp_id}" shape="circle" placeholder="Photo" style="{IMG_S}"></image-slot>'
        f'<div data-dc-tpl="{t(2)}">'
        f'<div data-dc-tpl="{t(3)}" style="{NAME_S}">{name}</div>'
        f'<div data-dc-tpl="{t(4)}" style="{TTL_S}">'
        f'<div data-dc-tpl="{t(5)}" style="{EN_S}">{title_en}</div>'
        f'<div data-dc-tpl="{t(6)}" style="{KR_S}">{title_kr}</div>'
        f'</div>'
        f'<div data-dc-tpl="{t(7)}" style="{BIO_S}">'
        f'<div data-dc-tpl="{t(8)}" style="{EN_S}">{bio_en}</div>'
        f'<div data-dc-tpl="{t(9)}" style="{KR_S}">{bio_kr}</div>'
        f'</div></div></div>'
    )


# --- 1. Session 2 Title ---
print("[1] Session 2 title...")
for old in ["Agentic AI &amp; Physical AI in the Luxury Ecosystem",
            "Agentic AI & Physical AI in the Luxury Ecosystem",
            "Agentic &amp; Physical AI in the Luxury Ecosystem"]:
    c = html.count(old)
    if c:
        new = old.replace("Agentic AI &amp;", "Agentic &amp;").replace("Agentic AI &", "Agentic &").replace("Luxury Ecosystem", "Luxury Fashion Ecosystem").replace("Agentic &amp; Physical AI in the Luxury Ecosystem", "Agentic &amp; Physical AI in the Luxury Fashion Ecosystem")
        html = html.replace(old, new)
        print(f"  {c}x replaced [{old[:40]}]")


# --- 2. Olivia Davis -> Audrey Hansen ---
print("[2] Olivia Davis -> Audrey Hansen...")
AUDREY_EN = "Audrey Hansen is co-founder and CEO of Siren, an AI-powered fashion intelligence platform that helps brands and retailers optimize inventory, pricing, and demand. She leads Siren&#39;s product vision and commercial strategy, working at the intersection of fashion, data science, and artificial intelligence. She brings a founder&#39;s perspective on how technology can transform the operational and creative sides of the fashion industry."
AUDREY_KR = "\uc624\ub4dc\ub9ac \ud55c\uc13c\uc740 AI\ub85c \ud328\uc158 \ube0c\ub79c\ub4dc\uc640 \ub9ac\ud14c\uc77c\ub7ec\uc758 \uc7ac\uace0 \uad00\ub9ac, \uac00\uaca9 \ucc45\uc815, \uc218\uc694 \uc608\uce21\uc744 \ucd5c\uc801\ud654\ud558\ub294 \ud328\uc158 \uc778\ud154\ub9ac\uc804\uc2a4 \ud50c\ub7ab\ud3fc \uc0ac\uc774\ub80c(Siren)\uc758 \uacf5\ub3d9\ucc3d\uc5c5\uc790 \uaca8 \ub300\ud45c\ub2e4. \uc81c\ud488 \ube44\uc804\uacfc \uc0ac\uc5c5 \uc804\ub7b5\uc744 \ucd1d\uad04\ud558\uba70, \ud328\uc158&#183;\ub370\uc774\ud130 \uc0ac\uc774\uc5b8\uc2a4&#183;AI\uac00 \uad50\ucc28\ud558\ub294 \uc9c0\uc810\uc5d0\uc11c \uc77c\ud558\uace0 \uc788\ub2e4. \uae30\uc220\uc774 \ud328\uc158 \uc0b0\uc5c5\uc758 \uc6b4\uc601\uacfc \ucc3d\uc791 \ubc29\uc2dd\uc744 \uc5b4\ub5bb\uac8c \ubc14\uafb8\uc5b8 \uc218 \uc788\ub294\uc9c0\ub97c \uc9c1\uc811 \uad6c\ud604\ud574\uc628 \ucc3d\uc5c5\uac00\ub2e4."
html = replace_leaf(html, "309", "Audrey Hansen")
html = replace_leaf(html, "311", "Co-Founder &amp; CEO, Siren")
html = replace_leaf(html, "312", "Co-Founder &amp; CEO, Siren")
html = replace_leaf(html, "314", AUDREY_EN)
html = replace_leaf(html, "315", AUDREY_KR)


# --- 3. Sunghoon Kang title ---
print("[3] Sunghoon Kang title...")
html = replace_leaf(html, "350", "Co-Founder &amp; CEO, Studio Lab")
html = replace_leaf(html, "351", "\uacf5\ub3d9\ucc3d\uc5c5\uc790 &amp; CEO, Studio Lab")


# --- 4. Move Sunghoon S3 -> S2 ---
print("[4] Moving Sunghoon S3->S2...")
s_start, s_end = find_card_html(html, "345")
if s_start is not None and s_end is not None:
    card = html[s_start:s_end]
    html = html[:s_start] + html[s_end:]
    st_start, st_end = find_card_html(html, "316")
    if st_end:
        html = html[:st_end] + chr(10) + card + html[st_end:]
        print("  OK: moved after Stephan")
    else:
        print("  ERROR: Stephan not found")
else:
    print("  ERROR: Sunghoon not found")


# --- 5. Add Sang-Goo Lee ---
print("[5] Adding Sang-Goo Lee...")
SGL_EN = "Sang-Goo Lee is a professor at Seoul National University and founder and CTO of IntelliSys, an AI research and application company. His work bridges advanced machine learning research and industrial applications, with a focus on intelligent systems and AI integration across the fashion and luxury sectors. He brings both academic rigor and entrepreneurial experience to the intersection of artificial intelligence and the fashion industry."
SGL_KR = "\uc774\uc0c1\uad6c \uad50\uc218\ub294 \uc11c\uc6b8\ub300\ud559\uad50 \uad50\uc218\uc774\uc790 AI \uc5f0\uad6c&#183;\uc751\uc6a9 \uae30\uc5c5 \uc778\ud154\ub9ac\uc2dc\uc2a4(IntelliSys)\uc758 \ucc3d\uc5c5\uc790 \uacb8 \ucd5c\uace0\uae30\uc220\ucc45\uc784\uc790(CTO)\ub2e4. \uc9c0\ub2a5\ud615 \uc2dc\uc2a4\ud15c\uacfc \ud328\uc158&#183;\ub7ed\uc154\ub9ac \ubd84\uc57c AI \uc811\ubaa9\uc744 \uc911\uc2ec\uc73c\ub85c \ucca8\ub2e8 \uba38\uc2e0\ub7ec\ub2dd \uc5f0\uad6c\uc640 \uc0b0\uc5c5 \uc751\uc6a9\uc744 \uc5f0\uacb0\ud558\ub294 \uc5f0\uad6c\ub97c \uc774\uc5b4\uc654\ub2e4. \ud559\ubb38\uc801 \uae4a\uc774\uc640 \ucc3d\uc5c5 \uacbd\ud5d8\uc744 \ubc14\ud0d5\uc73c\ub85c AI\uc640 \ud328\uc158 \uc0b0\uc5c5\uc758 \uc811\uc810\uc744 \ud0d0\uad6c\ud558\uace0 \uc788\ub2e4."
sgl = make_card(400, "sp-13", "Sang-Goo Lee", "Professor, Seoul National University | Founder &amp; CTO, IntelliSys", "\uc11c\uc6b8\ub300\ud559\uad50 \uad50\uc218 | \ucc3d\uc5c5\uc790 &amp; CTO, IntelliSys", SGL_EN, SGL_KR)
s2_start, s2_end = find_card_html(html, "345")
if s2_end is not None:
    html = html[:s2_end] + chr(10) + sgl + html[s2_end:]
    print("  OK: Sang-Goo Lee added")
else:
    print("  ERROR: Sunghoon card not found")


# --- 6. Add Maisa Benatti ---
print("[6] Adding Maisa Benatti...")
MB_EN = "Maisa Benatti is CEO of AIUTA, an AI-powered platform transforming fashion commerce through virtual try-on and digital product visualization. She leads AIUTA&#39;s mission to bridge the physical and digital fashion experience, enabling consumers to visualize clothing before purchasing and helping brands reduce returns while boosting conversion. She brings expertise in fashion technology, consumer experience design, and AI-driven personalization."
MB_KR = "\ub9c8\uc774\uc0ac \ubca0\ub098\ud2f0\ub294 \uac00\uc0c1 \ucc29\uc758(virtual try-on)\uc640 \ub514\uc9c0\ud138 \uc0c1\ud488 \uc2dc\uac01\ud654\uc5d0 \ud2b9\ud654\ub41c AI \ud328\uc158 \ud50c\ub7ab\ud3fc \uc544\uc774\uc6b0\ud0c0(AIUTA)\uc758 \ub300\ud45c\ub2e4. \uc18c\ube44\uc790\uac00 \uad6c\ub9e4 \uc804 \uc637\uc744 \ubbf8\ub9ac \ud655\uc778\ud560 \uc218 \uc788\ub3c4\ub85d \ud574 \ubc18\ud488\uc744 \uc904\uc774\uace0 \uc804\ud658\uc728\uc744 \ub192\uc774\ub294 \uac83\uc744 \ubaa9\ud45c\ub85c, \ud328\uc158 \uc1fc\ud551 \uacbd\ud5d8\uc758 \ub514\uc9c0\ud138 \uc804\ud658\uc744 \uc774\ub04c\uace0 \uc788\ub2e4. \ud328\uc158 \ud14c\ud06c, \uc18c\ube44\uc790 \uacbd\ud5d8 \ub514\uc790\uc778, AI \uae30\ubc18 \uac1c\uc778\ud654 \ubd84\uc57c\uc758 \uc804\ubb38\uc131\uc744 \uac16\ucd94\uace0 \uc788\ub2e4."
mb = make_card(420, "sp-14", "Maisa Benatti", "CEO, AIUTA", "CEO, AIUTA", MB_EN, MB_KR)
h_start, h_end = find_card_html(html, "355")
if h_end is not None:
    html = html[:h_end] + chr(10) + mb + html[h_end:]
    print("  OK: Maisa Benatti added")
else:
    print("  ERROR: Hannah card not found")


print(f"Writing {len(html):,} bytes...")
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done!")
