import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype
import os



modulepath = os.path.dirname(__file__)



def interest_columns_for_year(year):
    year = str(year)
    
    list_columns = pd.read_csv(os.path.join(modulepath, 'columns_to_load_each_year.csv'), sep=';')[year].dropna().values
    
    return list_columns


def interest_columns_for_year_treat(year):
    """
    From 'columns_to_load_each_year_treated.csv', gets the columns that must be loaded to create DataFrames with fewer attributes for better performance.
    The result of this function is usued as an argument when loading data with generate_rais_dataframe function from treat.py module. 
    """
    year = str(year)
    
    list_columns = pd.read_csv(os.path.join(modulepath, 'columns_to_load_each_year_treated.csv'), sep=';')[year].dropna().values
    
    return list_columns







list_column_keep_2010 = [
    'CBO Ocupação 2002'
    , 'CNAE 2.0 Classe'
    , 'CNAE 95 Classe'
    , 'Vínculo Ativo 31/12'
    , 'Faixa Etária'
    , 'Faixa Remun Dezem (SM)'
    , 'Faixa Remun Média (SM)'
    , 'Faixa Tempo Emprego'
    , 'Escolaridade após 2005'
    , 'Mun Trab'
    , 'Município'
    , 'Nacionalidade'
    , 'Natureza Jurídica'
    , 'Vl Remun Dezembro Nom'
    , 'Vl Remun Dezembro (SM)'
    , 'Vl Remun Média Nom'
    , 'Vl Remun Média (SM)'
    , 'CNAE 2.0 Subclasse'
    , 'Tamanho Estabelecimento'
    , 'Tipo Estab'
    , 'Tipo Estab.1'
    , 'Tipo Vínculo'
]

type_cat_tam_estabelecimento = CategoricalDtype(categories=[ -1, 1,  2,  3,  4,  5,  6,  7,  8,  9, 10], ordered=True)
type_cat_escolaridade = CategoricalDtype(categories=[ -1, 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11], ordered=True)
type_cat_faixa_etaria = CategoricalDtype(categories=['01', '02', '03', '04', '05', '06', '07', '08'], ordered=True)
type_cat_faixa_remu_media = CategoricalDtype(
    categories=[
        '00'
        ,'01'
        , '02'
        , '03'
        , '04'
        , '05'
        , '06'
        , '07'
        , '08'
        , '09'
        , '10'
        , '11'
    ]
    , ordered=True
)

type_cat_faixa_remu_media_dezembro = CategoricalDtype(
    categories=[
        '00'
        , '01'
        , '02'
        , '03'
        , '04'
        , '05'
        , '06'
        , '07'
        , '08'
        , '09'
        , '10'
        , '11'
        , '12'
    ]
    , ordered=True
)

type_cat_ind_tec = CategoricalDtype(
    categories=[
        'High-technology'
        , 'Medium-high-technology'
        , 'Medium-low-technology'
        , 'Low-technology'
        , 'Without Classification'
    ]
    , ordered=True
)


type_cat_know_services = CategoricalDtype(
    categories=[
        'High-tech knowledge-intensive services'
        , 'Knowledge-intensive financial services'
        , 'Knowledge-intensive market services'
        , 'Other knowledge-intensive services'
        , 'Less knowledge-intensive market services'
        , 'Other less knowledge-intensive services'
        , 'Without Classification'
    ]
    , ordered=True
)

type_cat_potec_grupo = CategoricalDtype(
    categories= ['Profissionais do Ensino', 'Engenheiros', 'Profissionais científicos', 'Pesquisadores', 'Diretores e Gerentes de P&D']    
        , ordered=True
)

type_cat_potec = CategoricalDtype(
    categories= ['Diretores e Gerentes de P&D'
                 ,'Engenheiros Mecatrônicos'
                 ,'Engenheiros Civis etc'
                 ,'Engenheiros agrônomos, de alimentos, florestais e de pesca'
                 ,'Pesquisadores'
                 ,'Biotecnologistas, geneticistas, pesquisadores em metrologia e especialistas em calibrações metereológicas'
                 ,'Matemáticos, estatísticos e afins'
                 ,'Profissionais da Informática'
                 ,'Físicos, químicos e afins'
                 ,'Biólogos e biomédicos'
                 ,'Professores de ensino Profissional'
                 ,'Professores de ensino superior'
                 ,'Demais Ocupações'
                ]    
        , ordered=True
)


dict_porte = {
    -1:'Ignorado'
    , 1:'Até 49'
    , 2:'Até 49'
    , 3:'Até 49'
    ,4:'Até 49'
    ,5:'Até 49'
    ,6:'de 50 a 99'
    ,7:'de 100 a 249'
    ,8:'de 250 a 499'
    ,9:'de 500 a 999'
    ,10:'a partir de 1000'
}


type_porte = CategoricalDtype(
    categories=[
        'Ignorado'
        ,'Até 49'
        ,'de 50 a 99'
        ,'de 100 a 249'
        ,'de 250 a 499'
        ,'de 500 a 999'
        ,'a partir de 1000'
    ]
    , ordered=True
)

