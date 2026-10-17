from dataclasses import dataclass
from Core.LiqLexer import LexerHeader
from Core.LiqParser import ParserHeader

"""
    derleme anı bellek deposu.
"""

@dataclass
class Box:
    lexerHeader:LexerHeader
    parserHeader:ParserHeader