"""
    Genel Hatalar
"""

class UnkownRequest(Exception):
    def __init__(self, Request) -> None:
        
        xecd = "u000001"
        xemsg = f"Iç Hata - Hatalı istek tipi. {Request.To}, {Request.Request} tipinde bir istek tanımıyor."
        xedtl = f"\tgönderen : {Request.From}\n\talan : {Request.To}\n\tistek : {Request.Request}\n\tpayload : {Request.Payload}\n\n"
        xmsg = f"Bir hata meydana geldi.\nHata Kodu : {xecd}\nHata Açıklaması : {xemsg}\n\nDetaylar : \n{xedtl}"
        super().__init__(xmsg)