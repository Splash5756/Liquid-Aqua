from dataclasses import dataclass
from re import Pattern
from Template.LexerMode import Mode

@dataclass
class TokenDef:
    """
    Regex -> re.compile | eşleşme için
    Name -> string | oluşturulacak tokene aktarılacak isim
    Priority -> int | tokenin öncelik numarası
    Mode -> bytes | lexer moduna erişim idsi
    Emit -> bool | tokenin işlenip işlenmeyeceğini belirtir
    ANID -> bytes | token erişimi için oluşturulan güvenilir bir id   
    """
    Regex:Pattern
    Name:str
    Priority:int
    Mode:bytearray|str|Mode
    Emit:bool
    ANID:bytearray

@dataclass
class Token:
    """
    Name -> string | eşleşme ismi
    Value -> string | eşleşen değer
    Pointers -> tuple(Pointers) | eşleşen değerin başlangıç ve son işaretçileri
    ANID -> Bytes | güvenilir bir id
    """
    Name:str
    Value:str
    Pointers:tuple[str,str]
    ANID:bytearray

"""
    if you read this you'll listen Duman(turkish rock group)
"""