from dataclasses import dataclass
from Template.Request import Request
from Template.Ast import Ast, LazyAst, AstDef
from Template.Exceptions import General

"""
    notlarım

    Request.payload'ı programla. core üzerinde
    örneğin "__COPY__" etiketinin altındaki herşeyi resulta kopyalamasını sağla
    alternatif olarak Başlığa taşı geçici veriyi
    mesela "__OVERWRITE__" ile üstüne yazma isteği gönderilebilinir
    yada "__PATCH__" ile bir verinin içeriği değiştirilebilinir

    ancak Freaky şeylerle uğraşmak yerine direkt çağrılar ayarlayıp Parser'ın ayarlama yapmasını sağlayabiliriz.

    yada Lexer gibi elemanlara __DO__ isimli bir job ekleyip payload field aracılığıyla parametrik düzenlemeler yapabiliriz mesela __DO__ Job:SetPointer
    misali. tabii daha güzel bir arayüz daha hoş olabilir.

    bana kalırsa ikiside olsun. çünkü __COPY__ ye ihtiyacım var. ancak şunu yapabiliriz. paket payloadında "__CORE__":{"__CMD__":["COPY","-FP","__COPY__","-CT","Result","-TP","__COPY__","-RM"]} gibi birşey olabilir
    dosya içi davranış kazanmak için payload ismini değiştiririz. yani tek istekte hem birden fazla komut hemde iş yaptırabiliriz.

    örnek:
        "__LEXER__":{"__CMD__":["Make","-v","_xHeader","&&","Read","-f","-X","Get","-f","Header","*","-t","_xHeader","&&","Write","-t","-X","Get","-type","Attr","-f","_xHeader","-v","Pointer","*","-v","-X","Get","-f","PTR","*"]}

    ile Lexer işaretcisini yeniden konumlandırabiliriz.
    bunun için bir komut seti belirtmek gerekiyor.

    az çok oturdu gibi ama.
    
    -v -> value demek
    -f -> from demek
    -t -> to demek
    && -> after demek
    -X -> Komutun sonucunu al demek
    * -> komutun sonu demek
    
    Misal

    make -type var -v abc komutu yapabiliriz
    bu durumda -type lazım

    yani argüman seti şu şekilde oluyor
    -v <Value>
    -f <Object>
    -t <Object>
    -type <Type>
    -X <Command> *
    <Command> && <Command> 

    komut seti de şu olabilir

    make
    read
    write
    get

    bunlar responsif istekleri tasarlamak için gerekli

    ancak birde bellek alanı tutma var.

    __COPY__ alanı fikrini programlanabilir posta servisi ile çöpe attığımızdan dolayı fazlası lazım

    bu durumda posta servisine 2. bir sistem eklemek gerekebilir. böylece zaten eninde sonunda ekleyeceğim header kopyalama mekaniğini bu sisteme ekleriz.

    sistem şu şekilde çalışır.
    posta servisinde kayıtlar bulunur. <boxid> <from> <to> <request> <payload> <end> formatında
    böylece kendine gelen isteklerden uygun olanlarının payload'ına ekleme yapar

    misal <Any> <Any> "Lexer" <Any> {"Header":LexerHeader} -1 kaydı lexere giden tüm isteklere başlık verisini ekler.

    bunu komut yürütebilen isteklerle kombinleyince

    <id> "Lexer" "Parser" "Result" {"Temp":cache} 1 ile lexerin göndereceği cevaba parser geçici bellek bilgisi dahil edilebilinir

    bu sisteme ekleme çıkarma yapmak için

    postmark -a/-r -id id -f from -t to -req reqtype -payload {} -i int
    
    gibi bir komut eklenebilir

    bu derleyicinin iç akışında olan bir davranış biçimi genişletilemez düzenlenemez. (en azından kod kütüphanesiyle belki eklenti sistemi ile değiştirilebilinir bu mesele ileride bakarız)
"""


@dataclass
class ParserHeader:
    """
        Duruma bağlı genişletilebilir
    """
    AstList:list[AstDef]
    BoxID:bytes

class Parser:
    @staticmethod
    def Parse(request:Request):
        match(request.Request):
            case "Result":
                #nereden geldiğini kontrol et
                pass
            case _:
                raise General.UnexpectedRequest(request)