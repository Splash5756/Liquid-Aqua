"""
    Genel Hatalar
"""
class General:
    class UnexpectedRequest(Exception):
        def __init__(self, Request) -> None:
            xecd = "General1"
            xemsg = f"Iç Hata - Beklenmeyen istek tipi. {Request.To}, {Request.Request} tipinde bir istek tanımıyor."
            xedtl = f"\tGönderen : {Request.From}\n\tAlan : {Request.To}\n\tIstek : {Request.Request}\n\tPayload : {Request.Payload}\n\n"
            xmsg = f"Bir hata meydana geldi.\nHata Kodu : {xecd}\nHata Açıklaması : {xemsg}\n\nDetaylar : \n{xedtl}"
            super().__init__(xmsg)

    class UnexpectedRequestPayload(Exception):
        def __init__(self, Request, Key, Expection, Value) -> None:
            xecd = "General2"
            xemsg = f"Iç Hata - Beklenmeyen istek ek verisi. {Request.Payload}, {Request.To} tarafından beklenen {Key} değerine '{type(Value)}' döndü."
            xedtl = f"\tGönderen : {Request.From}\n\tAlan : {Request.To}\n\tIstek : {Request.Request}\n\tPayload : {Request.Payload}\n\tAnahtar : {Key}\n\tBeklenen değer : {Expection}\n\tGelen değer : {Value}"
            xmsg = f"Bir hata meydana geldi.\nHata Kodu : {xecd}\nHata Açıklaması : {xemsg}\n\nDetaylar : \n{xedtl}"
            super().__init__(xmsg)

    class UnexpectedException(Exception):
        def __init__(self, Sender, *args: object) -> None:
            xecd = "General3"
            xemsg = f"Iç Hata - Beklenmeyen hata. {Sender} beklenmeyen bir durumla karşılaştı."
            xedtl = f"\tKonum : {Sender}\n\tEk Argümanlar : {args}\n\n"
            xmsg = f"Bir hata meydana geldi.\nHata Kodu : {xecd}\nHata Açıklaması : {xemsg}\n\nDetaylar : \n{xedtl}"
            super().__init__(xmsg,Sender,*args)

"""
    Lexer hataları
"""
class Lexer:
    class NoTokenMatched(Exception):
        def __init__(self, header) -> None:
            xecd = "Lexer1"
            xemsg = f"Iç Hata - Lexer eşleşme bulamadı. Lexer {header.BoxID} konumunda hiçbir eşleşme bulamadı."
            xedtl = f"\tBoxID : {header.BoxID}\n\tKaynak : {header.Source}\n\tTokenler : {header.TokenList}\n\tDavranışlar : {header.ModeList}\n\tIşaretçi : {header.Ptr.toStr()}\n\n"
            xmsg = f"Bir hata meydana geldi.\nHata Kodu : {xecd}\nHata Açıklaması : {xemsg}\n\nDetaylar : \n{xedtl}"
            super().__init__(xmsg)

    class ToMuchTokenMatched(Exception):
            def __init__(self, header, BestList) -> None:
                xecd = "Lexer2"
                xemsg = f"Iç Hata - Lexer birden fazla eşleşme buldu. Lexer {header.BoxID} konumunda {len(BestList)} eşleşme bulduğu için kararsız kaldı."
                xedtl = f"\tBoxID : {header.BoxID}\n\tKaynak : {header.Source}\n\tTokenler : {header.TokenList}\n\tDavranışlar : {header.ModeList}\n\tIşaretçi : {header.Ptr.toStr()}\n\tEşleşmeler : {BestList}\n\n"
                xmsg = f"Bir hata meydana geldi.\nHata Kodu : {xecd}\nHata Açıklaması : {xemsg}\n\nDetaylar : \n{xedtl}"
                super().__init__(xmsg)