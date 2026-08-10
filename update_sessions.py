#!/usr/bin/env python3
"""
KIFT 2026 Microsite Update Script - Daniel 8/8 email changes
"""
import re

print("Loading index.html...")
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
print(f"File loaded: {len(html):,} bytes")


def find_card_html(html, tpl_id):
    pattern = f'data-dc-tpl="{tpl_id}"'
    attr_pos = html.find(pattern)
    if attr_pos < 0:
        print(f"  ERROR: tpl={tpl_id} not found"); return None, None
    tag_start = html.rfind('<div', 0, attr_pos)
    if tag_start < 0:
        print(f"  ERROR: no <div for tpl={tpl_id}"); return None, None
    open_end = html.find('>', tag_start) + 1
    pos = open_end; depth = 1
    while pos < len(html) and depth > 0:
        lt = html.find('<', pos)
        if lt < 0: break
        chunk = html[lt:lt+10]
        if chunk.startswith('<div') and (len(chunk) < 5 or chunk[4] in ' \t\n\r>'):
            depth += 1; pos = html.find('>', lt) + 1
        elif chunk.startswith('</div'):
            depth -= 1
            if depth == 0:
                close_gt = html.find('>', lt); return tag_start, close_gt + 1
            pos = html.find('>', lt) + 1
        else:
            pos = html.find('>', lt) + 1
        if pos <= 0: break
    print(f"  ERROR: no closing </div> for tpl={tpl_id}"); return tag_start, None


def replace_leaf(html, tpl_id, new_content):
    pattern = rf'(<div[^>]*data-dc-tpl="{tpl_id}"[^>]*>)[^<]*(</div>)'
    new_html = re.sub(pattern, r'\g<1>' + new_content.replace('\\', '\\\\') + r'\g<2>', html, count=1)
    if new_html == html: print(f"  WARNING: tpl={tpl_id} unchanged")
    return new_html


CARD_STYLES = {
    'root':  'background: rgb(17, 18, 20); padding: 32px 24px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 16px;',
    'img':   'width: 200px; height: 200px;',
    'name':  'font-family: Pretendard, sans-serif; font-weight: 500; font-size: 18px; line-height: 1.4; letter-spacing: 2px;',
    'title': 'font-family: Pretendard, sans-serif; font-weight: 300; font-size: 13px; letter-spacing: 2px; color: rgb(62, 115, 211); margin-top: 4px; line-height: 1.5;',
    'bio':   'font-family: Pretendard, sans-serif; font-weight: 300; font-size: 13px; line-height: 1.7; color: rgb(168, 173, 178); margin-top: 12px; text-align: left;',
    'en':    'display: inline;',
    'kr':    'display: none;',
}

def make_card(t0, sp_id, name, title_en, title_kr, bio_en, bio_kr):
    t = lambda n: t0 + n
    cs = CARD_STYLES
    return (
        f'<div data-dc-tpl="{t(0)}" style="{cs[\'root\']}">'
        f'<image-slot data-dc-tpl="{t(1)}" id="{sp_id}" shape="circle" placeholder="Photo" style="{cs[\'img\']}"></image-slot>'
        f'<div data-dc-tpl="{t(2)}">'
        f'<div data-dc-tpl="{t(3)}" style="{cs[\'name\']}">{name}</div>'
        f'<div data-dc-tpl="{t(4)}" style="{cs[\'title\']}">'
        f'<div data-dc-tpl="{t(5)}" style="{cs[\'en\']}">{title_en}</div>'
        f'<div data-dc-tpl="{t(6)}" style="{cs[\'kr\']}">{title_kr}</div>'
        f'</div>'
        f'<div data-dc-tpl="{t(7)}" style="{cs[\'bio\']}">'
        f'<div data-dc-tpl="{t(8)}" style="{cs[\'en\']}">{bio_en}</div>'
        f'<div data-dc-tpl="{t(9)}" style="{cs[\'kr\']}">{bio_kr}</div>'
        f'</div></div></div>'
    )


# 1. Session 2 Title
print("[1] Updating Session 2 title...")
for old in ['Agentic AI &amp; Physical AI in the Luxury Ecosystem', 'Agentic AI & Physical AI in the Luxury Ecosystem']:
    c = html.count(old)
    if c:
        new = old.replace('Agentic AI &amp;', 'Agentic &amp;').replace('Agentic AI &', 'Agentic &').replace('Luxury Ecosystem', 'Luxury Fashion Ecosystem')
        html = html.replace(old, new); print(f"  {c}x: {old[:50]}")


