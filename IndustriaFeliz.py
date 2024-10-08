from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import BDconfig as data
import cadastrosiniciais as first
from BDconfig import db, app
from datetime import datetime, date
import index
import sys
import UsefulFunctions as uful
from UsefulFunctions import get_product_type
# esse import ira criar as bases de dados caso não existam


# ================== AQUI COMEÇA O PROGRAMA ==================
# cada app route e uma ação



# index.py
# ================== O INDICE DE NAVEGAÇÃO COMEÇA AQUI ==================


@app.route('/', methods=['POST','GET'])
def main():
    return index.main()


# Cadastros Gerais

@app.route('/cadastros_gerais_unidades_federativas', methods=['POST','GET'])
def cadastros_gerais_unidades_federativas(): 
    return index.cadastros_gerais_unidades_federativas()


@app.route('/cadastros_gerais_unidades_de_medidas', methods=['POST','GET'])
def cadastros_gerais_unidades_de_medidas(): 
    return index.cadastros_gerais_unidades_de_medidas()


@app.route('/cadastros_gerais_grupos_de_produtos', methods=['POST','GET'])
def cadastros_gerais_grupos_de_produtos(): 
    return index.cadastros_gerais_grupos_de_produtos()


@app.route('/cadastros_gerais_tipos_de_produtos', methods=['POST','GET'])
def cadastros_gerais_tipos_de_produtos(): 
    return index.cadastros_gerais_tipos_de_produtos()


# Cadastros de Entidades

@app.route('/cadastros_de_entidades_encargos_e_salarios', methods=['POST','GET'])
def cadastros_de_entidades_encargos_e_salarios(): 
    return index.cadastros_de_entidades_encargos_e_salarios()


@app.route('/cadastros_de_entidades_colaboradores', methods=['POST','GET'])
def cadastros_de_entidades_colaboradores(): 
    return index.cadastros_de_entidades_colaboradores()


@app.route('/cadastros_de_entidades_fornecedores', methods=['POST','GET'])
def cadastros_de_entidades_fornecedores(): 
    return index.cadastros_de_entidades_fornecedores()


#Cadastros de Materiais

@app.route('/cadastros_de_materiais_materia_prima', methods=['POST','GET'])
def cadastros_de_materiais_materia_prima(): 
    return index.cadastros_de_materiais_materia_prima()


@app.route('/cadastros_de_materiais_material_de_consumo', methods=['POST','GET'])
def cadastros_de_materiais_material_de_consumo(): 
    return index.cadastros_de_materiais_material_de_consumo()


@app.route('/cadastros_de_materiais_produtos', methods=['POST','GET'])
def cadastros_de_materiais_produtos(): 
    return index.cadastros_de_materiais_produtos()


#Movimentações

@app.route('/movimentacoes_compras', methods=['POST','GET'])
def movimentacoes_compras(): 
    return index.movimentacoes_compras()


#Relatorios


@app.route('/relatorios_precos_dos_produtos', methods=['POST','GET'])
def relatorios_precos_dos_produtos(): 
    return index.relatorios_precos_dos_produtos()


# ================== O INDICE DE NAVEGAÇÃO ACABA AQUI ==================


# ================== AQUI COMEÇA OS CADASTROS GERAIS ==================



#CADASTRAR UM PAÍS
@app.route('/cadastros_gerais_unidades_federativas_cadastrar', methods=['POST','GET'])
def cadastros_gerais_unidades_federativas_cadastrar():
    if request.method == 'POST':
        str_name = request.form['name']
        new_input = data.DB_COUNTRY(NAME=str_name)
        countries = data.DB_COUNTRY.query.all()
        for country in countries:
            if str_name.lower() in country.NAME.lower():
                return_link = '/cadastros_gerais_unidades_federativas'
                error_name = 'Esse pais ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect('/cadastros_gerais_unidades_federativas')
        except: 
            error_name = 'Ocorreu um erro ao cadastrar esse pais!'
            return_link = '/cadastros_gerais_unidades_federativas'
            return render_template('/erro.html', return_link=return_link, error_name=error_name)    
    else:
        return redirect('/cadastros_gerais_unidades_federativas')
    

#DELETAR O PAÍS
@app.route('/cadastros_gerais_unidades_federativas_deletar/<int:ID_COUNTRY>')
def cadastros_gerais_unidades_federativas_deletar(ID_COUNTRY):
    country_to_delete = data.DB_COUNTRY.query.get_or_404(ID_COUNTRY)
    try:
        db.session.delete(country_to_delete)
        db.session.commit()
        return redirect('/cadastros_gerais_unidades_federativas')
    except:
        error_name = 'Ocorreu um erro ao deletar esse pais!'
        return_link = ('/cadastros_gerais_unidades_federativas')
        return render_template('/erro.html', return_link=return_link, error_name=error_name)   


