import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
pd.options.display.float_format = '{:,.2f}'.format
from itertools import product
import matplotlib.pyplot as plt
import plotly.express as px
import os

modulepath = os.path.dirname(__file__)


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

dic_dtype = {
    'CBO Ocupação 2002' : 'category'
    ,'CNAE 2.0 Classe' : 'category'
    ,'CNAE 95 Classe' : 'category'
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
    , 'knowledge_services':'category'
    , 'technology_industries':type_cat_ind_tec
    , 'potec':type_cat_potec
}



def potec_evolution(ufs = ('pr', 'rs', 'pe'), years = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015], data_format='wide'):

    """
    ALTERADO
    For metropolises in the selected UFs, returns a DataFrame containing the Scientific and technical personnel (POTEC in the Portuguese abbreviation) for the given years.
    If data_formmat == 'wide', returned DataFrame holds metropolises and S&T personnel specificities as multi-index levels, while the number of labor contracts appears 
    in columns that represent each year. If data_format == 'long', returned DataFrame is in tidy layout, without multi-index layers, containing columns for S&T personnel 
    categories, a single column for the number of labor contracts, besides another one for years (Suited for plotting).

    """
    
    
    dict_df = dict()
    dict_df_ufs = dict()
    dict_rms = {'PR': 'Curitiba', 'RS':'Porto Alegre', 'PE': 'Recife'}
    ufs = tuple([unity.upper() for unity in ufs])

    for uf in ufs:
        for year in years:
            df = pd.read_csv(
                os.path.join(modulepath, f'data/rais_treated/{year}/{uf.upper()}{year}.zip')
#                f'data/rais_treated/{year}/{uf.upper()}{year}.zip'
                , compression='zip'
                , header=0
                , sep=';'
                , decimal=','
                , dtype=dic_dtype
                , usecols=['territorio_tese', 'potec']
            )


            filter_rm_territory = df.territorio_tese != df.territorio_tese.cat.categories[1]
            df = pd.DataFrame(df.loc[filter_rm_territory, :].groupby(by=['territorio_tese', 'potec'], observed=True).size())
            df.rename(columns={0:'PO Metropolitano'}, inplace=True)

            dict_df[uf + str(year)] = df

        if len(ufs) == 1 and len(years) == 1:
            break

        elif len(ufs) == 1 and len(years) > 1:
            list_dfs = [dict_df[uf + str(year)].reset_index().drop(columns='territorio_tese').set_index('potec') 
         for uf, year in product(ufs, years)]

            df = pd.concat(list_dfs,  axis=1)

            df.columns = years

        else:

            list_dfs = [dict_df[uf + str(year)].reset_index().drop(columns='territorio_tese').set_index('potec') for year in years]

            df = pd.concat(list_dfs, axis=1)

            df.columns = years

            dict_df_ufs[uf] = df

            dict_df = dict()


            df = pd.concat(dict_df_ufs.values(),  axis=0, keys=dict_df_ufs.keys())

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

            df['Potec Grupo'] = df.reset_index()['potec'].map(dict_potec).values

            df[years] = df[years].fillna(0).astype(np.int64)

            df['Tipo de Ocupação'] = df['Potec Grupo'].map({'Demais Ocupações':'Demais Ocupações'}).fillna('POTEC').values

            df = df.set_index(['Potec Grupo', 'Tipo de Ocupação'], append=True).reorder_levels([None,'Tipo de Ocupação','Potec Grupo', 'potec'])

            df.index.names = ['RM','Tipo de Ocupação','Potec Grupo', 'potec']

            df.rename(index=dict_rms, inplace=True) 

            df.sort_index(level=[0,1], ascending=False, inplace=True)
            
            
    if  data_format=='long':
        
        df = df.reset_index().drop(columns='potec').groupby(by=['RM', 'Tipo de Ocupação','Potec Grupo']).sum().reset_index().melt(id_vars=['RM', 'Tipo de Ocupação', 'Potec Grupo']).rename(columns={'variable':'ano', 'value':'pessoal'})
        df = df[df['Tipo de Ocupação'] == 'POTEC']
        df['Potec Grupo'] = df['Potec Grupo'].astype(type_cat_potec_grupo)
        
            

    return df


