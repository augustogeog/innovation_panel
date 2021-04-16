import pandas as pd
from pandas.api.types import CategoricalDtype
import numpy as np
import os
from itertools import product
from app_rais.dicts_constants import interest_columns_for_year
import app_rais.dicts_constants as dc

modulepath = os.path.dirname(__file__)


def pretreat_2018(list_ufs, year=2018):

    for uf in list_ufs:
        if os.path.isfile(os.path.join(modulepath, f'data/rais_original/{year}/{uf}{year}.txt')):
            print(f'{uf.upper()}{year}.txt already exists.')
            pass
        else:        
            if uf.upper() in ['RR', 'AP', 'AM', 'PA', 'TO', 'AC', 'RO']:
                file = 'RAIS_VINC_PUB_NORTE'
            elif uf.upper() in ['MT', 'MS', 'GO', 'DF']:
                file = 'RAIS_VINC_PUB_CENTRO_OESTE'
            elif uf.upper() in ['MG', 'RJ', 'ES']:
                file = 'RAIS_VINC_PUB_MG_ES_RJ'
            elif uf.upper() in ['PR', 'SC', 'RS']:
                file = 'RAIS_VINC_PUB_SUL'
            elif uf.upper() in ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']:
                file = 'RAIS_VINC_PUB_NORDESTE'
            elif uf.upper() == 'SP':
                file = 'RAIS_VINC_PUB_SP'

            df = pd.read_table(
                os.path.join(modulepath, f'data/rais_original/{year}/{file}.txt')
                , encoding='Latin-1'
                , sep=';'
                , decimal=','
                , dtype=dc.dic_dtype
                )
            df = df[df['Município'].str.startswith(dc.dict_uf_cod[uf])]

            df.to_csv(
                os.path.join(modulepath, f'data/rais_original/{year}/{uf}{year}.txt')
                , encoding='Latin-1'
                , sep=';'
                , decimal=','
                , index=False
            )
            print(print(f'{uf.upper()}{year}.txt saved.'))


def pretreat_rais(uf='PR', year=2007, treating=True):
    '''
    Loads Rais data into Pandas DataFrame regarding the year and Brazilian
    federation unity (UF) selected. If treating is set to True (default), 
    loads a predefined set of columns, overrides the automatically 
    inputed data types with others selected to enhance performance, 
    besides deleting registers of non active jobs in 12/31 of the selected year.
    
    '''

    year = int(year)

    list_column_keep = dc.interest_columns_for_year(year)


    if uf==None or year==None:
        print('Please set both uf and year.')
    
    else:    
    
        if treating == False:
            df = pd.read_table(
                os.path.join(modulepath, f'data/rais_original/{year}/{uf.upper()}{year}.txt')
                , encoding='Latin-1'
                , sep=';'
                , decimal=','
                )

        else:            
            

            df = pd.read_table(
                os.path.join(modulepath, f'data//rais_original//{year}//{uf.upper()}{year}.txt')
                , encoding='Latin-1'
                , sep=';'
                , usecols=list_column_keep
                , dtype=dc.dic_dtype
                , decimal=','
            )

            df = df.loc[df['Vínculo Ativo 31/12'] == 1]
            
            column_drop_2010 = ['Vínculo Ativo 31/12']
            df.drop(axis=1, labels=column_drop_2010, inplace=True)
            df.reset_index(inplace=True)
            df.drop(labels='index', axis=1, inplace=True)
            

            # Including some columns of interest related to territorial structure of Brazilian motropolises
            # Talvez eu deva fazer para a estrutura territorial o mesmo que fiz para as colunas de POTEC Tech Ind e KS adiante           
            df_territory_tese = pd.read_csv(
                os.path.join(modulepath,'../app_territory/data/territorio_tese.csv')
                , sep=';'
                , dtype={'Município':'category', 'territorio_tese': 'category'})
            df = df.merge(
                df_territory_tese
                , on='Município'
                , how='left')

            df_territory_regic = pd.read_csv(
                os.path.join(modulepath,'../app_territory/data/territorio_regic_ap_2018.csv')
                , sep=';'
                , dtype={'Município':'category', 'arranjo': 'category'})
            df = df.merge(
                df_territory_regic
                , on='Município'
                , how='left')

            df['Município'] = df.loc[:, 'Município'].map(dc.get_dict_mun_code()).astype('category')
            
            if (year < 2006) and (year >=1995):
            
                df['knowledge_services'] = df.loc[:, 'CNAE 95 Classe'].map(dc.get_dict_services_knowledge(int(year))).astype(dc.type_cat_know_services)
                df['technology_industries'] = df.loc[:, 'CNAE 95 Classe'].map(dc.get_dict_industries_tec(int(year))).astype(dc.type_cat_ind_tec)

            elif year >= 2006:  
            
                df['knowledge_services'] = df.loc[:, 'CNAE 2.0 Classe'].str.slice(0,3).map(dc.get_dict_services_knowledge(int(year))).astype(dc.type_cat_know_services)
                df['technology_industries'] = df.loc[:, 'CNAE 2.0 Classe'].str.slice(0,3).map(dc.get_dict_industries_tec(int(year))).astype(dc.type_cat_ind_tec)
            

            if (year >= 1995) and (year < 2003):
                df['potec'] = df.loc[:, 'CBO 94 Ocupação'].map(dc.get_dict_potec(int(year))).fillna('Demais Ocupações').astype(dc.type_cat_potec)
            
            elif year >=2003:
                df['potec'] = df.loc[:, 'CBO Ocupação 2002'].map(dc.get_dict_potec(int(year))).fillna('Demais Ocupações').astype(dc.type_cat_potec)
                  
    return df