#ATUALIZAR O PAÍS CADASTRADO
@app.route('/cadastros_gerais_unidades_federativas_update/<int:ID_COUNTRY>', methods=['GET', 'POST'])
def cadastros_gerais_unidades_federativas_update(ID_COUNTRY):
    country = data.DB_COUNTRY.query.get_or_404(ID_COUNTRY)
    if request.method == 'POST':
        country.NAME = request.form['name']
        countries = data.DB_COUNTRY.query.all()
        str_name = request.form['name']
        for country in countries:
            if str_name.lower() in country.NAME.lower() and country.ID != ID_COUNTRY:
                return_link = '/cadastros_gerais_unidades_federativas'
                error_name = 'Esse pais ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.commit()
            return redirect('/cadastros_gerais_unidades_federativas')
        except:
            error_name = 'Ocorreu um erro ao alterar esse pais!'
            return_link = '/cadastros_gerais_unidades_federativas'
            return render_template('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template('cadastros_gerais/cadastro_uf_update.html', country=country)


#CADASTRAR UM ESTADO DENTRO DO PAÍS 
@app.route('/cadastros_gerais_unidades_federativas_cadastrar_estado/<int:ID_COUNTRY>', methods=['GET', 'POST'])
def cadastros_gerais_unidades_federativas_cadastrar_estado(ID_COUNTRY): 
    country = data.DB_COUNTRY.query.get_or_404(ID_COUNTRY)
    estates = data.DB_ESTATE.query.order_by(data.DB_ESTATE.NAME).all()
    if request.method == 'POST':
        str_name = request.form['name']
        new_input = data.DB_ESTATE(NAME=str_name, ID_BD_COUNTRY=ID_COUNTRY)
        for state in estates:
            if state.ID_BD_COUNTRY == ID_COUNTRY and str_name.lower() in state.NAME.lower():
                return_link = '/cadastros_gerais_unidades_federativas'
                error_name = 'Esse estado ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect(f'/cadastros_gerais_unidades_federativas_cadastrar_estado/{ID_COUNTRY}')
        except:
            error_name = 'Ocorreu um erro ao cadastrar esse estado!'
            return_link = '/cadastros_gerais_unidades_federativas'
            return render_template('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template('cadastros_gerais/cadastro_uf_estado.html', country=country, estates=estates)


#DELETAR O ESTADO
@app.route('/cadastros_gerais_unidades_federativas_deletar_estado/<int:ID_ESTATE>/<int:ID_COUNTRY>')
def cadastros_gerais_unidades_federativas_deletar_estado(ID_ESTATE, ID_COUNTRY):
    estate_to_delete = data.DB_ESTATE.query.get_or_404(ID_ESTATE)
    try:
        db.session.delete(estate_to_delete)
        db.session.commit()
        return redirect(f'/cadastros_gerais_unidades_federativas_cadastrar_estado/{ID_COUNTRY}')
    except:
        error_name = 'Ocorreu um erro ao alterar esse estado!'
        return_link = 'cadastros_gerais/cadastro_uf_estado'
        return render_template('/erro.html', return_link=return_link, error_name=error_name)



#ATUALIZAR O ESTADO CADASTRADO
@app.route('/cadastros_gerais_unidades_federativas_update_estado/<int:ID_ESTATE>/<int:ID_COUNTRY>', methods=['GET', 'POST'])
def cadastros_gerais_unidades_federativas_update_estado(ID_ESTATE, ID_COUNTRY):
    estate = data.DB_ESTATE.query.get_or_404(ID_ESTATE)
    country = data.DB_COUNTRY.query.get_or_404(ID_COUNTRY)
    if request.method == 'POST':
        states = data.DB_ESTATE.query.all()
        estate.NAME = request.form['name']
        for state in states:
            if estate.NAME.lower() in state.NAME.lower() and state.ID != ID_ESTATE:
                    return_link = '/cadastros_gerais_unidades_federativas'
                    error_name = 'Esse estado ja foi cadastrado!'
                    return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.commit()
            return redirect(f'/cadastros_gerais_unidades_federativas_cadastrar_estado/{ID_COUNTRY}')
        except:
            error_name = 'Ocorreu um erro ao alterar esse estado!'
            return_link = 'cadastros_gerais/cadastro_uf_estado'
            return render_template('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template('cadastros_gerais/cadastro_uf_update_estado.html', estate=estate, country=country)


#CADASTRAR UMA CIDADE DENTRO DO ESTADO 
@app.route('/cadastros_gerais_unidades_federativas_cadastrar_cidade/<int:ID_ESTATE>/<int:ID_COUNTRY>', methods=['GET', 'POST'])
def cadastros_gerais_unidades__cadastrar_cidade(ID_ESTATE, ID_COUNTRY):
    estate = data.DB_ESTATE.query.get_or_404(ID_ESTATE)
    country = data.DB_COUNTRY.query.get_or_404(ID_COUNTRY)
    cityes = data.DB_CITY.query.order_by(data.DB_CITY.NAME).all()
    if request.method == 'POST':
        str_name = request.form['name']
        new_input = data.DB_CITY(NAME=str_name, ID_BD_ESTATE=ID_ESTATE)
        for city in cityes:
                if city.ID_BD_ESTATE == ID_ESTATE and str_name.lower() == city.NAME.lower():
                    return_link = '/cadastros_gerais_unidades_federativas'
                    error_name = 'Essa cidade ja foi cadastrada!'
                    return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect(f'/cadastros_gerais_unidades_federativas_cadastrar_cidade/{ID_ESTATE}/{ID_COUNTRY}')
        except:
            error_name = 'Ocorreu um erro ao cadastrar essa cidade!'
            return_link = '/cadastros_gerais_unidades_federativas'
            return render_template('/erro.html', return_link=return_link, error_name=error_name)

    else:
        return render_template('cadastros_gerais/cadastro_uf_cidade.html', estate=estate, cityes=cityes, country=country)


#DELETAR A CIDADE
@app.route('/cadastros_gerais_unidades_federativas_deletar_cidade/<int:ID_CITY>/<int:ID_ESTATE>/<int:ID_COUNTRY>')
def cadastros_gerais_unidades_federativas_deletar_cidado(ID_CITY,ID_ESTATE,ID_COUNTRY):
    city_to_delete = data.DB_CITY.query.get_or_404(ID_CITY)
    try:
        db.session.delete(city_to_delete)
        db.session.commit()
        return redirect(f'/cadastros_gerais_unidades_federativas_cadastrar_cidade/{ID_ESTATE}/{ID_COUNTRY}')
    except:
        error_name = 'Ocorreu um erro ao deletar essa cidade!'
        return_link = '/cadastros_gerais_unidades_federativas'
        return render_template('/erro.html', return_link=return_link, error_name=error_name)


#ATUALIZAR A CIDADE 
@app.route('/cadastros_gerais_unidades_federativas_update_cidade/<int:ID_CITY>/<int:ID_ESTATE>/<int:ID_COUNTRY>', methods=['GET', 'POST'])
def cadastros_gerais_unidades_federativas_update_cidade(ID_CITY, ID_ESTATE, ID_COUNTRY):
    city = data.DB_CITY.query.get_or_404(ID_CITY)
    estate = data.DB_ESTATE.query.get_or_404(ID_ESTATE)
    country = data.DB_COUNTRY.query.get_or_404(ID_COUNTRY)
    cityes = data.DB_CITY.query.all()
    if request.method == 'POST':
        city.NAME = request.form['name']
        for citi in cityes:
                 if city.NAME.lower() in citi.NAME.lower() and city.NAME.lower() == citi.NAME.lower() and citi.ID != ID_CITY:
                    return_link = '/cadastros_gerais_unidades_federativas'
                    error_name = 'Essa cidade ja foi cadastrada!'
                    return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.commit()
            return redirect(f'/cadastros_gerais_unidades_federativas_cadastrar_cidade/{ID_ESTATE}/{ID_COUNTRY}')
        except:
            error_name = 'Ocorreu um erro ao alterar essa cidade!'
            return_link = 'cadastros_gerais/cadastros_uf_cidade'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template('cadastros_gerais/cadastro_uf_update_cidade.html', city=city, estate=estate, country=country)


#CADASTRAR UNIDADES DE MEDIDAS
@app.route('/cadastros_gerais_unidades_de_medidas_cadastrar', methods=['POST', 'GET'])
def cadastros_gerais_unidades_de_medidas_cadastrar():
    if request.method == 'POST':
        str_name = request.form['name']
        str_abreviation = request.form['abreviation']
        new_input = data.DB_MEASURES(NAME=str_name, ABREVIATION=str_abreviation)
        measures = data.DB_MEASURES.query.all()
        try:
            for measure in measures:
                if str_name.lower() == measure.NAME.lower():
                    return_link = '/cadastros_gerais_unidades_de_medidas'
                    error_name = 'Essa unidade de medida ja foi cadastrado!'
                    return render_template('/erro.html',return_link=return_link ,error_name=error_name)
            db.session.add(new_input)
            db.session.commit()
            return redirect('/cadastros_gerais_unidades_de_medidas_cadastrar')
        except: 
            error_name = 'Ocorreu um erro ao cadastrar essa unidade de medida!'
            return_link = '/cadastros_gerais_unidades_de_medidas'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return redirect('/cadastros_gerais_unidades_de_medidas')


#DELETAR UNIDADES DE MEDIDAS
@app.route('/cadastros_gerais_unidades_de_medidas_deletar/<int:ID>')
def cadastros_gerais_unidades_de_medidas_deletar(ID):
    measure_to_delete = data.DB_MEASURES.query.get_or_404(ID)
    try:
        db.session.delete(measure_to_delete)
        db.session.commit()
        return redirect('/cadastros_gerais_unidades_de_medidas')
    except: 
        error_name = 'Ocorreu um erro ao deletar essa unidade de medida!'
        return_link = '/cadastros_gerais_unidades_de_medidas.html'
        return render_template('/erro.html', return_link=return_link, error_name=error_name)


#ALTERAR UNIDADES DE MEDIDA
@app.route('/cadastros_gerais_unidades_de_medidas_update/<int:ID>', methods=['GET', 'POST'])
def cadastros_gerais_unidades_de_medidas_update(ID):
    measure = data.DB_MEASURES.query.get_or_404(ID)
    measures = data.DB_MEASURES.query.all()
    if request.method == 'POST':
        measure.NAME = request.form['name']
        measure.ABREVIATION = request.form['abreviation']
        for measur in measures:
                    if measure.NAME.lower() in measur.NAME.lower() and measure.NAME.lower() == measur.NAME.lower() and measur.ID != ID:               
                                return_link = '/cadastros_gerais_unidades_de_medidas'
                                error_name = 'Essa unidade de medida ja foi cadastrada!'
                                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.commit()
            return redirect('/cadastros_gerais_unidades_de_medidas')
        except:
            error_name = 'Ocorreu um erro ao alterar essa unidade de medida!'
            return_link = '/cadastros_gerais_unidades_de_medidas'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template('cadastros_gerais/cadastro_um_update.html', measure=measure)
        

#CADASTRANDO GRUPOS DE PRODUTOS
@app.route('/cadastros_gerais_grupos_de_produtos_cadastrar', methods=['POST', 'GET'])
def cadastros_gerais_grupos_de_produtos_cadastrar():
    groups = data.DB_GROUP.query.all()
    if request.method == 'POST':
        str_name = request.form['name']
        new_input = data.DB_GROUP(NAME=str_name)
        for group in groups:
            if str_name.lower() == group.NAME.lower():
                return_link = '/cadastros_gerais_grupos_de_produtos'
                error_name = 'Esse grupo ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect('/cadastros_gerais_grupos_de_produtos')
        except: 
            error_name = 'Ocorreu um erro ao cadastrar esse grupo de produtos!'
            return_link = '/cadastros_gerais_grupos_de_produtos'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)    
    else:
        
        return redirect('/cadastros_gerais_grupos_de_produtos')


#DELETANDO GRUPOS DE PRODUTOS
@app.route('/cadastros_grupos_de_produtos_deletar/<int:ID>')
def cadastros_gerais_grupos_de_produtos_deletar(ID):
    group_to_delete = data.DB_GROUP.query.get_or_404(ID)
    try:
        db.session.delete(group_to_delete)
        db.session.commit()
        return redirect('/cadastros_gerais_grupos_de_produtos')
    except:
        error_name = 'Ocorreu um erro ao deletar esse grupo produto!'
        return_link = '/cadastros_gerais_grupo_de_produtos.html'
        return render_template('/erro.html', return_link=return_link, error_name=error_name)


#ALTERANDO GRUPOS DE PRODUTOS
@app.route('/cadastros_gerais_grupos_de_produtos_update/<int:ID>', methods=['GET', 'POST'])
def cadastros_gerais_grupos_de_produtos_update(ID):
    group = data.DB_GROUP.query.get_or_404(ID)
    groups = data.DB_GROUP.query.all()
    if request.method == 'POST':
        group.NAME = request.form['name']
        for groupi in groups:
            if group.NAME.lower() in groupi.NAME.lower() and group.NAME.lower() == groupi.NAME.lower() and groupi.ID != ID:
                return_link = '/cadastros_gerais_grupos_de_produtos'
                error_name = 'Esse grupo ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.commit()
            return redirect('/cadastros_gerais_grupos_de_produtos')
        except:
            error_name = 'Ocorreu um erro ao alterar esse grupo de produtos!'
            return_link = '/cadastros_gerais_grupos_de_produtos'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)    
    else:
        return render_template('cadastros_gerais/cadastro_gruposprodutos_update.html', group=group)
        

#CADASTRANDO TIPOS DE PRODUTOS
@app.route('/cadastros_gerais_tipos_de_produtos_cadastrar', methods=['POST', 'GET'])
def cadastros_gerais_tipos_de_produtos_cadastrar():
    if request.method == 'POST':
        str_name = request.form['name']
        str_abreviation = request.form['abreviation']
        new_input = data.DB_PRODUCT_TYPE(NAME=str_name, ABREVIATION=str_abreviation)
        pts = data.DB_PRODUCT_TYPE.query.all()
        for pt in pts:
            if str_name.lower() == pt.NAME.lower():
                return_link = '/cadastros_gerais_tipos_de_produtos'
                error_name = 'Esse tipo de produto ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect('/cadastros_gerais_tipos_de_produtos')
        except: 
            error_name = 'Ocorreu um erro ao cadastrar esse tipo de produtos!'
            return_link = '/cadastros_gerais_tipos_de_produtos'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)    
    else:
        return redirect('/cadastros_gerais_tipos_de_produtos')