dict_potec = {'Diretores e Gerentes de P&D':'Diretores e Gerentes de P&D'
              ,'Engenheiros Mecatrônicos':'Engenheiros'
              ,'Engenheiros Civis etc':'Engenheiros'
              ,'Engenheiros agrônomos, de alimentos, florestais e de pesca':'Engenheiros' 
              ,'Pesquisadores':'Pesquisadores'
              ,'Biotecnologistas, geneticistas, pesquisadores em metrologia e especialistas em calibrações metereológicas':'Profissionais científicos'
              ,'Matemáticos, estatísticos e afins':'Profissionais científicos'
              ,'Profissionais da Informática':'Profissionais científicos'
              ,'Físicos, químicos e afins':'Profissionais científicos'
              ,'Biólogos e biomédicos':'Profissionais científicos'
              ,'Professores de ensino Profissional':'Profissionais do Ensino'
              ,'Professores de ensino superior':'Profissionais do Ensino'
              ,'Demais Ocupações':'Demais Ocupações'
             }


dict_nat_jur={
    '1':'Administração Pública'
    ,'2':'Entidades Empresariais'
    ,'3':'Entidades sem Fins Lucrativos'
    ,'4':'Pessoas Físicas'
    ,'5':'Organizações Internacionais'
    ,'-':'Ignorado'
}



dict_nat_jur_detail = {
    '1015':'POD EXEC FE'
    ,'1023':'POD EXEC ES'
    ,'1031':'POD EXEC MU'
    ,'1040':'POD LEG FED'
    ,'1058':'POD LEG EST'
    ,'1066':'POD LEG MUN'
    ,'1074':'POD JUD FED'
    ,'1082':'POD JUD EST'
    ,'1104':'AUTARQ FED'
    ,'1112':'AUTARQ EST'
    ,'1120':'AUTARQ MUN'
    ,'1139':'FUNDAC FED'
    ,'1147':'FUNDAC EST'
    ,'1155':'FUNDAC MUN'
    ,'1163':'ORG AUT FED'
    ,'1171':'ORG AUT EST'
    ,'1180':'ORG AUT MUN'
    ,'1198':'COM POLINAC'
    ,'1201':'FUNDO PUBLIC'
    ,'1210':'ASSOC PUBLIC'
    ,'1228':'CONS PUB D PRIV'
    ,'1236':'UF'
    ,'1244':'MUN'
    ,'1252':'FUN PUB PRIV FED'
    ,'1260':'FUN PUB PRIV UF'
    ,'1279':'FUN PUB PRIV MUN'
    ,'2011':'EMP PUB'
    ,'2038':'SOC MISTA'
    ,'2046':'SA ABERTA'
    ,'2054':'SA FECH'
    ,'2062':'SOC QT LTDA'
    ,'2070':'SOC COLETV'
    ,'2089':'SOC COMD SM'
    ,'2097':'SOC COMD AC'
    ,'2127':'SOC CTA PAR'
    ,'2135':'FRM MER IND'
    ,'2143':'COOPERATIVA'
    ,'2151':'CONS EMPRES'
    ,'2160':'GRUP SOC'
    ,'2178':'FIL EMP EXT'
    ,'2194':'FIL ARG-BRA'
    ,'2216':'EMP DOM EXT'
    ,'2224':'FUN INVEST'
    ,'2232':'SOC SIMP PUR'
    ,'2240':'SOC SIMP LTD'
    ,'2259':'SOC SIMP COL'
    ,'2267':'SOC SIMP COM'
    ,'2275':'EMPR BINAC'
    ,'2283':'CONS EMPREG'
    ,'2291':'CONS SIMPLES'
    ,'2305':'EMP IND LTDA'
    ,'2313':'EMP IND SIMPLES'
    ,'3034':'CARTORIO'
    ,'3069':'OUT FUND PR'
    ,'3077':'SERV SOC AU'
    ,'3085':'CONDOMIN'
    ,'3107':'COM CONC'
    ,'3115':'ENT MED ARB'
    ,'3131':'ENT SOCIAL07'
    ,'3204':'FIL FUN EXT'
    ,'3212':'FUN DOM EXT'
    ,'3220':'ORG RELIG'
    ,'3239':'COMUN INDIG'
    ,'3247':'FUNDO PRIVAD'
    ,'3255':'PARTIDO'
    ,'3263':'PARTIDO'
    ,'3271':'PARTIDO'
    ,'3280':'PARTIDO'
    ,'3298':'FRENTE PLEB'
    ,'3301':'OS'
    ,'3999':'OUTR ORG'
    ,'4014':'EMP IND IMO'
    ,'4022':'SEG ESPEC'
    ,'4081':'CONTR IND07'
    ,'4090':'CAN CARG POL'
    ,'4111':'LEILOEIRO'
    ,'4120':'PROD RURAL'
    ,'5010':'ORG INTERNAC'
    ,'5029':'REPR DIPL ES'
    ,'5037':'OUT INST EXT'
    ,'-1':'INGNORADO'  
}