def save_treated(df=None, year=None, uf=None):
    
    
    if year == None or uf == None:
        print('Please do not forget to insert df, year and uf.')
    
    else:
        
        # inserir aqui uma condição para verificar se o arquivo já existe.
        
        directory = os.path.join(modulepath, f'data/rais_treated/{year}/')
        os.makedirs(directory, exist_ok=True)

        df.to_pickle(os.path.join(directory, f'{uf.upper()}{year}.zip'))


def original_to_treated_loop(ufs=None, years=None):

    for uf, year  in product(ufs, years):
        
        try:
            df = pretreat_rais(uf=uf, year=year, treating=True)
            save_treated(df=df, year=year, uf=uf)
            print(f'{uf.upper()}{year}.zip saved.')
        
        except:
            print(f'{uf.upper()}{year}.zip could not be saved.')



def generate_rais_dataframe(list_ufs, year, data_format='wide', filter_metarea=False, territorio='arranjo'):

    """
    For selected Brazilian Federation Unities (ufs) and year, loads pretreated Rais data into a Pandas DataFrame and treat it so 
    it is suited to analysis of formally employed personnel with respect to metrics of: scientific and technical (S&T)
    personnel (POTEC), organization legal status, economic sectors, categories of services according to intensity of applied 
    knowledge, industry technological levels; and level of education.
    
    If filter_metarea is set to True, it will load data reffering just to the metropolitan areas of the selected Federation Unities,
    leaving out data of remaining municipalities.
    
    If territorio is equal to 'arranjo', the resulting DataFrame will have data related to population arrangement for Brazilian Metropolises. Else, if
    territorio is equal to 'territorio_tese', it will use the territorial refference used in the thesis found at 
    https://acervodigital.ufpr.br/handle/1884/58421?show=full
    
    """
    if year > 2005:
        escolaridade = 'Escolaridade após 2005'
    else:
        escolaridade = 'Grau Instrução 2005-1985'
    
    # Loads each file into DataFrame and assign it to the dictionary dict_df
    dict_df = dict()
    for uf in list_ufs:
        df = pd.read_pickle(os.path.join(modulepath, f'data/rais_treated/{year}/{uf}{year}.zip'))
        
        df['UF'] = uf.upper()
        df['UF'] = df['UF'].astype('category')