#DELETANDO TIPOS DE PRODUTOS
@app.route('/cadastros_gerais_tipos_de_produtos_deletar/<int:ID>')
def cadastros_gerais_tipos_de_produtos_deletar(ID):
    type_to_delete = data.DB_PRODUCT_TYPE.query.get_or_404(ID)
    try:
        db.session.delete(type_to_delete)
        db.session.commit()
        return redirect('/cadastros_gerais_tipos_de_produtos')
    except: 
        error_name = 'Ocorreu um erro ao deletar esse tipo de produto!'
        return_link = '/cadastros_gerais_grupo_de_produtos.html'
        return render_template('/erro.html', return_link=return_link, error_name=error_name)

#ALTERANDO TIPOS DE PRODUTOS
@app.route('/cadastros_gerais_tipos_de_produtos_update/<int:ID>', methods=['GET', 'POST'])
def cadastros_gerais_tipos_de_produtos_update(ID):
    type = data.DB_PRODUCT_TYPE.query.get_or_404(ID)
    if request.method == 'POST':
        type.NAME = request.form['name']
        type.ABREVIATION = request.form['abreviation']
        pts = data.DB_PRODUCT_TYPE.query.all()
        for pt in pts:
                if type.NAME.lower() in pt.NAME.lower() and type.NAME.lower() == pt.NAME.lower() and pt.ID != ID:
                    return_link = '/cadastros_gerais_tipos_de_produtos'
                    error_name = 'Esse tipo de produto ja foi cadastrado!'
                    return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.commit()
            return redirect('/cadastros_gerais_tipos_de_produtos')
        except:
            error_name = 'Ocorreu um erro ao alterar esse grupo de produtos!'
            return_link = '/cadastros_gerais_tipos_de_produtos'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)    
    else:
        return render_template('cadastros_gerais/cadastro_tiposprodutos_update.html', type=type)
        


# ================== AQUI ACABA OS CADASTROS GERAIS ==================


# ================== AQUI COMEÇA O CADASTRO ENTIDADES ==================


#CADASTRANDO ENCARGOS E SALARIOS
@app.route('/cadastros_de_entidades_encargos_e_salarios_cadastros', methods=['POST', 'GET'])
def cadastros_de_entidades_encargos_e_salarios_cadastras():
    if request.method == 'POST':
        str_name = request.form['name']
        float_rent = request.form['rent']
        new_input = data.DB_JOB(NAME=str_name, RENT=float_rent)
        jobs = data.DB_JOB.query.all()
        try:
            for job in jobs:
                if str_name.lower() == job.NAME.lower():
                    return_link = '/cadastros_de_entidades_encargos_e_salarios'
                    error_name = 'Esse encargo já foi cadastrado!'
                    return render_template('/erro.html',return_link=return_link ,error_name=error_name)
            db.session.add(new_input)
            db.session.commit()
            return redirect('/cadastros_de_entidades_encargos_e_salarios')
        except: 
            error_name = 'Ocorreu um erro ao cadastrar as entidades.'
            return_link = '/cadastros_de_entidades_encargos_e_salarios'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)  
    else:
        return redirect('/cadastros_de_entidades_encargos_e_salarios')


