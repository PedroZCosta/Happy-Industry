from flask import render_template, redirect
import BDconfig as data
import UsefulFunctions as uful
from sqlalchemy import desc


#indice do menu


def main():
    """
    Redireciona a Janela para Página Inicial.

    :return: main.html.
    """
    return render_template('main.html')

# Cadastros Gerais

def cadastros_gerais_unidades_federativas():
    """
    Redireciona a Janela de Unidades Federativas.

    :return: cadastro_uf.html.
    """
    countryes = data.DB_COUNTRY.query.order_by(data.DB_COUNTRY.NAME).all()
    if len(countryes) < 1:
        return redirect('/cadastar_brasil')
    else:
        return render_template('cadastros_gerais/cadastro_uf.html', countryes=countryes)


def cadastros_gerais_unidades_de_medidas():
    """
    Redireciona a Janela de Unidades de Medidas.

    :return: cadastro_um.html.
    """
    measures = data.DB_MEASURES.query.order_by(data.DB_MEASURES.NAME).all()
    return render_template('cadastros_gerais/cadastro_um.html', measures=measures)


def cadastros_gerais_grupos_de_produtos():
    """
    Redireciona a Janela de Grupos de Produtos.

    :return: cadastro_gruposprodutos.html.
    """
    groups = data.DB_GROUP.query.order_by(data.DB_GROUP.NAME).all()
    return render_template('cadastros_gerais/cadastro_gruposprodutos.html', groups=groups)


def cadastros_gerais_tipos_de_produtos():
    """
    Redireciona a Janela de Tipos de Produtos.

    :return: cadastro_tiposprodutos.html.
    """
    types = data.DB_PRODUCT_TYPE.query.order_by(data.DB_PRODUCT_TYPE.NAME).all()
    if len(types) < 1:
        return redirect('/cadastrar_tiposdeprodutos')
    else:
        return render_template('cadastros_gerais/cadastro_tiposprodutos.html', types=types)


# Cadastros de Entidades

def cadastros_de_entidades_encargos_e_salarios():
    """
    Redireciona a Janela de Encargos e Salários.

    :return: cadastro_encargos.html.
    """
    jobs = data.DB_JOB.query.order_by(data.DB_JOB.NAME).all()
    return render_template('cadastros_entidades/cadastro_encargos.html', jobs=jobs, format_currency=uful.format_currency)


def cadastros_de_entidades_colaboradores():
    """
    Redireciona a Janela de Colaboradores.

    :return: cadastro_colaboradores.html.
    """
    workers = data.DB_WORKERS.query.order_by(data.DB_WORKERS.NAME).all()
    jobs = data.DB_JOB.query.order_by(data.DB_JOB.NAME).all()
    countryes = data.DB_COUNTRY.query.order_by(data.DB_COUNTRY.NAME).all()
    estates = data.DB_ESTATE.query.order_by(data.DB_ESTATE.NAME).all()
    cityes = data.DB_CITY.query.order_by(data.DB_CITY.NAME).all()
    return render_template('cadastros_entidades/cadastro_colaboradores.html', workers=workers, jobs=jobs, countryes=countryes
                           , estates=estates, cityes=cityes, get_worker_job=uful.get_worker_job)


def cadastros_de_entidades_fornecedores():
    """
    Redireciona a Janela de Fornecedores.

    :return: cadastro_fornecedores.html.
    """
    suppliers = data.DB_SUPPLIER.query.order_by(data.DB_SUPPLIER.NAME).all()
    countryes = data.DB_COUNTRY.query.order_by(data.DB_COUNTRY.NAME).all()
    estates = data.DB_ESTATE.query.order_by(data.DB_ESTATE.NAME).all()
    cityes = data.DB_CITY.query.order_by(data.DB_CITY.NAME).all()
    return render_template('cadastros_entidades/cadastro_fornecedores.html', suppliers=suppliers, countryes=countryes
                           , estates=estates, cityes=cityes, get_city=uful.get_city, get_state=uful.get_state, get_country=uful.get_country)


#Cadastros de Materiais

