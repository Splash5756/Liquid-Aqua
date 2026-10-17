from dataclasses import dataclass

"""
    Box içi istek tipi örneği
"""

@dataclass
class Request:
    """
        From -> String | isteği gönderenin ismi
        To -> string | isteğin gönderildiği isim
        Request -> string | istek
        Payload -> Dictionary | ek bilgi
    """
    From:str
    To:str
    Request:str
    Payload:dict