#DELETANDO ENCARGOS E SALARIOS
@app.route('/cadastros_de_entidades_encargos_e_salarios_deletar/<int:ID>')
def cadastros_de_entidades_encargos_e_salarios_deletar(ID):
    job_to_delete = data.DB_JOB.query.get_or_404(ID)
    try:
        db.session.delete(job_to_delete)
        db.session.commit()
        return redirect('/cadastros_de_entidades_encargos_e_salarios')
    except:
        error_name = 'Ocorreu um erro ao deletar encargos e salários!'
        return_link = '/cadastros_de_entidades_encargos_e_salarios'
        return render_template('/erro.html', return_link=return_link, error_name=error_name)


#ALTERANDO ENCARGOS E SALARIOS
@app.route('/cadastros_de_entidades_encargos_e_salarios_update/<int:ID>', methods=['GET', 'POST'])
def cadastros_de_entidades_encargos_e_salarios_update(ID):
    job = data.DB_JOB.query.get_or_404(ID)
    jobs = data.DB_JOB.query.all()
    if request.method == 'POST':
        job.NAME = request.form['name']
        job.RENT = request.form['rent']
        for jobi in jobs:
            if job.NAME.lower() in jobi.NAME.lower() and job.NAME.lower() == jobi.NAME.lower() and jobi.ID != ID:
                return_link = '/cadastros_de_entidades_encargos_e_salarios'
                error_name = 'Esse encargo já foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.commit()
            return redirect('/cadastros_de_entidades_encargos_e_salarios')
        except:
            error_name = 'Ocorreu um erro ao alterar as entidades.'
            return_link = '/cadastros_de_entidades_encargos_e_salarios'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)  
    else:
        return render_template('cadastros_entidades/cadastro_encargos_update.html', job=job)


#CADASTRANDO COLABORADORES 
@app.route('/cadastros_de_entidades_colaboradores_cadastros', methods=['POST', 'GET'])
def cadastros_de_entidades_colaboradores_cadastros():
    if request.method == 'POST':
        str_name = request.form['name']
        int_id_bd_job = request.form['id_bd_job']
        int_id_bd_country = request.form['id_bd_country']
        int_id_bd_estate = request.form['id_bd_estate']
        int_id_bd_city = request.form['id_bd_city']
        str_district = request.form['district']
        str_road = request.form['road']
        int_number = request.form['number']
        str_complement = request.form['complement']
        str_cep = request.form['cep']
        date_born_date = datetime.strptime(request.form['born_date'], '%Y-%m-%d')
        date_admission_date = datetime.strptime(request.form['admission_date'], '%Y-%m-%d')
        mail_email = request.form['email']
        str_phone = request.form['phone']
        int_cpf = request.form['cpf']
        int_rg = request.form['rg']
        int_pis = request.form['pis']
        new_input = data.DB_WORKERS(NAME=str_name, ID_BD_JOB=int_id_bd_job, ID_BD_COUNTRY=int_id_bd_country, ID_BD_ESTATE=int_id_bd_estate, ID_BD_CITY=int_id_bd_city,
                                DISTRICT=str_district, ROAD=str_road, NUMBER=int_number, COMPLEMENT=str_complement, CEP=str_cep, BORN_DATE=date_born_date,
                                 ADMISSION_DATE=date_admission_date, EMAIL=mail_email, PHONE=str_phone, CPF=int_cpf, RG=int_rg, PIS=int_pis, ACTIVE=1 )
        names = data.DB_WORKERS.query.all()
        emails = data.DB_WORKERS.query.all()
        cpfs = data.DB_WORKERS.query.all()
        rgs = data.DB_WORKERS.query.all()
        spis = data.DB_WORKERS.query.all()
        for name in names:
            if str_name.lower() in name.NAME.lower() and str_name.lower() == name.NAME.lower():
                return_link = '/cadastros_de_entidades_colaboradores_cadastros'
                error_name = 'Esse nome ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        for email in emails:
            if mail_email.lower() in email.EMAIL.lower() and mail_email.lower() == email.EMAIL.lower():
                return_link = '/cadastros_de_entidades_colaboradores_cadastros'
                error_name = 'Esse email ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        for cpf in cpfs:
            if int_cpf.lower() in cpf.CPF.lower() and int_cpf.lower() == cpf.CPF.lower():
                return_link = '/cadastros_de_entidades_colaboradores_cadastros'
                error_name = 'Esse CPF ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        for rg in rgs:
            if int_rg.lower() in rg.RG.lower() and int_rg.lower() == rg.RG.lower():
                return_link = '/cadastros_de_entidades_colaboradores_cadastros'
                error_name = 'Esse RG ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        for pis in spis:
            if int_pis.lower() in pis.PIS.lower() and int_pis.lower() == pis.PIS.lower():
                return_link = '/cadastros_de_entidades_colaboradores_cadastros'
                error_name = 'Esse PIS ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect('/cadastros_de_entidades_colaboradores')
        except Exception :
            error_name = 'Ocorreu um erro ao cadastrar colaboradores' 
            return_link = '/cadastros_de_entidades_colaboradores'
            return redirect('/templates/erro.html', return_link=return_link, error_name=error_name)
    else:
        return redirect('/cadastros_de_entidades_colaboradores')


#DELETANDO COLABORADORES
@app.route('/cadastros_de_entidades_colaboradores_deletar/<int:ID>')
def cadastros_de_entidades_colaboradores_deletar(ID):
    worker_to_delete = data.DB_WORKERS.query.get_or_404(ID)
    try:
        db.session.delete(worker_to_delete)
        db.session.commit()
        return redirect('/cadastros_de_entidades_colaboradores')
    except:
            error_name = 'Ocorreu um erro ao deletar colaboradores' 
            return_link = '/cadastros_de_entidades_colaboradores'
            return redirect('/templates/erro.html', return_link=return_link, error_name=error_name)


