from flask import redirect
import BDconfig as data
from BDconfig import db

# TABELA COM OS ESTADOS E AS PRINCIPAIS CIDADES DO BRASIL
brazilian_cities = {
    "Acre": ["Rio Branco", "Cruzeiro do Sul", "Senador Guiomard", "Tarauacá", "Feijó", "Plácido de Castro", "Xapuri", "Porto Acre", "Sena Madureira", "Mâncio Lima", "Manoel Urbano", "Assis Brasil", "Epitaciolândia", "Brasiléia", "Jordão", "Santa Rosa do Purus", "Porto Walter", "Rodrigues Alves", "Marechal Thaumaturgo", "Capixaba"],
    "Alagoas": ["Maceió", "Arapiraca", "Rio Largo", "Palmeira dos Índios", "São Miguel dos Campos", "Arapiraca", "Coruripe", "Penedo", "União dos Palmares", "Santana do Ipanema", "Delmiro Gouveia", "Campo Alegre", "São Luís do Quitunde", "São Sebastião"],
    "Amapá": ["Macapá", "Santana", "Laranjal do Jari", "Oiapoque", "Mazagão", "Tartarugalzinho", "Pedra Branca do Amapari", "Calçoene", "Cutias", "Porto Grande", "Vitória do Jari", "Serra do Navio", "Amapá", "Ferreira Gomes", "Pracuúba", "Itaubal"],
    "Amazonas": ["Manaus", "Parintins", "Itacoatiara", "Manacapuru", "Coari", "São Gabriel da Cachoeira", "Tabatinga", "Maués", "Tefé", "Manicoré", "Humaitá", "Iranduba", "Eirunepé", "Rio Preto da Eva", "Boca do Acre", "Barreirinha", "Presidente Figueiredo", "Carauari", "Santo Antônio do Içá", "Tonantins"],
    "Bahia": ["Salvador", "Feira de Santana", "Vitória da Conquista", "Camaçari", "Itabuna", "Juazeiro", "Lauro de Freitas", "Ilhéus", "Jequié", "Teixeira de Freitas", "Alagoinhas", "Barreiras", "Porto Seguro", "Simões Filho", "Paulo Afonso", "Candeias", "Valença", "Santo Antônio de Jesus", "Jacobina", "Guanambi"],
    "Ceará": ["Fortaleza", "Caucaia", "Juazeiro do Norte", "Maracanaú", "Sobral", "Crato", "Itapipoca", "Maranguape", "Iguatu", "Quixadá", "Pacatuba", "Quixeramobim", "Aquiraz", "Russas", "Canindé", "Crateús", "Aracati", "Pacajus", "Cascavel", "Camocim"],
    "Distrito Federal": ["Brasília", "Ceilândia", "Gama", "Taguatinga", "Planaltina", "Recanto das Emas", "Samambaia", "Cruzeiro", "Sobradinho", "Valparaíso de Goiás", "Santa Maria", "Paranoá", "Águas Lindas de Goiás", "Riacho Fundo", "Brazlândia", "São Sebastião", "Itapoã"],
    "Espírito Santo": ["Vitória", "Vila Velha", "Serra", "Cariacica", "Cachoeiro de Itapemirim", "Linhares", "São Mateus", "Colatina", "Guarapari", "Aracruz", "Viana", "Nova Venécia", "Barra de São Francisco", "Santa Maria de Jetibá", "Castelo", "Domingos Martins", "Itapemirim"],
    "Goiás": ["Goiânia", "Aparecida de Goiânia", "Anápolis", "Rio Verde", "Luziânia", "Águas Lindas de Goiás", "Valparaíso de Goiás", "Trindade", "Formosa", "Novo Gama", "Itumbiara", "Senador Canedo", "Catalão", "Jataí", "Planaltina", "Cristalina", "Porangatu", "Mineiros", "Goianésia", "Jaraguá"],
    "Maranhão": ["São Luís", "Imperatriz", "São José de Ribamar", "Timon", "Caxias", "Codó", "Paço do Lumiar", "Açailândia", "Bacabal", "Balsas", "Santa Inês", "Barra do Corda", "Pinheiro", "Chapadinha", "Itapecuru Mirim", "Grajaú", "Coroatá", "Barreirinhas", "Zé Doca", "Tutóia"],
    "Mato Grosso": ["Cuiabá", "Várzea Grande", "Rondonópolis", "Sinop", "Tangará da Serra", "Cáceres", "Sorriso", "Lucas do Rio Verde", "Primavera do Leste", "Barra do Garças", "Alta Floresta", "Pontes e Lacerda", "Nova Mutum", "Campo Verde", "Juína", "Colniza", "Peixoto de Azevedo", "Poconé", "Matupá", "Sapezal"],
    "Mato Grosso do Sul": ["Campo Grande", "Dourados", "Três Lagoas", "Corumbá", "Ponta Porã", "Naviraí", "Nova Andradina", "Sidrolândia", "Aquidauana", "Maracaju", "Amambai", "Rio Brilhante", "Coxim", "Caarapó", "Miranda", "Bonito", "São Gabriel do Oeste", "Jardim", "Bataguassu", "Paranaíba"],
    "Minas Gerais": ["Belo Horizonte", "Uberlândia", "Contagem", "Juiz de Fora", "Belo Horizonte", "Betim", "Montes Claros", "Ribeirão das Neves", "Uberaba", "Governador Valadares", "Ipatinga", "Sete Lagoas", "Divinópolis", "Santa Luzia", "Ibirité", "Poços de Caldas", "Patos de Minas", "Teófilo Otoni", "Ponte Nova", "Pouso Alegre"],
    "Pará": ["Belém", "Ananindeua", "Santarém", "Marabá", "Castanhal", "Parauapebas", "Itaituba", "Cametá", "Bragança", "Marabá", "Abaetetuba", "Barcarena", "Conceição do Araguaia", "Paragominas", "Tucuruí", "Igarapé-Miri", "Altamira", "Moju", "Breves", "Santarém"],
    "Paraíba": ["João Pessoa", "Campina Grande", "Santa Rita", "Patos", "Campina Grande", "Bayeux", "Cabedelo", "Sousa", "Cajazeiras", "Guarabira", "Sapé", "Mamanguape", "Queimadas", "Monteiro", "Pombal", "Esperança", "Pedras de Fogo", "Rio Tinto", "Solânea", "Alagoa Grande"],
    "Paraná": ["Curitiba", "Londrina", "Maringá", "Ponta Grossa", "Cascavel", "São José dos Pinhais", "Foz do Iguaçu", "Colombo", "Guarapuava", "Paranaguá", "Araucária", "Toledo", "Apucarana", "Pinhais", "Campo Largo", "Arapongas", "Umuarama", "Piraquara", "Cambé", "Campo Mourão"],
    "Pernambuco": ["Recife", "Jaboatão dos Guararapes", "Olinda", "Caruaru", "Paulista", "Petrolina", "Cabo de Santo Agostinho", "Camaragibe", "Garanhuns", "Vitória de Santo Antão", "Igarassu", "São Lourenço da Mata", "Santa Cruz do Capibaribe", "Abreu e Lima", "Ipojuca", "Serra Talhada", "Araripina", "Gravatá", "Carpina", "Goiana"],
    "Piauí": ["Teresina", "Parnaíba", "Picos", "Parnaíba", "Floriano", "Piripiri", "Campo Maior", "Picos", "Piracuruca", "Barras", "José de Freitas", "São Raimundo Nonato", "Oeiras", "Paulistana", "Miguel Alves", "Luzilândia", "União", "Batalha", "Esperantina", "Altos"],
    "Rio de Janeiro": ["Rio de Janeiro", "São Gonçalo", "Duque de Caxias", "Nova Iguaçu", "Niterói", "Campos dos Goytacazes", "Belford Roxo", "São João de Meriti", "Petrópolis", "Volta Redonda", "Magé", "Macaé", "Itaboraí", "Mesquita", "Nova Friburgo", "Barra Mansa", "Nilópolis", "Teresópolis", "Nova Iguaçu", "Queimados"],
    "Rio Grande do Norte": ["Natal", "Mossoró", "Parnamirim", "Macaíba", "Natal", "Ceará-Mirim", "Caicó", "São Gonçalo do Amarante", "Nova Cruz", "Apodi", "Mossoró", "Pau dos Ferros", "Currais Novos", "João Câmara", "Assu", "Canguaretama", "Santa Cruz", "Macau", "Areia Branca", "Baraúna"],
    "Rio Grande do Sul": ["Porto Alegre", "Caxias do Sul", "Pelotas", "Caxias do Sul", "Canoas", "Santa Maria", "Gravataí", "Viamão", "Novo Hamburgo", "São Leopoldo", "Rio Grande", "Alvorada", "Santa Cruz do Sul", "Cachoeirinha", "Uruguaiana", "Bagé", "Bento Gonçalves", "Erechim", "Guaíba", "Sapucaia do Sul"],
    "Rondônia": ["Porto Velho", "Ji-Paraná", "Ariquemes", "Vilhena", "Cacoal", "Guajará-Mirim", "Jaru", "Rolim de Moura", "Ouro Preto do Oeste", "Pimenta Bueno", "Buritis", "Nova Mamoré", "Machadinho d'Oeste", "Espigão d'Oeste", "Alta Floresta d'Oeste", "Candeias do Jamari", "Presidente Médici", "São Miguel do Guaporé", "Nova Brasilândia d'Oeste", "Costa Marques"],
    "Roraima": ["Boa Vista", "Rorainópolis", "Boa Vista", "Cantá", "Caracaraí", "Mucajaí", "Pacaraima", "Bonfim", "Normandia", "São João da Baliza", "Alto Alegre", "Caroebe", "Uiramutã", "São Luiz"],
    "Santa Catarina": ["Abdon Batista", "Abelardo Luz", "Agrolândia", "Agronômica", "Água Doce", "Águas de Chapecó", "Águas Frias", "Águas Mornas", "Alfredo Wagner", "Alto Bela Vista", "Anchieta", "Angelina", "Anita Garibaldi", "Anitápolis", "Antônio Carlos", "Apiúna", "Arabutã", "Araquari", "Araranguá", "Armazém", "Arroio Trinta", "Arvoredo", "Ascurra", "Atalanta", "Aurora", "Balneário Arroio do Silva", "Balneário Barra do Sul", "Balneário Camboriú", "Balneário Gaivota", "Bandeirante", "Barra Bonita", "Barra Velha", "Bela Vista do Toldo", "Belmonte", "Benedito Novo", "Biguaçu", "Blumenau", "Bocaina do Sul", "Bom Jardim da Serra", "Bom Jesus", "Bom Jesus do Oeste", "Bom Retiro", "Bombinhas", "Botuverá", "Braço do Norte", "Braço do Trombudo", "Brunópolis", "Brusque", "Caçador", "Caibi", "Calmon", "Camboriú", "Campo Alegre", "Campo Belo do Sul", "Campo Erê", "Campos Novos", "Canelinha", "Canoinhas", "Capão Alto", "Capinzal", "Capivari de Baixo", "Catanduvas", "Caxambu do Sul", "Celso Ramos", "Cerro Negro", "Chapadão do Lageado", "Chapecó", "Cocal do Sul", "Concórdia", "Cordilheira Alta", "Coronel Freitas", "Coronel Martins", "Correia Pinto", "Corupá", "Criciúma", "Cunha Porã", "Cunhataí", "Curitibanos", "Descanso", "Dionísio Cerqueira", "Dona Emma", "Doutor Pedrinho", "Entre Rios", "Ermo", "Erval Velho", "Faxinal dos Guedes", "Flor do Sertão", "Florianópolis", "Formosa do Sul", "Forquilhinha", "Fraiburgo", "Frei Rogério", "Galvão", "Garopaba", "Garuva", "Gaspar", "Governador Celso Ramos", "Grão Pará", "Gravatal", "Guabiruba", "Guaraciaba", "Guaramirim", "Guarujá do Sul", "Guatambú", "Herval d'Oeste", "Ibiam", "Ibicaré", "Ibirama", "Içara", "Ilhota", "Imaruí", "Imbituba", "Imbuia", "Indaial", "Iomerê", "Ipira", "Iporã do Oeste", "Ipuaçu", "Ipumirim", "Iraceminha", "Irani", "Irati", "Irineópolis", "Itá", "Itaiópolis", "Itajaí", "Itapema", "Itapiranga", "Itapoá", "Ituporanga", "Jaborá", "Jacinto Machado", "Jaguaruna", "Jaraguá do Sul", "Jardinópolis", "Joaçaba", "Joinville", "José Boiteux", "Jupiá", "Lacerdópolis", "Lages", "Laguna", "Lajeado Grande", "Laurentino", "Lauro Müller", "Lebon Régis", "Leoberto Leal", "Lindóia do Sul", "Lontras", "Luiz Alves", "Luzerna", "Macieira", "Mafra", "Major Gercino", "Major Vieira", "Maracajá", "Maravilha", "Marema", "Massaranduba", "Matos Costa", "Meleiro", "Mirim Doce", "Modelo", "Mondaí", "Monte Carlo", "Monte Castelo", "Morro da Fumaça", "Morro Grande", "Navegantes", "Nova Erechim", "Nova Itaberaba", "Nova Trento", "Nova Veneza", "Novo Horizonte", "Orleans", "Otacílio Costa", "Ouro", "Ouro Verde", "Paial", "Painel", "Palhoça", "Palma Sola", "Palmeira", "Palmitos", "Papanduva", "Paraíso", "Passo de Torres", "Passos Maia", "Paulo Lopes", "Pedras Grandes", "Penha", "Peritiba", "Petrolândia", "Pinhalzinho", "Pinheiro Preto", "Piratuba", "Planalto Alegre", "Pomerode", "Ponte Alta", "Ponte Alta do Norte", "Ponte Serrada", "Porto Belo", "Porto União", "Pouso Redondo", "Praia Grande", "Presidente Castello Branco", "Presidente Getúlio", "Presidente Nereu", "Princesa", "Quilombo", "Rancho Queimado", "Rio das Antas", "Rio do Campo", "Rio do Oeste", "Rio do Sul", "Rio dos Cedros", "Rio Fortuna", "Rio Negrinho", "Rio Rufino", "Riqueza", "Rodeio", "Romelândia", "Salete", "Saltinho", "Salto Veloso", "Sangão", "Santa Cecília", "Santa Helena", "Santa Rosa de Lima", "Santa Rosa do Sul", "Santa Terezinha", "Santa Terezinha do Progresso", "Santiago do Sul", "Santo Amaro da Imperatriz", "São Bento do Sul", "São Bernardino", "São Bonifácio", "São Carlos", "São Cristovão do Sul", "São Domingos", "São Francisco do Sul", "São João Batista", "São João do Itaperiú", "São João do Oeste", "São João do Sul", "São Joaquim", "São José", "São José do Cedro", "São José do Cerrito", "São Lourenço do Oeste", "São Ludgero", "São Martinho", "São Miguel da Boa Vista", "São Miguel do Oeste", "São Pedro de Alcântara", "Saudades", "Schroeder", "Seara", "Serra Alta", "Siderópolis", "Sombrio", "Sul Brasil", "Taió", "Tangará", "Tigrinhos", "Tijucas", "Timbé do Sul", "Timbó", "Timbó Grande", "Três Barras", "Treviso", "Treze de Maio", "Treze Tílias", "Trombudo Central", "Tubarão", "Tunápolis", "Turvo", "União do Oeste", "Urubici", "Urupema", "Urussanga", "Vargeão", "Vargem", "Vargem Bonita", "Vidal Ramos", "Videira", "Vitor Meireles", "Witmarsum", "Xanxerê", "Xavantina", "Xaxim", "Zortéa"],
    "São Paulo": ["São Paulo", "Guarulhos", "Campinas", "São Paulo", "São Bernardo do Campo", "Santo André", "Osasco", "São José dos Campos", "São Paulo", "Ribeirão Preto", "Sorocaba", "Mauá", "São José do Rio Preto", "São Paulo", "Mogi das Cruzes", "Santos", "São Paulo", "São Caetano do Sul", "Jundiaí", "Piracicaba"],
    "Sergipe": ["Aracaju", "Nossa Senhora do Socorro", "Aracaju", "Lagarto", "Itabaiana", "São Cristóvão", "Estância", "Nossa Senhora da Glória", "Tobias Barreto", "Itabaiana", "Simão Dias", "Nossa Senhora das Dores", "Capela", "Propriá", "Barra dos Coqueiros", "Canindé de São Francisco", "Boquim", "Poço Redondo", "Nossa Senhora do Socorro"],
    "Tocantins": ["Palmas", "Araguaína", "Gurupi", "Palmas", "Araguaína", "Gurupi", "Porto Nacional", "Paraíso do Tocantins", "Guaraí", "Colinas do Tocantins", "Formoso do Araguaia", "Tocantinópolis", "Miracema do Tocantins", "Dianópolis", "Nova Olinda", "Araguatins", "Pedro Afonso", "Xambioá", "São Miguel do Tocantins", "Taguatinga"]
}