def cadastros_de_materiais_materia_prima():
    """
    Redireciona a Janela de Materias Primas.

    :return: cadastro_mp.html.
    """
    mps = data.DB_MP.query.order_by(data.DB_MP.NAME).all()
    measures = data.DB_MEASURES.query.order_by(data.DB_MEASURES.NAME).all()
    return render_template('cadastros_materiais/cadastro_mp.html', mps=mps, measures=measures, format_percentage=uful.format_percentage
                           , get_measure=uful.get_measure)


def cadastros_de_materiais_material_de_consumo():
    """
    Redireciona a Janela de Materiais de Consumo.

    :return: cadastro_mc.html.
    """
    mcs = data.DB_MC.query.order_by(data.DB_MC.NAME).all()
    measures = data.DB_MEASURES.query.order_by(data.DB_MEASURES.NAME).all()
    return render_template('cadastros_materiais/cadastro_mc.html', mcs=mcs, measures=measures, format_percentage=uful.format_percentage
                           , get_measure=uful.get_measure)


def cadastros_de_materiais_produtos():
    """
    Redireciona a Janela de Produtos.

    :return: cadastro_produtos.html.
    """
    products = data.DB_PROD.query.order_by(data.DB_PROD.NAME).all()
    groups = data.DB_GROUP.query.order_by(data.DB_GROUP.NAME).all()
    return render_template('cadastros_materiais/cadastro_produtos.html', products=products, groups=groups, get_group=uful.get_group)


#Movimentações

def movimentacoes_compras():
    """
    Redireciona a Janela de Compras.

    :return: movimentacao_compras.html.
    """
    purchases = data.DB_PURCHASES.query.order_by(desc(data.DB_PURCHASES.NF_DATA)).all()
    products = data.DB_PROD.query.all()
    products_types = data.DB_PRODUCT_TYPE.query.all()
    mps = data.DB_MP.query.all()
    mcs = data.DB_MC.query.all()
    suppliers = data.DB_SUPPLIER.query.all()
    measures = data.DB_MEASURES.query.all()
    return render_template('movimentacoes/movimentacao_compras.html', products_types=products_types, products=products, suppliers=suppliers
                           , purchases=purchases, mps=mps, mcs=mcs, measures=measures, get_product_type=uful.get_product_type, get_product_info=uful.get_product_info
                           , get_supplier_name=uful.get_supplier_name, format_currency=uful.format_currency, format_percentage=uful.format_percentage
                           , calculate_total_price=uful.calculate_total_price, get_product_measure=uful.get_product_measure)


#Relatorios




def relatorios_precos_dos_produtos():
    """
    Redireciona a Janela de Preços dos Produtos.

    :return: relatorio_precosprodutos.html.
    """
    products = data.DB_PROD.query.all()
    groups = data.DB_GROUP.query.order_by(data.DB_GROUP.NAME).all()
    products_types = data.DB_PRODUCT_TYPE.query.all()
    mps = data.DB_MP.query.all()
    mcs = data.DB_MC.query.all()
    suppliers = data.DB_SUPPLIER.query.all()
    measures = data.DB_MEASURES.query.all()
    products_mp = data.DB_PROD_MP.query.all()
    products_mc = data.DB_PROD_MC.query.all()
    products_mo = data.DB_PROD_MO.query.all()
    return render_template('relatorios/relatorio_precosprodutos.html', products_types=products_types, products=products, suppliers=suppliers
                           , groups=groups, mps=mps, mcs=mcs, measures=measures, products_mp=products_mp, products_mo=products_mo, products_mc=products_mc
                           , get_product_type=uful.get_product_type, get_product_info=uful.get_product_info, get_supplier_name=uful.get_supplier_name
                           , format_currency=uful.format_currency, format_percentage=uful.format_percentage, get_db_mp=uful.get_db_mp, get_measureabv=uful.get_measureabv
                           , get_db_mc=uful.get_db_mc, calculate_total_price=uful.calculate_total_price, get_product_measure=uful.get_product_measure, get_latest_price=uful.get_latest_price
                           , get_latest_purchase=uful.get_latest_purchase, calculate_labor_cost=uful.calculate_labor_cost, calculate_price_min=uful.calculate_price_min
                           , calculate_total_cost=uful.calculate_total_cost)