#ALTERANDO COLABORADORES
@app.route('/cadastros_de_entidades_colaboradores_update/<int:ID>', methods=['GET', 'POST'])
def cadastros_de_entidades_colaboradores_update(ID):
    worker = data.DB_WORKERS.query.get_or_404(ID)
    jobs = data.DB_JOB.query.order_by(data.DB_JOB.NAME).all()
    countryes = data.DB_COUNTRY.query.order_by(data.DB_COUNTRY.NAME).all()
    estates = data.DB_ESTATE.query.order_by(data.DB_ESTATE.NAME).all()
    cityes = data.DB_CITY.query.order_by(data.DB_CITY.NAME).all()
    if request.method == 'POST':
        worker.NAME = request.form['name']
        worker.ID_BD_JOB = request.form['id_bd_job']
        worker.ID_BD_COUNTRY = request.form['id_bd_country']
        worker.ID_BD_ESTATE = request.form['id_bd_estate']
        worker.ID_BD_CITY = request.form['id_bd_city']
        worker.DISTRICT = request.form['district']
        worker.ROAD = request.form['road']
        worker.NUMBER = request.form['number']
        worker.COMPLEMENT = request.form['complement']
        worker.CEP = request.form['cep']
        worker.BORN_DATE = datetime.strptime(request.form['born_date'], '%Y-%m-%d')
        worker.ADMISSION_DATE = datetime.strptime(request.form['admission_date'], '%Y-%m-%d')
        worker.EMAIL = request.form['email']
        worker.PHONE = request.form['phone']
        worker.CPF = request.form['cpf']
        worker.RG = request.form['rg']
        worker.PIS = request.form['pis']
        worker.ACTIVE = request.form['active']
        names = data.DB_WORKERS.query.all()
        emails = data.DB_WORKERS.query.all()
        cpfs = data.DB_WORKERS.query.all()
        rgs = data.DB_WORKERS.query.all()
        spis = data.DB_WORKERS.query.all()
        for name in names:
            if worker.NAME.lower() in name.NAME.lower() and worker.NAME.lower() == name.NAME.lower() and name.ID != ID:
                return_link = '/cadastros_de_entidades_colaboradores_cadastros'
                error_name = 'Esse nome ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        for email in emails:
            if worker.EMAIL.lower() in email.EMAIL.lower() and worker.EMAIL.lower() == email.EMAIL.lower() and email.ID != ID:
                return_link = '/cadastros_de_entidades_colaboradores_cadastros'
                error_name = 'Esse email ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        for cpf in cpfs:
            if worker.CPF.lower() in cpf.CPF.lower() and worker.CPF.lower() == cpf.CPF.lower() and cpf.ID != ID:
                return_link = '/cadastros_de_entidades_colaboradores_cadastros'
                error_name = 'Esse CPF ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        for rg in rgs:
            if worker.RG.lower() in rg.RG.lower() and worker.RG.lower() == rg.RG.lower() and rg.ID != ID:
                return_link = '/cadastros_de_entidades_colaboradores_cadastros'
                error_name = 'Esse RG ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        for pis in spis:
            if worker.PIS.lower() in pis.PIS.lower() and worker.PIS.lower() == pis.PIS.lower() and pis.ID != ID:
                return_link = '/cadastros_de_entidades_colaboradores_cadastros'
                error_name = 'Esse PIS ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.commit()
            return redirect('/cadastros_de_entidades_colaboradores')
        except:
            error_name = 'Ocorreu um erro ao cadastrar colaboradores!' 
            return_link = '/cadastros_de_entidades_colaboradores'
            return redirect('/templates/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template('cadastros_entidades/cadastro_colaboradores_update.html', worker=worker, jobs=jobs, countryes=countryes, estates=estates, cityes=cityes)




#CADASTRANDO FORNECEDORES
@app.route('/cadastros_de_entidades_fornecedores_cadastros', methods=['POST', 'GET'])
def cadastros_de_entidades_fornecedores_cadastros():
    if request.method == 'POST':
        str_name = request.form['name']
        int_id_bd_country = request.form['id_bd_country']
        int_id_bd_estate = request.form['id_bd_estate']
        int_id_bd_city = request.form['id_bd_city']
        str_district = request.form['district']
        str_road = request.form['road']
        int_number = request.form['number']
        str_complement = request.form['complement']
        str_cep = request.form['cep']
        mail_email = request.form['email']
        str_phone = request.form['phone']
        int_cnpj = request.form['cnpj']
        new_input = data.DB_SUPPLIER(NAME=str_name, ID_BD_COUNTRY=int_id_bd_country, ID_BD_ESTATE=int_id_bd_estate, ID_BD_CITY=int_id_bd_city,
                                DISTRICT=str_district, ROAD=str_road, NUMBER=int_number, COMPLEMENT=str_complement, CEP=str_cep,
                                EMAIL=mail_email, PHONE=str_phone, CNPJ=int_cnpj, ACTIVE=1 )
        names = data.DB_SUPPLIER.query.all()
        emails = data.DB_SUPPLIER.query.all()
        cnpjs = data.DB_SUPPLIER.query.all()
        for name in names:
            if str_name.lower() in name.NAME.lower() and str_name.lower() == name.NAME.lower():
                return_link = '/cadastros_de_entidades_fornecedores_cadastros'
                error_name = 'Esse nome ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        for email in emails:
            if mail_email.lower() in email.EMAIL.lower() and mail_email.lower() == email.EMAIL.lower():
                return_link = '/cadastros_de_entidades_fornecedores_cadastros'
                error_name = 'Esse email ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        for cnpj in cnpjs:
            if int_cnpj.lower() in cnpj.CNPJ.lower() and int_cnpj.lower() == cnpj.CNPJ.lower():
                return_link = '/cadastros_de_entidades_fornecedores_cadastros'
                error_name = 'Esse CNPJ ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect('/cadastros_de_entidades_fornecedores')
        except Exception as e: 
            print(str(e))  # Print the error message
            return 'An error occurred while saving your data: ' + str(e)
    else:
        return redirect('/cadastros_de_entidades_fornecedores')


#DELETANDO FORNECEDORES
@app.route('/cadastros_de_entidades_fornecedores_deletar/<int:ID>')
def cadastros_de_entidades_fornecedores_deletar(ID):
    worker_to_delete = data.DB_SUPPLIER.query.get_or_404(ID)
    try:
        db.session.delete(worker_to_delete)
        db.session.commit()
        return redirect('/cadastros_de_entidades_fornecedores')
    except:
            error_name = 'Ocorreu um erro ao deletar fornecedores!' 
            return_link = '/cadastros_de_entidades_fornecedores_cadastros'
            return redirect('/templates/erro.html', return_link=return_link, error_name=error_name)


#ALTERANDO FORNECEDORES
@app.route('/cadastros_de_entidades_fornecedores_update/<int:ID>', methods=['GET', 'POST'])
def cadastros_de_entidades_fornecedores_update(ID):
    supplier = data.DB_SUPPLIER.query.get_or_404(ID)
    countryes = data.DB_COUNTRY.query.order_by(data.DB_COUNTRY.NAME).all()
    estates = data.DB_ESTATE.query.order_by(data.DB_ESTATE.NAME).all()
    cityes = data.DB_CITY.query.order_by(data.DB_CITY.NAME).all()
    if request.method == 'POST':
        supplier.NAME = request.form['name']
        supplier.ID_BD_COUNTRY = request.form['id_bd_country']
        supplier.ID_BD_ESTATE = request.form['id_bd_estate']
        supplier.ID_BD_CITY = request.form['id_bd_city']
        supplier.DISTRICT = request.form['district']
        supplier.ROAD = request.form['road']
        supplier.NUMBER = request.form['number']
        supplier.COMPLEMENT = request.form['complement']
        supplier.CEP = request.form['cep']
        supplier.EMAIL = request.form['email']
        supplier.PHONE = request.form['phone']
        supplier.CNPJ = request.form['cnpj']
        supplier.ACTIVE = request.form['active']
        names = data.DB_SUPPLIER.query.all()
        emails = data.DB_SUPPLIER.query.all()
        cnpjs = data.DB_SUPPLIER.query.all()
        for name in names:
            if supplier.NAME.lower() in name.NAME.lower() and supplier.NAME.lower() == name.NAME.lower() and name.ID != ID:
                return_link = '/cadastros_de_entidades_fornecedores'
                error_name = 'Esse nome ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        for email in emails:
            if supplier.EMAIL.lower() in email.EMAIL.lower() and supplier.EMAIL.lower() == email.EMAIL.lower() and email.ID != ID:
                return_link = '/cadastros_de_entidades_fornecedores'
                error_name = 'Esse email ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        for cnpj in cnpjs:
            if supplier.CNPJ.lower() in cnpj.CNPJ.lower() and supplier.CNPJ.lower() == cnpj.CNPJ.lower() and cnpj.ID != ID:
                return_link = '/cadastros_de_entidades_fornecedores'
                error_name = 'Esse CNPJ ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.commit()
            return redirect('/cadastros_de_entidades_fornecedores')
        except:
            error_name = 'Ocorreu um erro ao alterar fornecedores!' 
            return_link = '/cadastros_de_entidades_fornecedores'
            return redirect('/templates/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template('cadastros_entidades/cadastro_fornecedores_update.html', supplier=supplier, countryes=countryes, estates=estates, cityes=cityes)





# ================== AQUI ACABA OS CADASTROS DE ENTIDADES ==================


# ================== AQUI COMEÇA OS CADASTROS DE MATERIAIS ==================


#CADASTRANDO MATERIA PRIMA
@app.route('/cadastros_de_materiais_materia_prima_cadastros', methods=['POST', 'GET'])
def cadastros_de_materiais_materia_prima_cadastros():
    if request.method == 'POST':
        str_name = request.form['name']
        int_id_bd_measures = request.form['id_bd_measures']
        float_ipi = request.form['ipi']
        mps = data.DB_MP.query.all()
        new_input = data.DB_MP(NAME=str_name, ID_BD_MEASURES=int_id_bd_measures, IPI=float_ipi)
        for mp in mps:
                if str_name.lower() == mp.NAME.lower():
                    return_link = '/cadastros_de_materiais_materia_prima'
                    error_name = 'Essa materia prima ja foi cadastrada!'
                    return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect('/cadastros_de_materiais_materia_prima')
        except: 
            error_name = 'Ocorreu um erro ao cadastrar a matéria prima!' 
            return_link = '/cadastros_de_materiais_materia_prima'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return redirect('/cadastros_de_materiais_materia_prima')


#DELETANDO MATERIA PRIMA
@app.route('/cadastros_de_materiais_materia_prima_deletar/<int:ID>')
def cadastros_de_materiais_materia_prima_deletar(ID):
    mp_to_delete = data.DB_MP.query.get_or_404(ID)
    try:
        db.session.delete(mp_to_delete)
        db.session.commit()
        return redirect('/cadastros_de_materiais_materia_prima')
    except:
            error_name = 'Ocorreu um erro ao deletar a matéria prima!' 
            return_link = '/cadastros_de_materiais_materia_prima'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)


#ALTERANDO MATERIA PRIMA
@app.route('/cadastros_de_materiais_materia_prima_update/<int:ID>', methods=['GET', 'POST'])
def cadastros_de_materiais_materia_prima_update(ID):
    mp = data.DB_MP.query.get_or_404(ID)
    measures = data.DB_MEASURES.query.order_by(data.DB_MEASURES.NAME).all()
    mps = data.DB_MP.query.all()
    if request.method == 'POST':
        mp.NAME = request.form['name']
        mp.ID_BD_MEASURES = request.form['id_bd_measures']
        mp.IPI = request.form['ipi']
        for mpi in mps:
            if  mp.NAME.lower() in mpi.NAME.lower() and mp.NAME.lower() == mpi.NAME.lower() and mpi.ID != ID:
                return_link = '/cadastros_de_materiais_materia_prima'
                error_name = 'Esse tipo de produto ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.commit()
            return redirect('/cadastros_de_materiais_materia_prima')
        except:
            error_name = 'Ocorreu um erro ao alterar a matéria prima!' 
            return_link = '/cadastros_de_materiais_materia_prima'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template('cadastros_materiais/cadastro_mp_update.html', mp=mp, measures=measures)


#CADASTRANDO MATERIAL DE CONSUMO
@app.route('/cadastros_de_materiais_material_de_consumo_cadastros', methods=['POST', 'GET'])
def cadastros_de_materiais_material_de_consumo_cadastros():
    if request.method == 'POST':
        str_name = request.form['name']
        int_id_bd_measures = request.form['id_bd_measures']
        float_ipi = request.form['ipi']
        float_difal = request.form['difal']
        new_input = data.DB_MC(NAME=str_name, ID_BD_MEASURES=int_id_bd_measures, IPI=float_ipi, DIFAL=float_difal)
        mcs = data.DB_MC.query.all()
        for mc in mcs:
            if str_name.lower() == mc.NAME.lower():
                return_link = '/cadastros_de_materiais_material_de_consumo'
                error_name = 'Esse material de consumo ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect('/cadastros_de_materiais_material_de_consumo')
        except: 
            error_name = 'Ocorreu um erro ao cadastrar o material de consumo!' 
            return_link = '/cadastros_de_materiais_material_de_consumo_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return redirect('/cadastros_de_materiais_material_de_consumo')


#DELETANDO MATERIAL DE CONSUMO
@app.route('/cadastros_de_materiais_material_de_consumo_deletar/<int:ID>')
def cadastros_de_materiais_material_de_consumo_deletar(ID):
    mc_to_delete = data.DB_MC.query.get_or_404(ID)
    try:
        db.session.delete(mc_to_delete)
        db.session.commit()
        return redirect('/cadastros_de_materiais_material_de_consumo_cadastros')
    except:
            error_name = 'Ocorreu um erro ao deletar o material de consumo!' 
            return_link = '/cadastros_de_materiais_material_de_consumo_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)


#ALTERANDO MATERIAL DE CONSUMO
@app.route('/cadastros_de_materiais_material_de_consumo_update/<int:ID>', methods=['GET', 'POST'])
def cadastros_de_materiais_material_de_consumo_update(ID):
    mc = data.DB_MC.query.get_or_404(ID)
    measures = data.DB_MEASURES.query.order_by(data.DB_MEASURES.NAME).all()
    mcs = data.DB_MC.query.all()
    if request.method == 'POST':
        mc.NAME = request.form['name']
        mc.ID_BD_MEASURES = request.form['id_bd_measures']
        mc.IPI = request.form['ipi']
        mc.DIFAL = request.form['difal']
        for mci in mcs:
            if  mc.NAME.lower() in mci.NAME.lower() and mc.NAME.lower() == mci.NAME.lower() and mci.ID != ID:
                return_link = '/cadastros_de_materiais_material_de_consumo'
                error_name = 'Esse material de consumo ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.commit()
            return redirect('/cadastros_de_materiais_material_de_consumo')
        except:
            error_name = 'Ocorreu um erro ao alterar o material de consumo!' 
            return_link = '/cadastros_de_materiais_material_de_consumo_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template('cadastros_materiais/cadastro_mc_update.html', mc=mc, measures=measures)


#CADASTRANDO PRODUTOS
@app.route('/cadastros_de_materiais_produtos_cadastros', methods=['POST', 'GET'])
def cadastros_de_materiais_produtos_cadastros():
    if request.method == 'POST':
        str_name = request.form['name']
        str_cod = request.form['cod']
        int_id_bd_group = request.form['id_bd_group']
        new_input = data.DB_PROD(COD=str_cod, NAME=str_name, ID_BD_GROUP=int_id_bd_group)
        prods = data.DB_PROD.query.all()
        for prodi in prods:
            if str_name.lower() in prodi.NAME.lower() and str_name.lower() == prodi.NAME.lower():
                return_link = '/cadastros_de_materiais_produtos'
                error_name = 'Esse produto ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect('/cadastros_de_materiais_produtos')
        except: 
            error_name = 'Ocorreu um erro ao cadastrar o produto!' 
            return_link = '/cadastros_de_materiais_produtos_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return redirect('/cadastros_de_materiais_produtos')


#DELETANDO PRODUTOS
@app.route('/cadastros_de_materiais_produtos_deletar/<int:ID>')
def cadastros_de_materiais_produtos_deletar(ID):
    product_to_delete = data.DB_PROD.query.get_or_404(ID)
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('/cadastros_de_materiais_produtos')
    except:
            error_name = 'Ocorreu um erro ao deletar o produto!' 
            return_link = '/cadastros_de_materiais_produtos_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)


#ALTERANDO PRODUTOS
@app.route('/cadastros_de_materiais_produtos_update/<int:ID>', methods=['GET', 'POST'])
def cadastros_de_materiais_produtos_update(ID):
    product = data.DB_PROD.query.get_or_404(ID)
    products_mp = data.DB_PROD_MP.query.order_by(data.DB_PROD_MP.ID).all()
    products_mo = data.DB_PROD_MO.query.order_by(data.DB_PROD_MO.ID).all()
    products_mc = data.DB_PROD_MC.query.order_by(data.DB_PROD_MC.ID).all()
    groups = data.DB_GROUP.query.order_by(data.DB_GROUP.NAME).all()
    measures = data.DB_MEASURES.query.order_by(data.DB_MEASURES.NAME).all()
    mps = data.DB_MP.query.order_by(data.DB_MP.NAME).all()
    mcs = data.DB_MC.query.order_by(data.DB_MC.NAME).all()
    prods = data.DB_PROD.query.all()   
    if request.method == 'POST':
        product.NAME = request.form['name']
        product.ID_BD_GROUP = request.form['id_bd_group']
        product.COD = request.form['cod']
        for prod in prods:
            if product.NAME.lower() in prod.NAME.lower() and product.NAME.lower() == prod.NAME.lower() and prod.ID != ID:
                return_link = '/cadastros_de_materiais_produtos'
                error_name = 'Esse produto ja foi cadastrado!'
                return render_template('/erro.html',return_link=return_link ,error_name=error_name)
        try:
            db.session.commit()
            return redirect('/cadastros_de_materiais_produtos')
        except:
            error_name = 'Ocorreu um erro ao alterar o produto!' 
            return_link = '/cadastros_de_materiais_produtos_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template(f'cadastros_materiais/cadastro_produtos_update.html', product=product, groups=groups, mps=mps, mcs=mcs, measures=measures, 
                               products_mo=products_mo, products_mc=products_mc, products_mp=products_mp, get_db_mp=uful.get_db_mp, get_db_mc=uful.get_db_mc
                               ,  get_product_measure=uful.get_product_measure, get_measureabv=uful.get_measureabv)