dict_escolaridade = {
    -1:'Não-Superior'
    ,1:'Não-Superior'
    ,2:'Não-Superior'
    ,3:'Não-Superior'
    ,4:'Não-Superior'
    ,5:'Não-Superior'
    ,6:'Não-Superior'
    ,7:'Não-Superior'
    ,8:'Não-Superior'
    ,9:'Superior'
    ,10:'Mestrado'
    ,11:'Doutorado'
}

dict_escolaridade1 = {
    -1:'Inferior ao Ensino Médio Completo'
    ,1:'Inferior ao Ensino Médio Completo'
    ,2:'Inferior ao Ensino Médio Completo'
    ,3:'Inferior ao Ensino Médio Completo'
    ,4:'Inferior ao Ensino Médio Completo'
    ,5:'Inferior ao Ensino Médio Completo'
    ,6:'Inferior ao Ensino Médio Completo'
    ,7:'Ensino Médio ao Superior Incompleto'
    ,8:'Ensino Médio ao Superior Incompleto'
    ,9:'Superior'
    ,10:'Mestrado'
    ,11:'Doutorado'
}

dic_dtype = {
    'CBO Ocupação 2002' : 'category'
    ,'CNAE 2.0 Classe' : 'category'
    ,'CNAE 95 Classe' : 'category'
    , 'Idade':'int32'
    , 'Ind Simples':'category'
    ,'Faixa Etária' : type_cat_faixa_etaria
    ,'Faixa Remun Dezem (SM)' : type_cat_faixa_remu_media_dezembro
    ,'Faixa Remun Média (SM)' : type_cat_faixa_remu_media
    ,'Faixa Tempo Emprego' : 'category'
    ,'Escolaridade após 2005' : type_cat_escolaridade
    ,'Mun Trab' : 'category'
    ,'Município' : 'category'
    ,'Nacionalidade' : 'category'
    ,'Natureza Jurídica' : 'category'
    ,'CNAE 2.0 Subclasse' : 'category'
    ,'Tamanho Estabelecimento' : type_cat_tam_estabelecimento
    ,'Tipo Estab' : 'category'
    ,'Tipo Estab.1' : 'category'
    ,'Tipo Vínculo' : 'category'
    , 'Vl Remun Dezembro Nom' : np.float64
    , 'Vl Remun Média Nom' : np.float32
    , 'Vl Remun Dezembro (SM)' : np.float64
    , 'Vl Remun Média (SM)' : np.float64
    , 'Tempo Emprego' : np.float64
    , 'territorio_tese':'category'
    , 'arranjo':'category'
    , 'knowledge_services':type_cat_know_services
    , 'technology_industries':type_cat_ind_tec
    , 'potec':type_cat_potec
    , 'Raça Cor':'category'
    , 'Sexo Trabalhador':'category'
}



def get_dict_services_knowledge():

    df_sectors_technology = pd.read_csv(
        os.path.join(modulepath,'../app_rais/data/sector_structure/estrutura setorial.csv')
        , sep=';'
        , dtype={
            'cod_cnae_grupo':'category'
            ,'CNAE_grupo':'category'
            , 'technology_industries':'category'
            }
    ) 
    dict_services_knowledge = {row[1]['cod_cnae_grupo']:row[1]['knowledge_services'] for row in df_sectors_technology.iterrows()}

    return dict_services_knowledge


def get_dict_industries_tec():

    df_sectors_technology = pd.read_csv(
        os.path.join(modulepath,'../app_rais/data/sector_structure/estrutura setorial.csv')
        , sep=';'
        , dtype={
            'cod_cnae_grupo':'category'
            ,'CNAE_grupo':'category'
            , 'technology_industries':'category'
            }
    ) 
    dict_industries_tec = {row[1]['cod_cnae_grupo']:row[1]['technology_industries'] for row in df_sectors_technology.iterrows()}

    return dict_industries_tec


def get_dict_potec():

    df_potec = pd.read_csv(
        os.path.join(modulepath,'data/occupation_structure/potec.csv')
        , sep=';'
        , dtype=dic_dtype
    )
    
    
    dict_potec = {row[1]['CBO Ocupação 2002']:row[1]['potec'] for row in df_potec.iterrows()}
    
    
    return dict_potec


            


#def generate_columns_file(uf_base=, ):
#    """
#    NOT READY!!!!!!!!!!!!!
#    
#    Having a given Federation Unity (UF) as source, looks for every Rais Original file of said UF to generate the list of  
#    
#    """
#    list_files = glob.glob(pathname=f'app_rais/data/rais_original/**/PE**.txt', recursive=True)
#
#    dfcolumns = pd.DataFrame()
#
#    for file in list_files:
#        df = pd.read_table(
#            file
#            , encoding='Latin-1'
#            , sep=';'
#        #    , usecols=list_column_keep_2010
#            , dtype=dic_dtype
#            , decimal=','
#            , nrows=1
#        )
#
#        dfcolumns = dfcolumns.append(df.columns.to_series(), ignore_index=True)
#    dfcolumns = dfcolumns.transpose().reset_index().drop(columns='index')
#    dfcolumns.columns = [x[-8:-4] for x in  list_files]
#    dfcolumns.to_csv('columns_to_load_each_year.csv')
#    return dfcolumns
