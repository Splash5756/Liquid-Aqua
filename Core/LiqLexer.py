from dataclasses import dataclass
from Template.Token import Token, TokenDef
from Template.StrPointer import Pointer
from Template.LexerMode import Mode
from Template.Request import Request
from Template.Exceptions import UnkownRequest

@dataclass
class LexerHeader:
    """
        lexerin bellek alanı. dosya spesifik olacağı için ayrı tutuluyor.

        Ptr -> son kalınan yeri işaret eden işaretçi
        Source -> string tipte kaynak kod
        TokenList -> Token tanımlarını içeren liste
        ModeList -> Lexer davranış Scriptlerini içeren liste
    """
    Ptr:Pointer
    Source:str
    TokenList:list[TokenDef]
    ModeList:list[Mode]

class Lexer:
    @staticmethod
    def Lex(request:Request):
        match(request.Request):
            case "CaptureToken":
                """
                    
                """
                pass
            case "LookAhead":
                pass
            case _:
                raise UnkownRequest(request)
        pass