#CADASTRANDO MATÉRIA PRIMA NOS PRODUTOS
@app.route('/cadastros_de_materiais_produtos_cadastros_mp/<int:ID>', methods=['POST', 'GET'])
def cadastros_de_materiais_produtos_cadastros_mp(ID):
    if request.method == 'POST':
        int_id_bd_prod = request.form['id_bd_prod']
        int_id_bd_mp = request.form['id_bd_mp']
        float_quantity = request.form['quantity']
        new_input = data.DB_PROD_MP(ID_BD_PROD=int_id_bd_prod, ID_BD_MP=int_id_bd_mp, QUANTITY=float_quantity)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect(f'/cadastros_de_materiais_produtos_update/{ID}')
        except: 
            error_name = 'Ocorreu um erro ao alterar a materia prima!' 
            return_link = '/cadastros_de_materiais_produtos_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return redirect(f'/cadastros_de_materiais_produtos_update/{ID}')


#DELETANDO MATÉRIA PRIMA NOS PRODUTOS
@app.route('/cadastros_de_materiais_produtos_deletar_mp/<int:ID_PROD>/<int:ID_PROD_MP>')
def cadastros_de_materiais_produtos_deletar_mp(ID_PROD, ID_PROD_MP):
    product_to_delete = data.DB_PROD_MP.query.get_or_404(ID_PROD_MP)
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect(f'/cadastros_de_materiais_produtos_update/{ID_PROD}')
    except:
            error_name = 'Ocorreu um erro ao deletar a materia prima!' 
            return_link = '/cadastros_de_materiais_produtos_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)