def plot_potec_evolution(df, dynamic=True, data_format='long'):
    """
    Returns a bar plot that represents the number of labor contracts for S&T personnel groups for different years. If dynamic == True, returns a dynamic plot, otherwise
    returns a static one.
    By default, accepts the long formmat of the DataFrame generated by potec_evolution function. If the wide version of the DataFrame is passed, data_format must be 
    set to 'wide'.
    """
    if data_format == 'wide':
                
        df = df.reset_index().drop(columns='potec').groupby(by=['RM', 'Tipo de Ocupação','Potec Grupo']).sum().reset_index().melt(id_vars=['RM', 'Tipo de Ocupação', 'Potec Grupo']).rename(columns={'variable':'ano', 'value':'pessoal'})
        df = df[df['Tipo de Ocupação'] == 'POTEC']
        df['Potec Grupo'] = df['Potec Grupo'].astype(type_cat_potec_grupo)

    if dynamic == True:
        fig = px.bar(data_frame=df
               , y='pessoal'
               , x='RM'
               , color='Potec Grupo'
               , animation_frame='ano'
               , category_orders={'Potec Grupo':
                                  ['Profissionais do Ensino'
                                   , 'Profissionais científicos'
                                   ,'Engenheiros'
                                   , 'Pesquisadores'
                                   , 'Diretores e Gerentes de P&D'
                                  ]}
               , title=f'POTEC entre {df.ano.astype(np.int32).min()} e {df.ano.astype(np.int32).max()}'
               , height=700, color_discrete_sequence=['rgb(141, 201, 199)', 'rgb(136, 136, 238)', '#1F77B4', 'rgb(250, 255, 195)', 'rgb(228,70,70)']
              , range_y=(0,50000)
        )

        fig.update_layout(transition = {'duration': 600})

        
    elif dynamic == False:
        fig = px.bar(data_frame=df
                     , x='ano'
                     , y='pessoal'
                     , facet_row='RM'
                     , color='Potec Grupo'
                     , category_orders={'Potec Grupo':
                                        ['Profissionais do Ensino'
                                         , 'Profissionais científicos'
                                         ,'Engenheiros'
                                         , 'Pesquisadores'
                                         , 'Diretores e Gerentes de P&D'
                                        ]}
                     , title=f'POTEC entre {df.ano.astype(np.int32).min()} e {df.ano.astype(np.int32).max()}'
                     , height=700, color_discrete_sequence=['rgb(141, 201, 199)', 'rgb(136, 136, 238)', '#1F77B4', 'rgb(250, 255, 195)', 'rgb(228,70,70)'])
    
    return fig



def potec_rm_compare(ufs = ('pr', 'rs', 'pe'), year = 2015, multi_index=True, data_format='wide'):

    dict_df = dict()
    dict_df_ufs = dict()
    dict_rms = {'PR': 'Curitiba', 'RS':'Porto Alegre', 'PE': 'Recife'}

    ufs = tuple([unity.upper() for unity in ufs])

    for uf in ufs:
        df = pd.read_csv(
            os.path.join(modulepath, f'data/rais_treated/{year}/{uf.upper()}{year}.zip')
#            f'data/rais_treated/{year}/{uf.upper()}{year}.zip'
            , compression='zip'
            , header=0
            , sep=';'
            , decimal=','
            , dtype=dic_dtype
            , usecols=['territorio_tese', 'potec']
        )
        filter_rm_territory = df.territorio_tese != df.territorio_tese.cat.categories[1]
        df = pd.DataFrame(df.loc[filter_rm_territory, :].groupby(by=['territorio_tese', 'potec'], observed=True).size())
        df.rename(columns={0:'PO Metropolitano'}, inplace=True)
        dict_df[uf] = df

    list_dfs = [dict_df[uf].reset_index().drop(columns='territorio_tese').set_index('potec') for uf in ufs]

    list_rms = [dict_rms[uf] for uf in ufs]

    df = pd.concat(list_dfs, axis=1)

    df.columns= list_rms

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

    df['Potec Grupo'] = df.reset_index()['potec'].map(dict_potec).values

    df[list_rms] = df[list_rms].fillna(0).astype(np.int64)

    df['Tipo de Ocupação'] = df['Potec Grupo'].map({'Demais Ocupações':'Demais Ocupações'}).fillna('POTEC').values

    df = df.set_index(['Potec Grupo', 'Tipo de Ocupação'], append=True).reorder_levels(['Tipo de Ocupação','Potec Grupo', 'potec'])

    df.index.names = ['Tipo de Ocupação','Potec Grupo', 'Potec']

    df.sort_index(level=[0,1], ascending=False, inplace=True)

    if data_format=='long':
        df.reset_index(inplace=True)
        df = df[df['Tipo de Ocupação'] == 'POTEC'].melt(id_vars=['Potec Grupo', 'Potec'], value_vars=['Curitiba', 'Porto Alegre', 'Recife'], var_name='RM', value_name='Pessoal')
    
    return df


def plot_potec_rm_compare(df, data_format='long'):

    if data_format=='wide':
        df.reset_index(inplace=True)
        df = df[df['Tipo de Ocupação'] == 'POTEC'].melt(id_vars=['Potec Grupo', 'Potec'], value_vars=['Curitiba', 'Porto Alegre', 'Recife'], var_name='RM', value_name='Pessoal')
    
    df = df.groupby(['RM','Potec Grupo']).sum().reset_index()
    
    fig = px.bar(
        data_frame=df
        , x='RM'
        , y='Pessoal'
        , color='Potec Grupo'
        , category_orders={'Potec Grupo':['Profissionais do Ensino', 'Profissionais científicos', 'Engenheiros', 'Pesquisadores', 'Diretores e Gerentes de P&D']}
        , color_discrete_sequence=['rgb(141, 201, 199)', 'rgb(136, 136, 238)', '#1F77B4', 'rgb(250, 255, 195)', 'rgb(228,70,70)']
    )
    
    return fig