# 2. Olivia Davis => Audrey Hansen
print("[2] Replacing Olivia Davis => Audrey Hansen...")
AUDREY_EN = ("Audrey Hansen is co-founder and CEO of Siren, an AI-powered fashion intelligence platform that helps brands and retailers optimize inventory, pricing, and demand. She leads Siren&#39;s product vision and commercial strategy, working at the intersection of fashion, data science, and artificial intelligence. She brings a founder&#39;s perspective on how technology can transform the operational and creative sides of the fashion industry.")
AUDREY_KR = ("오드리 한센은 AI로 패션 브랜드와 리테일러의 재고 관리, 가격 책정, 수요 예측을 최적화하는 패션 인텔리전스 플랫폼 사이렌(Siren)의 공동창업자 겸 대표다. 제품 비전과 사업 전략을 총괄하며, 패션&#183;데이터 사이언스&#183;AI가 교차하는 지점에서 일하고 있다. 기술이 패션 산업의 운영과 창작 방식을 어떻게 바꿀 수 있는지를 직접 구현해온 창업가다.")
html = replace_leaf(html, '309', 'Audrey Hansen')
html = replace_leaf(html, '311', 'Co-Founder &amp; CEO, Siren')
html = replace_leaf(html, '312', 'Co-Founder &amp; CEO, Siren')
html = replace_leaf(html, '314', AUDREY_EN)
html = replace_leaf(html, '315', AUDREY_KR)


# 3. Sunghoon Kang title
print("[3] Updating Sunghoon Kang title...")
html = replace_leaf(html, '350', 'Co-Founder &amp; CEO, Studio Lab')
html = replace_leaf(html, '351', '공동창업자 &amp; CEO, Studio Lab')


# 4. Move Sunghoon S3 => S2
print("[4] Moving Sunghoon Kang S3 => S2...")
s_start, s_end = find_card_html(html, '345')
if s_start is not None and s_end is not None:
    card = html[s_start:s_end]
    html = html[:s_start] + html[s_end:]
    st_start, st_end = find_card_html(html, '316')
    if st_end:
        html = html[:st_end] + chr(10) + card + html[st_end:]
        print("  OK: moved after Stephan Heller")
    else:
        print("  ERROR: Stephan not found")
else:
    print("  ERROR: Sunghoon not found")


# 5. Add Sang-Goo Lee
print("[5] Adding Sang-Goo Lee to S2...")
SGL_EN = ("Sang-Goo Lee is a professor at Seoul National University and founder and CTO of IntelliSys, an AI research and application company. His work bridges advanced machine learning research and industrial applications, with a focus on intelligent systems and AI integration across the fashion and luxury sectors. He brings both academic rigor and entrepreneurial experience to the intersection of artificial intelligence and the fashion industry.")
SGL_KR = ("이상구 교수는 서울대학교 교수이자 AI 연구&#183;응용 기업 인텔리시스(IntelliSys)의 창업자 겸 최고기술책임자(CTO)다. 지능형 시스템과 패션&#183;럭셔리 분야 AI 접목을 중심으로 첨단 머신러닝 연구와 산업 응용을 연결하는 연구를 이어왔다. 학문적 깊이와 창업 경험을 바탕으로 AI와 패션 산업의 접점을 탐구하고 있다.")
sgl_card = make_card(400, 'sp-13', 'Sang-Goo Lee', 'Professor, Seoul National University | Founder &amp; CTO, IntelliSys', '서울대학교 교수 | 창업자 &amp; CTO, IntelliSys', SGL_EN, SGL_KR)
s2_start, s2_end = find_card_html(html, '345')
if s2_end is not None:
    html = html[:s2_end] + chr(10) + sgl_card + html[s2_end:]
    print("  OK: Sang-Goo Lee added")
else:
    print("  ERROR: Sunghoon card not found for insertion")


# 6. Add Maisa Benatti
print("[6] Adding Maisa Benatti to S3...")
MB_EN = ("Maisa Benatti is CEO of AIUTA, an AI-powered platform transforming fashion commerce through virtual try-on and digital product visualization. She leads AIUTA&#39;s mission to bridge the physical and digital fashion experience, enabling consumers to visualize clothing before purchasing and helping brands reduce returns while boosting conversion. She brings expertise in fashion technology, consumer experience design, and AI-driven personalization.")
MB_KR = ("마이사 베나티는 가상 착의(virtual try-on)와 디지털 상품 시각화에 특화된 AI 패션 플랫폼 아이우타(AIUTA)의 대표다. 소비자가 구매 전 옷을 미리 확인할 수 있도록 해 반품을 줄이고 전환율을 높이는 것을 목표로, 패션 쇼핑 경험의 디지털 전환을 이끌고 있다. 패션 테크, 소비자 경험 디자인, AI 기반 개인화 분야의 전문성을 갖추고 있다.")
mb_card = make_card(420, 'sp-14', 'Maisa Benatti', 'CEO, AIUTA', 'CEO, AIUTA', MB_EN, MB_KR)
h_start, h_end = find_card_html(html, '355')
if h_end is not None:
    html = html[:h_end] + chr(10) + mb_card + html[h_end:]
    print("  OK: Maisa Benatti added")
else:
    print("  ERROR: Hannah card not found")


print(f"Writing {len(html):,} bytes...")
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done!")
