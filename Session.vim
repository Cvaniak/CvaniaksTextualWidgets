let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/OpenSource/CvaniaksTextualWidgets/ck_widgets/widgets
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +94 ~/OpenSource/CvaniaksTextualWidgets/main.py
badd +197 ~/OpenSource/CvaniaksTextualWidgets/ck_widgets/widgets/value_bar.py
badd +70 ~/.local/lib/python3.8/site-packages/rich/panel.py
badd +356 ~/.local/lib/python3.8/site-packages/rich/color.py
badd +44 ~/OpenSource/CvaniaksTextualWidgets/ck_widgets/color/color_tools.py
badd +19 ~/.local/lib/python3.8/site-packages/rich/align.py
badd +42 ~/.local/lib/python3.8/site-packages/rich/text.py
badd +32 ~/.local/lib/python3.8/site-packages/textual/reactive.py
badd +1 ~/OpenSource/CvaniaksTextualWidgets/ck_widgets/color/__init__.py
badd +2 ~/OpenSource/CvaniaksTextualWidgets/ck_widgets/widgets/__init__.py
badd +1 ~/OpenSource/CvaniaksTextualWidgets/ck_widgets/widgets/debug_window.py
badd +147 /usr/lib/python3.8/__future__.py
badd +41 ~/.local/lib/python3.8/site-packages/rich/repr.py
argglobal
%argdel
edit ~/OpenSource/CvaniaksTextualWidgets/ck_widgets/color/color_tools.py
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
vsplit
wincmd _ | wincmd |
vsplit
2wincmd h
wincmd w
wincmd w
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 31 + 105) / 211)
exe 'vert 2resize ' . ((&columns * 73 + 105) / 211)
exe 'vert 3resize ' . ((&columns * 105 + 105) / 211)
argglobal
enew
file ~/OpenSource/CvaniaksTextualWidgets/NERD_tree_1
balt ~/OpenSource/CvaniaksTextualWidgets/main.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal nofen
wincmd w
argglobal
balt ~/OpenSource/CvaniaksTextualWidgets/main.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 43 - ((24 * winheight(0) + 27) / 54)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 43
normal! 06|
wincmd w
argglobal
if bufexists("~/OpenSource/CvaniaksTextualWidgets/ck_widgets/widgets/value_bar.py") | buffer ~/OpenSource/CvaniaksTextualWidgets/ck_widgets/widgets/value_bar.py | else | edit ~/OpenSource/CvaniaksTextualWidgets/ck_widgets/widgets/value_bar.py | endif
if &buftype ==# 'terminal'
  silent file ~/OpenSource/CvaniaksTextualWidgets/ck_widgets/widgets/value_bar.py
endif
balt ~/OpenSource/CvaniaksTextualWidgets/ck_widgets/color/color_tools.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 23 - ((22 * winheight(0) + 27) / 54)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 23
normal! 036|
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 31 + 105) / 211)
exe 'vert 2resize ' . ((&columns * 73 + 105) / 211)
exe 'vert 3resize ' . ((&columns * 105 + 105) / 211)
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToOFcI
let &winminheight = s:save_winminheight
let &winminwidth = s:save_winminwidth
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
