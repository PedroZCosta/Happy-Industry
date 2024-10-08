import BDconfig as data


def helo():
    """
    Foi utilizado para testes, vai ficar no código pois levou 4 horas para funcionar
    """
    return 'helo'


def get_db_mc(id_bd_mc):
    """
    Retorna informações da bade de dados de Materiais de Consumo.

    :param id_bd_mc: a chave da linha da base de dados
    :return: retorna informações da base de dados BD_MC de acordo com o ID.
    """
    db_mc = data.DB_MC.query.filter_by(ID=id_bd_mc).first() 
    return db_mc


def get_db_mp(id_bd_mp):
    """
    Retorna informações da bade de dados de Materias Primas.

    :param id_bd_mp: a chave da linha da base de dados
    :return: retorna informações da base de dados BD_MP de acordo com o ID.
    """
    db_mp = data.DB_MP.query.filter_by(ID=id_bd_mp).first() 
    return db_mp


def get_group(group_id):
    """
    Retorna o nome do grupo o ID da grupo.

    :param group_id: a chave da medida para a tabela BD_GROUP
    :return: retorna o NAME da tabela BD_GROUP de acordo com o ID.
    """
    group = data.DB_GROUP.query.filter_by(ID=group_id).first()
    return group.NAME if group else None


def get_measureabv(measure_id):
    """
    Retorna a abreviação da medida utilizando o ID da medida.

    :param measure_id: a chave da medida para a tabela BD_MEASURES
    :return: retorna o ABREVIATION da tabela BD_MEASURES de acordo com o ID.
    """
    measure = data.DB_MEASURES.query.filter_by(ID=measure_id).first()
    return measure.ABREVIATION if measure else None


def get_measure(measure_id):
    """
    Retorna o nome da medida utilizando o ID da medida.

    :param measure_id: a chave da medida para a tabela BD_MEASURES
    :return: retorna o NAME da tabela BD_MEASURES de acordo com o ID.
    """
    measure = data.DB_MEASURES.query.filter_by(ID=measure_id).first()
    return measure.NAME if measure else None


def get_city(city_id):
    """
    Retorna o nome da cidade utilizando o ID da cidade.

    :param city_id: a chave do cidade para a tabela BD_CITY
    :return: retorna o NAME da tabela BD_CITY de acordo com o ID.
    """
    city = data.DB_CITY.query.filter_by(ID=city_id).first()
    return city.NAME if city else None


def get_state(state_id):
    """
    Retorna o nome do estado utilizando o ID do estado.

    :param state_id: a chave do estado para a tabela BD_ESTATE
    :return: retorna o NAME da tabela BD_ESTATE de acordo com o ID.
    """
    state = data.DB_ESTATE.query.filter_by(ID=state_id).first()
    return state.NAME if state else None


def get_country(country_id):
    """
    Retorna o nome do país utilizando o ID do país.

    :param country_id: a chave do país para a tabela BD_COUNTRY
    :return: retorna o NAME da tabela BD_COUNTRY de acordo com o ID.
    """
    country = data.DB_COUNTRY.query.filter_by(ID=country_id).first()
    return country.NAME if country else None


def get_worker_job(job_id):
    """
    Retorna o nome da função do operador utilizando o ID do trabalho.

    :param job_id: a chave do encargo para a tabela BD_JOB
    :return: retorna o NAME da tabela BD_JOB de acordo com o ID.
    """
    job = data.DB_JOB.query.filter_by(ID=job_id).first()
    return job.NAME if job else None


def get_product_measure(product_id, product_type_id):
    """
    Retorna a tabela DB_MEASURES utilizando o ID de um MP ou MC, e o seu typo.

    :param product_id: a chave do produto (Materia prima ou Material de consumo) da tabela BD_MP ou DB_MC desejado
    :param product_type_id: o valor para converter
    :return: retorna a informação da tabela DB_MEASURES de acordo com o ID.
    """
    measure_id = get_product_info(product_id, product_type_id).ID_BD_MEASURES
    measure = data.DB_MEASURES.query.filter_by(ID=measure_id).first()
    return measure
    

def get_product_type(product_type_id):
    """
    Retorna a tabela do tipo de produco (1=MP , 2=MC)

    :param product_type_id: o valor para converter
    :return: retorna a informação da tabela product_type de acordo com o ID.
    """
    product_type = data.DB_PRODUCT_TYPE.query.filter_by(ID=product_type_id).first()
    return product_type


def get_product_info(product_id, product_type_id):
    """
    Retorna as informações das tabelas DB_MP ou DB_MC de acordo com o tipo e id do produto

    :param product_id: a chave do produto (Materia prima ou Material de consumo) da tabela BD_MP ou DB_MC desejado
    :param product_type_id: a chave do tipo do produto, utlizada para selecionar a tabela desejada
    :return: retorna a informação da tabela escolhida de acordo com o ID.
    """
    if product_type_id == 1:
        product = data.DB_MP.query.filter_by(ID=product_id).first()
    elif product_type_id == 2:
        product = data.DB_MC.query.filter_by(ID=product_id).first()
    else:
        product = None
    return product


def get_supplier_name(supplier_id):
    """
    Retorna o nome de um fornecedor utilizando sua ID

    :param supplier_id: a key correspondente ao fornecedor
    :return: retorna o nome do fornecedor.
    """
    supplier = data.DB_SUPPLIER.query.filter_by(ID=supplier_id).first()
    return supplier.NAME if supplier else None


def format_currency(amount):
    """
    Formata um valor para monetario

    :param amount: o valor para converter
    :return: retorna o valor em formato monetario.
    """
    if amount is not None:
        return "R$ {:.2f}".format(amount)
    else:
        return '0.00'


