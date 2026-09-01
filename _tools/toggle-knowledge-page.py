# -*- coding: utf-8 -*-
"""
知識頁「認識奧剛」的顯示／隱藏切換。

用法（在網站根目錄執行）：
    python _tools/toggle-knowledge-page.py status
    python _tools/toggle-knowledge-page.py hide
    python _tools/toggle-knowledge-page.py show

隱藏時會做三件事，確保網站上不留任何痕跡：
  1. 頁面檔案移到 _drafts/。GitHub Pages 走 Jekyll，底線開頭的
     資料夾不會被發佈，所以該網址會變成 404，不只是沒有連結。
  2. 從所有頁面的導覽列移除「認識奧剛」（實際刪除，不是註解）。
  3. 從 sitemap.xml 移除該網址，避免 Google 繼續嘗試索引。

顯示時完全反向操作。兩個方向都可重複執行，不會產生重複內容。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = 'what-is-orgonite.html'
LIVE = os.path.join(ROOT, PAGE)
HIDDEN_DIR = os.path.join(ROOT, '_drafts')
HIDDEN = os.path.join(HIDDEN_DIR, PAGE)

NAV_PAGES = ['index.html', 'course-trial.html', 'course-advanced-2days.html', PAGE]

NAV_LINE = '                <li><a href="%s" class="nav-link">認識奧剛</a></li>\n' % PAGE
NAV_ANCHOR = '                <li><a href="index.html#about" class="nav-link">關於我們</a></li>\n'
# 首頁的導覽列用的是同頁錨點
NAV_ANCHOR_INDEX = '                <li><a href="#about" class="nav-link">關於我們</a></li>\n'

SITEMAP = os.path.join(ROOT, 'sitemap.xml')
SITEMAP_ENTRY = """    <url>
        <loc>https://lightwithinstudio.tw/%s</loc>
        <lastmod>2026-09-01</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
""" % PAGE
SITEMAP_ANCHOR = '</urlset>'


def read(p):
    return io.open(p, encoding='utf-8').read()


def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)


def page_paths():
    """回傳目前實際存在、需要改導覽列的頁面。"""
    out = []
    for name in NAV_PAGES:
        for cand in (os.path.join(ROOT, name), os.path.join(HIDDEN_DIR, name)):
            if os.path.exists(cand):
                out.append(cand)
                break
    return out


def set_nav(enabled):
    changed = []
    for path in page_paths():
        s = read(path)
        has = NAV_LINE in s
        if enabled and not has:
            anchor = NAV_ANCHOR_INDEX if NAV_ANCHOR_INDEX in s else NAV_ANCHOR
            if anchor not in s:
                raise SystemExit('找不到導覽列插入點：%s' % path)
            s = s.replace(anchor, anchor + NAV_LINE)
            changed.append(os.path.basename(path))
        elif not enabled and has:
            s = s.replace(NAV_LINE, '')
            changed.append(os.path.basename(path))
        else:
            continue
        write(path, s)
    return changed


def set_sitemap(enabled):
    s = read(SITEMAP)
    has = PAGE in s
    if enabled and not has:
        write(SITEMAP, s.replace(SITEMAP_ANCHOR, SITEMAP_ENTRY + SITEMAP_ANCHOR))
        return True
    if not enabled and has:
        s = re.sub(r'    <url>\s*<loc>[^<]*%s</loc>.*?</url>\n' % re.escape(PAGE),
                   '', s, flags=re.S)
        write(SITEMAP, s)
        return True
    return False


def move(to_hidden):
    if to_hidden:
        if not os.path.exists(LIVE):
            return False
        if not os.path.isdir(HIDDEN_DIR):
            os.makedirs(HIDDEN_DIR)
        os.replace(LIVE, HIDDEN)
    else:
        if not os.path.exists(HIDDEN):
            return False
        os.replace(HIDDEN, LIVE)
    return True


def status():
    live = os.path.exists(LIVE)
    hidden = os.path.exists(HIDDEN)
    navs = [os.path.basename(p) for p in page_paths() if NAV_LINE in read(p)]
    in_map = PAGE in read(SITEMAP)
    state = '顯示中' if live else ('已隱藏' if hidden else '檔案不存在')
    print('知識頁狀態：%s' % state)
    print('  頁面位置    : %s' % (PAGE if live else ('_drafts/' + PAGE if hidden else '（找不到）')))
    print('  導覽列連結  : %s' % (', '.join(navs) if navs else '無'))
    print('  sitemap.xml : %s' % ('已收錄' if in_map else '未收錄'))
    if live and hidden:
        print('  ！警告：兩個位置都有檔案，請手動確認')
    return live


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    if cmd == 'status':
        status()
        return
    if cmd not in ('hide', 'show'):
        raise SystemExit('用法：python _tools/toggle-knowledge-page.py [status|hide|show]')

    show = (cmd == 'show')
    # 顯示時先把檔案移回來，導覽列才找得到它；隱藏時先清連結再移走
    if show:
        move(to_hidden=False)
        navs = set_nav(True)
        smap = set_sitemap(True)
    else:
        navs = set_nav(False)
        smap = set_sitemap(False)
        move(to_hidden=True)

    print('已切換為「%s」' % ('顯示' if show else '隱藏'))
    print('  導覽列異動  : %s' % (', '.join(navs) if navs else '無（本來就是這個狀態）'))
    print('  sitemap.xml : %s' % ('已更新' if smap else '無需異動'))
    print()
    status()
    print()
    print('提醒：改完要 commit 並 push 才會反映到線上。')


if __name__ == '__main__':
    main()