def potec_proporcao_rm_uf(ufs = ('pr', 'rs', 'pe'), year = 2015, tidy=True):

    ufs = ('pr', 'rs', 'pe')
    year = 2015
    multi_index=False

    dict_df = dict()
    dict_df_ufs = dict()
    dict_rms = {'PR': 'Curitiba', 'RS':'Porto Alegre', 'PE': 'Recife'}

    ufs = tuple([unity.upper() for unity in ufs])

    for uf in ufs:
        df = pd.read_csv(
            os.path.join(modulepath, f'data/rais_treated/{year}/{uf.upper()}{year}.zip')
#            f'data/rais_treated/{year}/{uf.upper()}{year}.zip'
            , compression='zip'
            , header=0
            , sep=';'
            , decimal=','
            , dtype=dic_dtype
            , usecols=['territorio_tese', 'potec']
        )
        
        df = pd.DataFrame(df.groupby(by=['territorio_tese', 'potec'], observed=True).size())
        df.rename(columns={0:'Pessoal'}, inplace=True)
        dict_df[uf] = df

    list_dfs = [dict_df[uf].reset_index().set_index('potec') for uf in ufs]

    list_rms = [dict_rms[uf] for uf in ufs]

    df = pd.concat(list_dfs, axis=0)

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

    df['Potec Grupo'] = df.reset_index()['potec'].map(dict_potec).values

    df['Tipo Pessoal'] = df.reset_index()['potec'].map({'Demais Ocupações':'Demais Ocupações'}).fillna('POTEC').values

    df = df.reset_index()[['territorio_tese', 'Tipo Pessoal', 'Potec Grupo', 'potec', 'Pessoal']]

    df['UF'] = df['territorio_tese'].map({'Restante do Paraná':'PR'
                               , 'Espaço Metropolitano de Curitiba':'PR'
                               ,'Restante do Rio Grande do Sul':'RS'
                               ,'Espaço Metropolitano de Porto Alegre':'RS'
                               ,'Espaço Metropolitano de Recife':'PE'
                               , 'Restante de Pernambuco':'PE'}).values

    if tidy == True:    
        df = df[df['Tipo Pessoal'] == 'POTEC'].drop(columns=['potec', 'Potec Grupo', 'Tipo Pessoal']).groupby(['UF', 'territorio_tese']).sum().reset_index()
    
    else:
        df = df[['UF','territorio_tese', 'Tipo Pessoal', 'Potec Grupo', 'potec', 'Pessoal']]
    
    return df


def plot_potec_proporcao_rm_uf(df, data_format='long'):

    if data_format=='wide':

        df = df[df['Tipo Pessoal'] == 'POTEC'].drop(columns=['potec', 'Potec Grupo', 'Tipo Pessoal']).groupby(['UF', 'territorio_tese']).sum().reset_index()
        
    fig = px.bar(data_frame=df
                , x='UF'
                , y='Pessoal'
                , color='territorio_tese'
                , color_discrete_sequence=['#1F77B4', 'rgb(228,70,70)']
                , hover_name='territorio_tese'
                , title='Participação das RMs no total vínculos de POTEC na UF'
                , text='territorio_tese'
                , hover_data={'Pessoal':True, 'UF':False, 'territorio_tese':False}
                )

    fig.update_layout(showlegend=False)
    
    return fig


def aggregate_potec(ufs = ['pr', 'rs', 'pe'], year = [2015]):



    dict_df = dict()

    ufs = tuple([unity.upper() for unity in ufs])

    for uf, year in product(ufs, year):

        df = pd.read_csv(
            os.path.join(modulepath, f'data/rais_treated/{year}/{uf.upper()}{year}.zip')
#            f'data/rais_treated/{year}/{uf.upper()}{year}.zip'
            , compression='zip'
            , header=0
            , sep=';'
            , decimal=','
            , dtype=dic_dtype
            , usecols=['territorio_tese', 'potec']
        )

        filter_potec = df.potec != df.potec.cat.categories[0]  
        filter_rm_territory = df.territorio_tese != df.territorio_tese.cat.categories[1]


        df_composed = pd.DataFrame(df.loc[filter_potec & filter_rm_territory, :].groupby(by=['territorio_tese', 'potec'], observed=True).size().sort_index())


        df_composed['PO estadual'] = df.loc[filter_potec,:].groupby(by=['potec'], observed=True).count().sort_index().values

        df_composed.rename(columns={0:'PO Metropolitano'}, inplace=True)

        df_composed['Participação do setor no espaço metropolitano (%)'] = df_composed['PO Metropolitano'] / df_composed['PO Metropolitano'].sum() *100

        df_composed['Participação do espaço metropolitano no estado (%)'] = df_composed['PO Metropolitano'] / df_composed['PO estadual'] *100

        dict_df[uf] = df_composed
        
        
    list_dfs = [dict_df[uf].reset_index().drop(columns='territorio_tese').set_index('potec') for uf in ufs]
    list_keys = [dict_df[uf].index[0][0] for uf in ufs]
    
    df_composed = pd.concat(list_dfs,  axis=0, keys=list_keys)
    
    return df_composed