brazilian_states = ["Acre","Alagoas","Amapá","Amazonas","Bahia","Ceará","Distrito Federal","Espírito Santo","Goiás","Maranhão","Mato Grosso","Mato Grosso do Sul","Minas Gerais","Pará","Paraíba","Paraná","Pernambuco","Piauí","Rio de Janeiro","Rio Grande do Norte","Rio Grande do Sul","Rondônia","Roraima","Santa Catarina","São Paulo","Sergipe","Tocantins"]


def cadastrar_brasil():
    """
    Realiza o Cadastro do Brasil e suas principais cidades na base de dados a primeira vez que ela é acessada pelo link
    DB_COUNTRY, DB_ESTATE e DB_CITY

    :return: redireciona para pagina unidades federativas.
    """
    try:
        country = data.DB_COUNTRY(NAME='Brasil')
        db.session.add(country)
        db.session.commit()
        for state in brazilian_states:
            state = data.DB_ESTATE(ID_BD_COUNTRY=country.ID, NAME=state)
            db.session.add(state)
            db.session.commit()
            adicionar_cidade(state.NAME,state.ID)
        return redirect('/cadastros_gerais_unidades_federativas')
    except: 
        return 'Ocorreu um Erro Cadastrando o País'
    

def adicionar_cidade(state_name, state_id):
    """
    Realiza o cadastro das cidades para cada estado conforme a lista contida na biblioteca informada.

    :param state_name: o nome do estado que foi cadastrado
    :param state_id: o endereço do estado que foi cadastrado
    :return: Cidades cadastradas para o estado DB_CITY.
    """
    try:
        cities = brazilian_cities.get(state_name, [])
        for city_name in cities:
            city = data.DB_CITY(NAME=city_name, ID_BD_ESTATE=state_id)
            db.session.add(city)
        db.session.commit()
        return True
    except:
        return 'Ocorreu um Erro Cadastrando as Cidades'
    

def cadastrar_tiposdeprodutos():
    """
    Cadastra os tipos de produto Materia Prima e Materiais de Consumo na base de dados DB_PRODUCT_TYPE.
    o cadastro destes dois intens é obrigatório devido a serem utilizados no cálculo de custos do produto.

    :return: Tipos de produtos cadastrados.
    """
    try:
        #MP ID = 1
        tipo = data.DB_PRODUCT_TYPE(NAME='Matérias Primas', ABREVIATION='MP')
        db.session.add(tipo)
        #MC ID = 2
        tipo = data.DB_PRODUCT_TYPE(NAME='Materiais de Consumo', ABREVIATION='MC')
        db.session.add(tipo)
        db.session.commit()
        return redirect('/cadastros_gerais_tipos_de_produtos')
    except:
        return 'Ocorreu um Erro Cadastrando os Tipos de Produtos'