#ALTERANDO MATÉRIA PRIMA NOS PRODUTOS _---- esse precisa terminar -----____
@app.route('/cadastros_de_materiais_produtos_alterar_mp/<int:ID_PROD>/<int:ID_PROD_MP>', methods=['GET', 'POST'])
def cadastros_de_materiais_produtos_alterar_mp(ID_PROD,ID_PROD_MP):
    product = data.DB_PROD.query.get_or_404(ID_PROD)
    product_mp = data.DB_PROD_MP.query.get_or_404(ID_PROD_MP)
    if request.method == 'POST':
        product_mp.QUANTITY = request.form['quantity']
        try:
            db.session.commit()
            return redirect(f'/cadastros_de_materiais_produtos_update/{ID_PROD}')
        except:
            error_name = 'Ocorreu um erro ao alterar a materia prima!'
            return_link = '/cadastros_de_materiais_produtos_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template('cadastros_materiais/cadastro_produtos_mp_update.html', product_mp=product_mp, product=product)


#CADASTRANDO MATERIAL DE CONSUMO NOS PRODUTOS
@app.route('/cadastros_de_materiais_produtos_cadastros_mc/<int:ID>', methods=['POST', 'GET'])
def cadastros_de_materiais_produtos_cadastros_mc(ID):
    if request.method == 'POST':
        int_id_bd_prod = request.form['id_bd_prod']
        int_id_bd_mc = request.form['id_bd_mc']
        float_quantity = request.form['quantity']
        new_input = data.DB_PROD_MC(ID_BD_PROD=int_id_bd_prod, ID_BD_MC=int_id_bd_mc, QUANTITY=float_quantity)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect(f'/cadastros_de_materiais_produtos_update/{ID}')
        except: 
            error_name = 'Ocorreu um erro ao cadastrar os materiais dos produtos!'
            return_link = '/cadastros_de_materiais_produtos_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return redirect(f'/cadastros_de_materiais_produtos_update/{ID}')


#DELETANDO MATERIAL DE CONSUMO NOS PRODUTOS
@app.route('/cadastros_de_materiais_produtos_deletar_mc/<int:ID_PROD>/<int:ID_PROD_MC>')
def cadastros_de_materiais_produtos_deletar_mc(ID_PROD, ID_PROD_MC):
    product_to_delete = data.DB_PROD_MC.query.get_or_404(ID_PROD_MC)
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect(f'/cadastros_de_materiais_produtos_update/{ID_PROD}')
    except:
            error_name = 'Ocorreu um erro ao deletar os materiais dos produtos!'
            return_link = '/cadastros_de_materiais_produtos_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)


#ALTERANDO MATERIAL DE CONSUMO NOS PRODUTOS
@app.route('/cadastros_de_materiais_produtos_alterar_mc/<int:ID_PROD>/<int:ID_PROD_MC>', methods=['GET', 'POST'])
def cadastros_de_materiais_produtos_alterar_mc(ID_PROD,ID_PROD_MC):
    product = data.DB_PROD.query.get_or_404(ID_PROD)
    product_mc = data.DB_PROD_MC.query.get_or_404(ID_PROD_MC)
    if request.method == 'POST':
        product_mc.QUANTITY = request.form['quantity']
        try:
            db.session.commit()
            return redirect(f'/cadastros_de_materiais_produtos_update/{ID_PROD}')
        except:
            error_name = 'Ocorreu um erro ao alterar os materiais dos produtos!'
            return_link = '/cadastros_de_materiais_produtos_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template('cadastros_materiais/cadastro_produtos_mc_update.html', product_mc=product_mc, product=product)


