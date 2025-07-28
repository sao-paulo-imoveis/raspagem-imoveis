import scrapy

class ImovelItem(scrapy.Item):
    imobiliaria = scrapy.Field()
    codigo = scrapy.Field()
    url_detalhes = scrapy.Field()
    url_img = scrapy.Field()
    preco = scrapy.Field()
    bairro = scrapy.Field()
    cidade = scrapy.Field()
    tipo = scrapy.Field()
    dormitorios = scrapy.Field()
    metragem = scrapy.Field()
    vagas = scrapy.Field()
    data_captura = scrapy.Field()
    endereco = scrapy.Field()
    descricao = scrapy.Field()
    condominio_nome = scrapy.Field()
    iptu = scrapy.Field()
    iptu_periodo = scrapy.Field()
    condominio = scrapy.Field()
    condominio_periodo = scrapy.Field()
    caracteristicas = scrapy.Field()
    
    # Novo campo agrupando os essenciais como dicionário booleano
    caracteristicas_essenciais = scrapy.Field()  # {'academia': True, 'piscina': False, ...}