def format_percentage(percentage):
    """
    Formata um valor para percentual

    :param percentage: o valor para converter
    :return: retorna o valor em formato percentual.
    """
    try:
        if percentage is not None:
            return "{:.2f}%".format(percentage)
        else:
            return '0.00%'
    except:
        return '0.00%'


def calculate_total_price(price, quantity, transport_cost, difal=0, ipi=0):
    """
    Retorna o preço total de uma compra com difal e icms.

    :param price: o preço informado
    :param quantity: a quantidade informada
    :param transport_cost: o preço do frete
    :param difal: o % da difal aplicado, caso nao informado 0
    :param ipi: o % do IPI informado, caso não informado 0
    :return: retorna o preço calculado do produto.
    """
    total_price = (price * quantity) + transport_cost
    total_price += (price * quantity * difal) / 100
    total_price += (price * quantity * ipi) / 100
    return total_price


#defs para os relatorios
def get_latest_price(product_id, product_type_id):
    """
    Retorna o ultimo preço de um produto.

    :param product_id: o ID do produto desejado
    :param product_type_id: o ID do tipo do produto (Materia prima ou Material de consumo)
    :return: retorna o preço do produto.
    """
    purchase = (data.DB_PURCHASES.query.filter_by(ID_BD_PROD=product_id, ID_BD_PRODUCT_TYPE=product_type_id).order_by(data.DB_PURCHASES.NF_DATA.desc()).first())
    return purchase.PRICE if purchase else 0


def get_latest_purchase(product_id, product_type_id):
    """
    Tras a ultima compra por ordem de data de um produto.

    :param product_id: o ID do produto desejado
    :param product_type_id: o ID do tipo do produto (Materia prima ou Material de consumo)
    :return: retorna  um dicionario contento as informações de compra do produto.
    """
    purchase = (data.DB_PURCHASES.query
                .filter_by(ID_BD_PROD=product_id, ID_BD_PRODUCT_TYPE=product_type_id)
                .order_by(data.DB_PURCHASES.NF_DATA.desc())
                .first())
    
    if not purchase:
        return {'price': 0, 'difal': 0, 'ipi': 0, 'transport_cost': 0, 'quantity': 0}
    
    if product_type_id == 1:
        product = data.DB_MP.query.filter_by(ID=product_id).first()
        difal = 0
        ipi = product.IPI if product else 0
    elif product_type_id == 2:
        product = data.DB_MC.query.filter_by(ID=product_id).first()
        difal = product.DIFAL if product else 0
        ipi = product.IPI if product else 0
    else:
        difal = 0
        ipi = 0
    
    return {
        'price': purchase.PRICE,
        'difal': difal,
        'ipi': ipi,
        'transport_cost': purchase.TRANSPORT_COST,
        'quantity': purchase.QUANTITY
    }


def calculate_total_cost(product_id):
    """
    Calcula o custo total de um produto a ser produzido.

    :param product_id: o ID do produto desejado
    :return: custo total da produção de um item em formato de moeda.
    """
    products_mp = data.DB_PROD_MP.query.all()
    products_mc = data.DB_PROD_MC.query.all()
    products_mo = data.DB_PROD_MO.query.all()

    total_cost = 0
    
    # Calculo do custo de materia prima
    for product_mp in products_mp:
        if product_mp.ID_BD_PROD == product_id:
            latest_purchase = get_latest_purchase(product_mp.ID_BD_MP, 1)
            total_cost += calculate_total_price(latest_purchase['price'], product_mp.QUANTITY, (latest_purchase['transport_cost']/latest_purchase['quantity']), latest_purchase['difal'], latest_purchase['ipi'])
    
    # Calculo dos custos de materiais de consumo
    for product_mc in products_mc:
        if product_mc.ID_BD_PROD == product_id:
            latest_purchase = get_latest_purchase(product_mc.ID_BD_MC, 2)
            total_cost += calculate_total_price(latest_purchase['price'], 1, (latest_purchase['transport_cost']/latest_purchase['quantity']), latest_purchase['difal'], latest_purchase['ipi']) / product_mc.QUANTITY
    
    # Calculo do preço da mão de obra
    for product_mo in products_mo:
        if product_mo.ID_BD_PROD == product_id:
            total_cost += calculate_labor_cost(product_mo.WORKERS_QUANTITY, product_mo.LOT_AMMOUNT, product_mo.TIME_TO_PRODUCE, calculate_price_min(product_mo.ID_BD_PROD))
    
    return format_currency(total_cost)


def calculate_price_min(ID):
    """
    Calcula o preço da mão de obra por minuto.

    :param ID: algum bug nos impediu de deixar sem parametro, mas não é utilizado para nada
    :return: price_min (custo pro minuto).
    """
    total_monthly_rent = 0
    active_workers = data.DB_WORKERS.query.filter_by(ACTIVE=1).all()
    if active_workers:
        for worker in active_workers:
            job = data.DB_JOB.query.filter_by(ID=worker.ID_BD_JOB).first()
            total_monthly_rent += job.RENT
        hourly_rate = total_monthly_rent / (220 * len(active_workers)) #220 horas por mês
        price_min = hourly_rate / 60 
    else:
        price_min = 0
    
    return price_min


def calculate_labor_cost(workers_quantity, lot_amount, time_to_produce, price_min):
    """
    Calcula o custo de mão de obra para produção.

    :param workers_quantity: numero de operadores envolvidos.
    :param lot_amount: numero de itens por lote.
    :param time_to_produce: tempo em minutos para produzir um lote.
    :param price_min: resultado da função price_min.
    :return: preço total da mão de obra.
    """
    price_min = price_min
    total_time = workers_quantity * time_to_produce
    total_cost = total_time * price_min  
    return (total_cost / lot_amount)