#        if filter_metarea == True:
#            filter_rm_territory = df.territorio_tese != df.territorio_tese.cat.categories[1]
#            df = df.groupby(by=['UF', territorio, 'Tamanho Estabelecimento', 'Natureza Jurídica', 'knowledge_services', 'technology_industries', 'Escolaridade após 2005','potec'], observed=True).size().reset_index()
#        
#        elif filter_metarea == False:
        df = df.groupby(
            by=[
                'UF'
                , 'Município'
#                , territorio
                , 'Tamanho Estabelecimento'
                , 'Natureza Jurídica'
                , 'knowledge_services'
                , 'technology_industries'
                , escolaridade
                ,'potec'], observed=True).size().reset_index()
        dict_df[uf] = df


    # Concatenates the DataFrames that are in dict_df
    df = pd.concat(dict_df.values(),  axis=0)


    df.rename(columns={0: 'Pessoal'}, inplace=True)
#    df['Município'] = df['Município'].astype('category')
    df['Cod Município'] = df['Município'].astype('category')
    df['Município'] = df.loc[:, 'Município'].map(dc.get_dict_mun_name()).astype('category')
#    df[territorio] = df[territorio].astype('category')
#    df.rename(columns={territorio:'Território'}, inplace=True)
    
    # Creates new columns for organization size, organization legal status, economic sectors, level of education and scientific and technical (S&T) personnel (POTEC)
    df['Tamanho Estabelecimento'] = df['Tamanho Estabelecimento'].map(dc.dict_porte).astype(dc.type_porte)
    df['Natureza Jurídica Grupo'] = df['Natureza Jurídica'].astype('category').str.slice(start=0, stop=1).map(dc.dict_nat_jur).astype('category')
    df['Natureza Jurídica'] = df['Natureza Jurídica'].map(dc.dict_nat_jur_detail).fillna('OUTROS').astype('category')
    df['Sectors'] = df.knowledge_services.map({'Without Classification':'Without Classification'}).fillna('Services')
    df['Sectors'] = ['Services' if x[1]['Sectors'] == 'Services' else 'Industry' if x[1]['technology_industries'] != 'Without Classification' and x[1]['Sectors'] != 'Services'  else 'Others' for x in df.iterrows()]
    df['Sectors'] = df['Sectors'].astype('category')
    df['Escolaridade1'] = df[escolaridade].map(dc.dict_escolaridade).astype(dc.type_escolaridade_treated)
    df['Escolaridade2'] = df[escolaridade].map(dc.dict_escolaridade1).astype(dc.type_escolaridade1_treated)
    df['Potec Grupo'] = df['potec'].map(dc.dict_potec).astype('category')
    df['UF'] = df['UF'].astype('category')
    

    df_territory_tese = pd.read_csv(
        os.path.join(modulepath,'../app_territory/data/territory.csv')
        , sep=';'
        , dtype={'Cod Município':'category', 'Território': 'category'})
    df = df.merge(
        df_territory_tese
        , on='Cod Município'
        , how='left')
    df['Cod Município'] = df['Cod Município'].astype('category')

    # Reorder columns
    df = df[[
        'UF'
        ,'Cod Município'
        , 'Município'
        ,'Território'
        , 'Sectors'
        , 'Tamanho Estabelecimento'
        , 'Natureza Jurídica Grupo'
        , 'Natureza Jurídica'
        , 'knowledge_services'
        , 'technology_industries'
        , 'Potec Grupo'
        , 'potec'
        , 'Escolaridade1'
        , 'Escolaridade2'
        , 'Pessoal'
    ]]
    
        
    return df


def load_save_rais_dataframe_loop(list_ufs, list_years, filter_metarea=False, territorio='arranjo'):
    
    directory = os.path.join(modulepath, f'data/rais_dataframes/')
    os.makedirs(directory, exist_ok=True)
    
    for year in list_years:
        df = generate_rais_dataframe(list_ufs=list_ufs, year=year, filter_metarea=filter_metarea, territorio=territorio)

        df.reset_index().drop(columns='index').to_feather(os.path.join(directory, f'ufs_with_motropolises_{year}.ftd'))
        print(f'ufs_with_motropolises_{year} saved.')