#CADASTRANDO MÃO DE OBRA NOS PRODUTOS
@app.route('/cadastros_de_materiais_produtos_cadastros_mo/<int:ID>', methods=['POST', 'GET'])
def cadastros_de_materiais_produtos_cadastros_mo(ID):
    if request.method == 'POST':
        int_id_bd_prod = request.form['id_bd_prod']
        str_name = request.form['name']
        float_workers_quantity = request.form['workers_quantity']
        float_lot_ammount = request.form['lot_ammount']
        float_time_to_produce = request.form['time_to_produce']
        new_input = data.DB_PROD_MO(ID_BD_PROD=int_id_bd_prod, NAME=str_name, WORKERS_QUANTITY=float_workers_quantity, LOT_AMMOUNT=float_lot_ammount, TIME_TO_PRODUCE=float_time_to_produce)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect(f'/cadastros_de_materiais_produtos_update/{ID}')
        except: 
            error_name = 'Ocorreu um erro ao cadastrar a mao de obra!'
            return_link = '/cadastros_de_materiais_produtos_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return redirect(f'/cadastros_de_materiais_produtos_update/{ID}')


#DELETANDO MÃO DE OBRA NOS PRODUTOS
@app.route('/cadastros_de_materiais_produtos_deletar_mo/<int:ID_PROD>/<int:ID_PROD_MO>')
def cadastros_de_materiais_produtos_deletar_mo(ID_PROD, ID_PROD_MO):
    product_to_delete = data.DB_PROD_MO.query.get_or_404(ID_PROD_MO)
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect(f'/cadastros_de_materiais_produtos_update/{ID_PROD}')
    except:
            error_name = 'Ocorreu um erro ao deletar a mao de obra!'
            return_link = '/cadastros_de_materiais_produtos_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)


#ALTERANDO MÃO DE OBRA NOS PRODUTOS
@app.route('/cadastros_de_materiais_produtos_alterar_mo/<int:ID_PROD>/<int:ID_PROD_MO>', methods=['GET', 'POST'])
def cadastros_de_materiais_produtos_alterar_mo(ID_PROD,ID_PROD_MO):
    product = data.DB_PROD.query.get_or_404(ID_PROD)
    product_mo = data.DB_PROD_MO.query.get_or_404(ID_PROD_MO)
    if request.method == 'POST':
        product_mo.WORKERS_QUANTITY = request.form['workers_quantity']
        product_mo.LOT_AMMOUNT = request.form['lot_ammount']
        product_mo.TIME_TO_PRODUCE = request.form['time_to_produce']
        try:
            db.session.commit()
            return redirect(f'/cadastros_de_materiais_produtos_update/{ID_PROD}')
        except:
            error_name = 'Ocorreu um erro ao alterar a mao de obra!'
            return_link = '/cadastros_de_materiais_produtos_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template('cadastros_materiais/cadastro_produtos_mo_update.html', product_mo=product_mo, product=product)


#CADASTRANDO COMPRAS
@app.route('/movimentacoes_compras_cadastros', methods=['POST', 'GET'])
def movimentacoes_compras_cadastros():
    if request.method == 'POST':
        int_id_bd_product_type = request.form['id_bd_product_type']
        int_id_bd_prod = request.form['id_bd_prod']
        int_id_bd_supplier = request.form['id_bd_supplier']
        date_nf_data = datetime.strptime(request.form['nf_data'], '%Y-%m-%d')
        str_nf_number = request.form['nf_number']
        float_price = request.form['price']
        float_quantity = request.form['quantity']
        float_transport_cost = request.form['transport_cost']
        new_input = data.DB_PURCHASES(ID_BD_PRODUCT_TYPE=int_id_bd_product_type, ID_BD_PROD=int_id_bd_prod, ID_BD_SUPPLIER=int_id_bd_supplier,
                                      NF_DATA=date_nf_data, NF_NUMBER=str_nf_number, PRICE=float_price, QUANTITY=float_quantity, TRANSPORT_COST=float_transport_cost)
        try:
            db.session.add(new_input)
            db.session.commit()
            return redirect('/movimentacoes_compras')
        except: 
            error_name = 'Ocorreu um erro ao cadastrar as compras!'
            return_link = '/movimentacoes_compras_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return redirect('/movimentacoes_compras')


#DELETANDO COMPRAS
@app.route('/movimentacoes_compras_cadastros_deletar/<int:ID>')
def movimentacoes_compras_cadastros_deletar(ID):
    product_to_delete = data.DB_PURCHASES.query.get_or_404(ID)
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('/movimentacoes_compras')
    except:
            error_name = 'Ocorreu um erro ao deletar as compras!'
            return_link = '/movimentacoes_compras_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)


#ALTERANDO COMPRAS
@app.route('/movimentacoes_compras_cadastros_update/<int:ID>', methods=['GET', 'POST'])
def movimentacoes_compras_cadastros_update(ID):
    purchase = data.DB_PURCHASES.query.get_or_404(ID)
    if request.method == 'POST':
        purchase.NF_DATA = datetime.strptime(request.form['nf_data'], '%Y-%m-%d')
        purchase.NF_NUMBER = request.form['nf_number']
        purchase.PRICE = request.form['price']
        purchase.QUANTITY = request.form['quantity']
        purchase.TRANSPORT_COST = request.form['transport_cost']
        try:
            db.session.commit()
            return redirect('/movimentacoes_compras_cadastros')
        except:
            error_name = 'Ocorreu um erro ao alterar as compras!'
            return_link = '/movimentacoes_compras_cadastros'
            return redirect('/erro.html', return_link=return_link, error_name=error_name)
    else:
        return render_template('movimentacoes/movimentacao_compras_update.html', purchase=purchase
                               , get_product_info=uful.get_product_info, get_supplier_name=uful.get_supplier_name)


# Rotas Extras Para Filtros

# Selecionar Estado com Base da Informação de um País
@app.route('/get_states/<country_id>')
def get_states(country_id):
    states = data.DB_ESTATE.query.filter_by(ID_BD_COUNTRY=country_id).order_by(data.DB_ESTATE.NAME).all()
    states_data = [{'ID': state.ID, 'NAME': state.NAME} for state in states]
    return jsonify(states_data)


# Selecionar Cidade com Base em um Estado
@app.route('/get_cities/<state_id>')
def get_cities(state_id):
    """
    Retorna a lista de cidades para o script contido nos htmls.

    :param id_bd_mc: a chave da linha da base de dados
    :return: retorna informações da base de dados BD_MC de acordo com o ID.
    """
    cities = data.DB_CITY.query.filter_by(ID_BD_ESTATE=state_id).order_by(data.DB_CITY.NAME).all()
    cities_data = [{'ID': city.ID, 'NAME': city.NAME} for city in cities]
    return jsonify(cities_data)


# Essa Rota ira cadastrar o Brasil, Seus Estados e Municípios
@app.route('/cadastar_brasil')
def cadastrar_brasil():
    """
    Cadastra o Brasil, Seus estados e principais municípios
    """
    return first.cadastrar_brasil()


# Essa rota ira cadastrar as Opções Material de Consumo e Matéria Prima  
@app.route('/cadastrar_tiposdeprodutos')
def cadastrar_tiposdeprodutos():
    """
    Cadastra os dois principais tipos de produtos MC/MP
    """
    return first.cadastrar_tiposdeprodutos()




# o programa acaba aqui, apos essa linha apenas teste de debug
if __name__ == "__main__":
    app.run(debug=True)


# para rodar digitar no terminal "python IndustriaFeliz.py"