syntax on

"autocmd BufReadPost * if line("'\"")>0 && line("'\"")<=line("$")|exe"normal g'\""|endif
au BufReadPost * if line("'\"") > 0|if line("'\"") <= line("$")|exe("norm '\"")|else|exe "norm $"|endif|endif

set number
set ruler
set cc=80

set autoindent
set smartindent
set cindent

set tabstop=4
"set expandtab
set shiftwidth=2

set hlsearch
set incsearch
set ignorecase
set showmatch

"set list
"set cursorline
"set cursorcolumn

"inoremap ( ()<ESC>i
"inoremap { {}<ESC>i
"inoremap [ []<ESC>i
"inoremap < <><ESC>i

"set background=dark/light
":colorscheme desert
:colorscheme darkblue

