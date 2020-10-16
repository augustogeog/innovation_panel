import numpy as np
import os
import pandas as pd
from pandas.api.types import CategoricalDtype
import plotly.express as px
import app_rais.dicts_constants as dc

modulepath = os.path.dirname(__file__)



def concentration_level(year, list_ufs, granular_level='sub_category'):
    
    
    df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_motropolises_{year}.ftd'))
    df = df[['UF', 'Território', 'Potec Grupo', 'potec', 'Pessoal']]
    df.insert(2, 'Tipo', df['Potec Grupo'].map({'Demais Ocupações':'Demais Ocupações'}).fillna('POTEC'))

    df = df[df['UF'].isin(list_ufs)]
    df['Território'] = df['Território'].replace(dc.dict_arranjo)
    df.rename(columns={'Território':'Espaço Metropolitano', 'potec':'Potec'}, inplace=True)
    df['UF'].loc[df['Espaço Metropolitano'] == 'Brasília'] = 'DF/GO'
    df = pd.merge(
        left=df.groupby(['UF', 'Espaço Metropolitano', 'Tipo','Potec'], observed=True).sum().reset_index()
        ,right = df.groupby(['UF', 'Potec'], observed=True).sum().reset_index()
        ,on = ['UF', 'Potec']
        , suffixes=(' Metropolitano', ' UF')
    )

    df = df[~df['Espaço Metropolitano'].str.startswith('Demais')]

    df = pd.merge(
        left=df
        ,right = df.groupby(['Espaço Metropolitano', 'Tipo']).sum()['Pessoal Metropolitano']
        ,on = ['Espaço Metropolitano', 'Tipo']
        , suffixes=('', ' Total')
    )

    df['Participação Metropolitana (%)'] = df['Pessoal Metropolitano'] / df['Pessoal Metropolitano Total'] * 100

    df['Participação na UF (%)'] = df['Pessoal Metropolitano'] / df['Pessoal UF'] * 100

    df.drop(columns=['Pessoal Metropolitano Total'], inplace=True)

    df = df.sort_values(['UF', 'Espaço Metropolitano', 'Tipo', 'Potec'])

    df = df.groupby(['UF', 'Espaço Metropolitano', 'Tipo', 'Potec'], observed=True).sum()
    
    if granular_level == 'Type':
        df = df.reset_index().groupby(['UF', 'Espaço Metropolitano', 'Tipo']).sum()

        df['Participação na UF (%)'] = df['Pessoal Metropolitano'] / df['Pessoal UF'] * 100 
        df = pd.merge(
            left=df.reset_index()
            , right=df.reset_index().groupby(['Espaço Metropolitano']).sum()['Pessoal Metropolitano']
            , on='Espaço Metropolitano'
            , suffixes=('', ' Total')
        )
        df['Participação Metropolitana (%)'] = df['Pessoal Metropolitano'] / df['Pessoal Metropolitano Total'] * 100

        df.drop(columns=['Pessoal Metropolitano Total'], inplace=True)

        df.set_index(['UF', 'Espaço Metropolitano', 'Tipo'], inplace=True)
              
    
    return df



def evolution_table(list_years, list_ufs, data_format='wide'):
    dict_df = dict()
    for year in list_years:
        df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_motropolises_{year}.ftd'))
        dict_df[str(year)] = df
    df = pd.concat(dict_df.values(), keys=dict_df.keys())
    df = df[(df['Potec Grupo'] != 'Demais Ocupações') & ~(df['Território'].str.startswith('Demais'))]
    df = df[['UF', 'Território', 'Potec Grupo', 'potec', 'Pessoal']].reset_index().rename(
        columns={'level_0':'Ano'}).drop(columns='level_1')
    
    df['Território'] = df['Território'].map(dc.dict_arranjo)
    df = df.rename(columns={'Território':'Espaço Metropolitano'})
    
    df = df.pivot_table(aggfunc='sum', columns='Ano', index=['Espaço Metropolitano', 'Potec Grupo'])
    df = df.rename_axis(columns={'Ano':''})
    df = df.droplevel(0, axis=1)
    
    if data_format == 'wide':
        pass
    elif data_format == 'long':
        df = df.melt(ignore_index=False, value_name='Pessoal', var_name='Ano').reset_index()
    
    return df

def evolution_plot(list_years, list_ufs):

    df = evolution_table(list_years=list_years, list_ufs=list_ufs, data_format='long')
    
    fig = px.bar(
        data_frame=df
        , y='Espaço Metropolitano'
        , x='Pessoal'
        , color='Potec Grupo'
        , animation_frame='Ano'
        , category_orders=
        {
            'Potec Grupo':
            [
                'Profissionais do Ensino'
                , 'Profissionais científicos'
                ,'Engenheiros'
                , 'Pesquisadores'
                , 'Diretores e Gerentes de P&D'
            ]
        }
        , title=f'POTEC entre {df.Ano.astype(np.int32).min()} e {df.Ano.astype(np.int32).max()}'
        , color_discrete_sequence=['rgb(141, 201, 199)', 'rgb(136, 136, 238)', '#1F77B4', 'rgb(250, 255, 195)', 'rgb(228,70,70)']
        , height=700
        , range_x=(0,300_000)
    )

    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000 
    
    return fig