from Core.LiqLexer import LexerHeader, Lexer
from Template.Request import Request
from Template.StrPointer import Pointer
from Template.Token import TokenDef
import re

h = LexerHeader(Pointer(),"abc",[TokenDef(re.compile("abc"),"Abc",1,"",True,b"ABC")],[],b"")
r = Request("","","CaptureToken",{"Header":h})
t = Lexer.Lex(r)
print(t)
print(h)