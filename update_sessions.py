#!/usr/bin/env python3
"""Diagnostic: test replace_leaf on tpl 309"""
import sys

print("Loading index.html...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
print(f"Loaded: {len(html):,} bytes")

marker = 'data-dc-tpl="309"'
pos = html.find(marker)
print(f"tpl-309 pos: {pos}")
if pos >= 0:
    tag_end = html.find(">", pos) + 1
    close_pos = html.find("</div>", tag_end)
    old_content = html[tag_end:close_pos]
    print(f"tag_end={tag_end}, close_pos={close_pos}")
    print(f"old_content: [{old_content[:60]}]")
    print(f"ctx_before: [{html[pos-10:pos+30]}]")
else:
    print("ERROR: tpl 309 not found!")
    sys.exit(1)

for tpl in ["311", "312", "314", "350", "355"]:
    m = f'data-dc-tpl="{tpl}"'
    p = html.find(m)
    if p >= 0:
        te = html.find(">", p) + 1
        cp = html.find("</div>", te)
        print(f"tpl-{tpl}: [{html[te:cp][:40]}]")
    else:
        print(f"tpl-{tpl}: NOT FOUND")

new_html = html[:tag_end] + "AUDREY_TEST" + html[close_pos:]
changed = (new_html != html)
print(f"HTML changed: {changed}, new len: {len(new_html)}")
if changed:
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)
    print("Written successfully")
else:
    print("ERROR: no change made")
    sys.exit(1)
