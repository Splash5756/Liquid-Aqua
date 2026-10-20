from dataclasses import dataclass
from Template.Token import Token, TokenDef
from Template.StrPointer import Pointer
from Template.LexerMode import Mode
from Template.Request import Request
from Template.Exceptions import General as GeneralExceptions
from Template.Exceptions import Lexer as LexerExceptions

"""
    hatırlatma!!! dosyada eksik var. LexerMode yani Lexer davranışları işlenmiyor. bunu en son entegre et.
    detaylar için _Match fonksiyonuna bak
"""

@dataclass
class LexerHeader:
    """
        lexerin bellek alanı. dosya spesifik olacağı için ayrı tutuluyor.

        Ptr -> son kalınan yeri işaret eden işaretçi
        Source -> string tipte kaynak kod
        TokenList -> Token tanımlarını içeren liste
        ModeList -> Lexer davranış Scriptlerini içeren liste
        BoxID -> HataAyıklamak için BoxID
    """
    Ptr:Pointer
    Source:str
    TokenList:list[TokenDef]
    ModeList:list[Mode]
    BoxID:bytes

class Lexer:
    @staticmethod
    def Lex(request:Request):
        if not "Header" in request.Payload:
            raise GeneralExceptions.UnexpectedRequestPayload(request,"Header",LexerHeader,None)

        if type(request.Payload["Header"]) != LexerHeader:
            raise GeneralExceptions.UnexpectedRequestPayload(request,"Header",LexerHeader,request.Payload["Header"])

        _xResultRequest = None
        match(request.Request):
            case "CaptureToken":
                """
                    Token alır ve işaretciyi hizalar
                """
                result = Lexer._Match(request.Payload["Header"])
                if (type(result) != dict) or (not result["Result"] in ["TokenEmitted","TokenNotEmitted"]):
                    raise GeneralExceptions.UnexpectedException(Lexer.Lex,f"dosya : {__file__}, Sınıf : {Lexer}, Fonksiyon : {Lexer.Lex}",f"Durum : {Lexer._Match} hatalı sonuç döndü.",f"Bellek Dökümü :\n\t{id(request)}.{request}\n\t{id(_xResultRequest)}.{_xResultRequest}\n\t{id(result)}.{result}")
                _xResultRequest = Request("Lexer","Parser","Result",{"Job":request.Request,"Result":result["Result"],"Item":result["Payload"]})
                if type(result["Payload"]) == Token:
                    request.Payload["Header"].Ptr = result["Payload"].Pointers[1]
                elif type(result["Payload"]) == tuple:
                    request.Payload["Header"].Ptr = result["Payload"][1]
            case "LookAhead":
                """
                    sadece token döndürür işaretciyi hizalamaz. sonraki tokeni kontrol etmek için elverişlidir.
                """
                result = Lexer._Match(request.Payload["Header"])
                if not result["Result"] in ["TokenEmitted","TokenNotEmitted"]:
                    #unexpected
                    raise
                _xResultRequest = Request("Lexer","Parser","Result",{"Job":request.Request,"Result":result["Result"],"Item":result["Payload"]})
            case _:
                raise GeneralExceptions.UnexpectedRequest(request)

        if type(_xResultRequest) == Request:
            return _xResultRequest

        raise GeneralExceptions.UnexpectedException(Lexer.Lex,f"dosya : {__file__}, Sınıf : {Lexer}, Fonksiyon : {Lexer.Lex}",f"Durum : _xResultRequest {type(_xResultRequest)} döndü. Beklenen değer {Request} idi",f"Bellek Dökümü :\n\t{id(request)}.{request}\n\t{id(_xResultRequest)}.{_xResultRequest}")

    @staticmethod
    def _Match(
        header:LexerHeader
    ) -> dict[str,str|Token|tuple[Pointer,Pointer]]:
        """
            Kaynak kodda kaldığı yerden token döndürür
        """

        """
            !!hatırlatma!!
            varsayılan davranış akışını iptal etmek için eşleşme algoritmasında değişikliğe gitmen gerekli. şuan sadece regex eşleştirip geçiyoruz. ancak ek özellikler ekleyebilmek için dll sisteminin oturması gerekli
            yapıyı bozmadan bakım yapmak için regex hesaplamalarının yapıldığı bölüme bak
        """

        # kaynak kodu kırp
        _xSource = header.Source[header.Ptr.raw:]

        # token listesini önceliğe göre bellekte yeniden hesapla
        _xTokenList = {}
        for t in header.TokenList:
            if not t.Priority in _xTokenList:
                _xTokenList[t.Priority] = []

            _xTokenList[t.Priority].append(t)

        # en son öncelikten en az önceliğe kadar eşleşme dene
        _xKeylist = list(_xTokenList.keys())
        _xKeylist.sort(reverse=True)
        _xMatches = {}
        for l in _xKeylist:
            for t in _xTokenList[l]:
                """
                    DLL davranışları buraya entegre olucak.
                    Regex eşleşmeleri harici bir api'a entegre olmalı. dll ile birlikte çalışmalılar.
                    buradan regex bölümünü çıkar. ve result değişkenini ek bir standarta bağla
                    iş bu kadar basit
                """

                result = t.Regex.match(_xSource) # bu satır yerine dll gelecek
                if result:
                    _xStr = result.group()
                    if not len(_xStr) in _xMatches:
                        _xMatches[len(_xStr)] = []
                    _xMatches[len(_xStr)].append({"definition":t,"result":_xStr})
                
            if len(_xMatches) > 0:
                break

        #belleği boşalt
        del _xKeylist
        del _xSource
        del _xTokenList

        #eşleşmeler arasından en uzununu seç
        _xKeylist = list(_xMatches.keys())
        _xKeylist.sort(reverse=True)
        if len(_xKeylist) > 0:
            if len(_xMatches[_xKeylist[0]]) == 1:
                t = _xMatches[_xKeylist[0]][0]["definition"]
                v = _xMatches[_xKeylist[0]][0]["result"]
                
                del _xMatches
                del _xKeylist
                
                if t.Emit:
                    return {"Result":"TokenEmitted","Payload":Token(t.Name,v,(header.Ptr,Lexer._CalculatePointer(header,v)),t.ANID)}

                return {"Result":"TokenNotEmitted","Payload":(header.Ptr,Lexer._CalculatePointer(header,v))}
            
            else:
                raise LexerExceptions.ToMuchTokenMatched(header,_xMatches)

        raise LexerExceptions.NoTokenMatched(header)

    @staticmethod
    def _CalculatePointer(
        header:LexerHeader,
        result:str
    ) -> Pointer:
        """
            işaretciyi hesaplar
        """
        _xX = header.Ptr.x
        _xY = header.Ptr.y
        _xRaw = header.Ptr.raw
        _xSource = header.Source[header.Ptr.raw:]
        _xResultLength = len(result)

        for c in _xSource[:_xResultLength]:
            if c == "\n":
                _xY = 1
                _xX += 1
            else:
                _xY += 1

        _xRaw += _xResultLength
        
        return Pointer(_xX,_xY,_xRaw)