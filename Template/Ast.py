from dataclasses import dataclass
from typing import Any
from Template.AstPattern import PatternItem
from Template.StrPointer import Pointer

@dataclass
class AstDef:
    """
        Name | string -> ast ismi
        Pattern | list[patternItem] -> eşleşme kontrolü için desen
        Priority | int -> eşleşme önceliklendirme
        Lazy | bool -> işleme önceliği
        DLID | bytes -> dll id script yürütme için
        ANID | bytes -> güvenilir bir id
    """
    Name:str
    Pattern:list[PatternItem]
    Priority:int
    IsLazy:bool
    DLID:bytes
    ANID:bytes

    """
        str to Any değer scrapper fonksiyon. ihtiyaç anında eklenecek. entegresi kolay değil. muhtemelen dll'e bağlanacak
    """
    #def _Value(self):

@dataclass
class Ast:
    """
        Name | string -> ast ismi
        Children | dict[int,Ast|LazyAst] -> bağ astlar.
        Value | str -> Ast'ın taşıdığı değer.
        DLID | bytes -> dll id
        ANID | bytes -> bir id 
    """
    Name:str
    """
       mapping aslında ast ağacını haritalandırmak için kullanılacaktı. ancak muhtemelen gerek yok 
    """
    #Mapping:dict[str,int] # ihtiyaç olmayabilir sadece fikir olarak kalsın öngöremedim
    Children:dict[int,Ast|LazyAst]
    Value:Any
    DLID:bytes
    ANID:bytes

@dataclass
class LazyAst:
    """
        ::Açıklama
        işleme önceliğini kontrol edebilmek için bazı bölümleri string olarak saklar ve vakti geldiğinde işler
        ::

        Name | str -> isim
        Pointers | tuple[ptr,ptr] -> aralık işaretcileri
        Value | str -> aralıktaki kaynak kod bloğu
    """
    Name:str
    Pointers:tuple[Pointer,Pointer]
    Value:str