These are some experimenting code to hack together a browser from ground up. 

I write my code in MyDef, a meta layer. The code is still in Python; MyDef just let me use macros and rearainge code for better reading and easier writing (or just to be lazy and keep my old habits). You don't have to know MyDef to follow, try read test.py, which is compiled from parse_html.def. It is a very simple HTML parser. You may test it by `python test.py`, which will parse `test.html` into a dom tree. 

parse_tyle.def parses CSS style sheets.

parse_script.def parses Javascript into abstract syntax tree.
