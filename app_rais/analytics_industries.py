import numpy as np
import os
import pandas as pd
from pandas.api.types import CategoricalDtype
import plotly.express as px
import matplotlib.pyplot as plt
import app_rais.dicts_constants as dc

modulepath = os.path.dirname(__file__)

def ind_level_comparison_table(year, list_ufs):
    df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_motropolises_{year}.ftd'))
    df = df[df['UF'].isin(list_ufs)]
    df = df[df['technology_industries'] != 'Without Classification']
    df_uf = df.copy()
    df = df[~df['Território'].str.startswith('Demais')]
    df = df.groupby(['UF', 'Território', 'technology_industries'], observed=True).agg(Pessoal_sum=('Pessoal', 'sum'))
    df = df.reset_index()
    df_uf = df_uf[['UF', 'technology_industries', 'Pessoal']].groupby(by=['UF', 'technology_industries'], observed=True).sum()
    df_uf = df_uf.reset_index()
    df_merged = pd.merge(left=df, right=df_uf, on=['UF', 'technology_industries'])
    df_merged = df_merged.rename(
        columns={'technology_industries':'Nível Tecnológico', 'Pessoal_sum': 'PO', 'Pessoal': 'PO estadual'})
    df_merged = df_merged.sort_values(by=['UF', 'Território', 'Nível Tecnológico'])
    PO_metropolitano = pd.merge(
        left=df_merged
        , right=pd.DataFrame(
            df_merged.groupby(
                ['Território']
                , observed=True).sum()['PO'])
        , on='Território')['PO_y'].values
    df_merged['Território'] = df_merged['Território'].replace(dc.dict_arranjo)
    df_merged['Participação Metropolitana (%)'] = df_merged['PO'] / PO_metropolitano * 100
    df_merged['Participação Estadual (%)'] = df_merged['PO'] / df_merged['PO estadual'] * 100
    df_merged = df_merged.groupby(['UF', 'Território', 'Nível Tecnológico'], observed=True).sum()
    
    return df_merged


def ind_level_comparison_plot(year, ufs):
    
    df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_motropolises_{year}.ftd'))
    df = df[df['UF'].isin(ufs)]
    df = df[df['technology_industries'] != 'Without Classification']
    df = df[~df['Território'].str.startswith('Demais')]
    df = df.groupby(['UF', 'Território', 'technology_industries'], observed=True).agg(Pessoal_sum=('Pessoal', 'sum'))
    df = df.reset_index()
    df['Território'] = df['Território'].map(dc.dict_arranjo)
    df['technology_industries'] = df['technology_industries'].map(
        {
        'High-technology':'Alto'
        , 'Medium-high-technology':'Médio-Alto'
        , 'Medium-low-technology':'Médio-Baixo'
        , 'Low-technology':'Baixo'
        }
    )
    df.rename(columns={'Território':'Espaço Metropolitano', 'Pessoal_sum':'Pessoal', 'technology_industries':'Nível Tecnológico'}, inplace=True)
    fig = px.bar(
        data_frame=df
        , x='Pessoal'
        , y='Espaço Metropolitano' 
        , color='Nível Tecnológico'
        , orientation='h'
        , color_discrete_map={
            'Alto':'rgb(103,0,31)'
            , 'Médio-Alto':'rgb(178,24,43)'
            , 'Médio-Baixo':'rgb(214,96,77)'
            , 'Baixo':'rgb(244,165,130)'}
        , height=700
        , title=f'Indústrias no Espaços Metropolitanos Segundo Nível Tecnológico em {year}'
    )


    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig


def ind_tech_level_evolution_dynamic(list_years, list_ufs, range_x, list_tec_level=None,  relative=False, focus='Baixo'):
    
    if focus == 'Baixo':
        focus = ['Manaus','Campinas', 'Curitiba','Belo Horizonte', 'São Paulo', 'Salvador', 'Vitória','Rio de Janeiro', 'Florianópolis', 'Porto Alegre', 'Recife', 'Brasília', 'Goiânia', 'Belém', 'Fortaleza', 'Total']
    elif focus == 'Alto':
        focus = ['Manaus','Campinas', 'Florianópolis', 'São Paulo','Rio de Janeiro', 'Brasília', 'Belo Horizonte', 'Porto Alegre', 'Curitiba', 'Goiânia', 'Fortaleza', 'Recife','Salvador', 'Vitória', 'Belém', 'Total']
    elif focus == 'Médio-Alto':
        focus = ['Manaus','Campinas','Curitiba','São Paulo', 'Belo Horizonte','Salvador', 'Porto Alegre','Florianópolis' ,'Rio de Janeiro','Recife', 'Goiânia', 'Brasília',  'Fortaleza', 'Belém', 'Vitória', 'Total']
    
    
    
    dict_df = dict()
    
    for year in list_years:
        year = str(year)
        df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_motropolises_{year}.ftd'))
        df = df[df['UF'].isin(list_ufs)]
        df = df[df['technology_industries'] != 'Without Classification']
        df = df[~df['Território'].str.startswith('Demais')]
        df = df.groupby(['UF', 'Território', 'technology_industries'], observed=True).agg(Pessoal=('Pessoal', 'sum'))
        df = df.reset_index()
        df['Território'] = df['Território'].map(dc.dict_arranjo)
        df['technology_industries'] = df['technology_industries'].map({
            'High-technology':'Alto'
            , 'Medium-high-technology':'Médio-Alto'
            , 'Medium-low-technology':'Médio-Baixo'
            , 'Low-technology':'Baixo'
        }
        )
        df.rename(columns={'Território':'Espaço Metropolitano', 'technology_industries':'Nível Tecnológico'}, inplace=True)
        if list_tec_level != None:
            df = df[df['Nível Tecnológico'].isin(list_tec_level)]
        
        dict_df[year] = df
        
    df = pd.concat(dict_df.values(),  axis=0, keys=dict_df.keys())
    df = df.reset_index().drop(columns='level_1').rename(columns={'level_0':'Ano'})
    df.sort_values(by=['Ano', 'UF', 'Espaço Metropolitano'], inplace=True)

#    df = df.reset_index().drop(columns='Index')


    if relative == True:
        # Preparing Total for Brazilian Metropolises
        df_total = df.groupby(['Ano', 'Nível Tecnológico']).agg(Pessoal=('Pessoal', 'sum')).reset_index()
        df_total['Espaço Metropolitano'] = 'Total'
        df_total['UF'] = 'BR'
        df_total = df_total[['Ano', 'Espaço Metropolitano', 'Nível Tecnológico', 'Pessoal']]

        df_total = pd.merge(
            left=df_total
            ,right=df_total.groupby(['Ano']).sum().reset_index()
            , on=['Ano']
            , suffixes=('', ' Total')
        )

        # Preparing the relative data for Brasilia
        df_bras = df[df['Espaço Metropolitano'] == 'Brasília']
        df_bras = pd.merge(
            left=df_bras.groupby(['Ano', 'Espaço Metropolitano', 'Nível Tecnológico']).agg(Pessoal=('Pessoal', 'sum')).reset_index()
            ,right=df_bras.groupby(['Ano', 'Espaço Metropolitano']).agg(Pessoal_total=('Pessoal', 'sum'))
            ,on=['Ano', 'Espaço Metropolitano']
        ).rename(columns={'Pessoal_total': 'Pessoal Total'})

        # Preparing the relative data for the remaining metropolitan areas
        df = df[df['Espaço Metropolitano'] != 'Brasília']
        df = pd.merge(
            left=df.groupby(['Ano', 'Espaço Metropolitano', 'Nível Tecnológico']).agg(Pessoal=('Pessoal', 'sum')).reset_index()
            ,right=df.groupby(['Ano', 'Espaço Metropolitano']).agg(Pessoal_total=('Pessoal', 'sum'))
            ,on=['Ano', 'Espaço Metropolitano']
        ).rename(columns={'Pessoal_total': 'Pessoal Total'})
        
        # concatenating everything

        df = pd.concat([df, df_bras, df_total])

        # calculating the relative values
        df['Pessoal %'] = df['Pessoal'] / df['Pessoal Total'] *100 
        df.drop(columns=['Pessoal', 'Pessoal Total'], inplace=True)
#        df['Ano'] = df['Ano'].astype('category')
#        df['Espaço Metropolitano'] = df['Espaço Metropolitano'].astype('category')
#        df['Nível Tecnológico'] = df['Nível Tecnológico'].astype(dc.type_cat_ind_tec)
#        df.sort_values(by=['Ano', 'Espaço Metropolitano', 'Nível Tecnológico'], inplace=True)
        
    

    fig = px.bar(
        data_frame=df
        , x=df.columns[-1]
        , y='Espaço Metropolitano' 
        , color='Nível Tecnológico'
        , animation_frame='Ano'
        , orientation='h'
        , category_orders={
            'Nível Tecnológico': ['Alto', 'Médio-Alto', 'Médio-Baixo', 'Baixo']
            , 'Espaço Metropolitano': focus
        }
        , color_discrete_map={
            'Alto':'rgb(103,0,31)'
            , 'Médio-Alto':'rgb(178,24,43)'
            , 'Médio-Baixo':'rgb(214,96,77)'
            , 'Baixo':'rgb(244,165,130)'}
        , height=700
        , title=f'Indústrias no Espaços Metropolitanos Segundo Nível Tecnológico entre {list_years[0]} e {list_years[-1]}'
        , range_x=(0,range_x)
        , barmode='relative'
    )
    
    
#    fig.update_layout(transition = {'duration': 20000})

    if relative != True:
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000    
   

    return fig

def ind_tech_level_evolution_table(total=True, save_feather=False):
    df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_metropolises_07to17.ftd'))
    
    df = df[df['technology_industries'] != 'Without Classification']
    
    df.rename(columns={'Território':'Espaço Metropolitano', 'technology_industries': 'Nível Tecnológico'}, inplace=True)

    df = df.groupby(by=['Espaço Metropolitano', 'Nível Tecnológico', 'Ano'], observed=True).agg(Pessoal=('Pessoal', 'sum'))

    df = df.reset_index()

    df = df[~df['Espaço Metropolitano'].str.startswith('Demais')]

    df['Espaço Metropolitano'] = df['Espaço Metropolitano'].replace(dc.dict_arranjo)

    df = df.pivot_table(values='Pessoal', columns='Ano', index=['Espaço Metropolitano', 'Nível Tecnológico'], fill_value=0)
    df.rename_axis(columns={'Ano':''}, inplace=True)
    
    if total == True:
        df_total = df.reset_index().groupby(['Nível Tecnológico'], observed=True).sum().reset_index()
        df_total.insert(0, 'Espaço Metropolitano', 'Total')
        df = pd.concat([df.reset_index(), df_total])
        df.set_index(['Espaço Metropolitano', 'Nível Tecnológico'], inplace=True)
        
    if save_feather == True:
        df.reset_index().to_feather('app_rais/data/rais_dataframes/metro_areas_ind_tec_evolution_07to17.ftd')
    
    return df


def ind_tech_level_evolution_line_plot(title, list_met=['Total'], height=700):
    df = pd.read_feather(os.path.join(modulepath,'data/rais_dataframes/metro_areas_ind_tec_evolution_07to17.ftd'))
    df = df.melt(id_vars=['Espaço Metropolitano', 'Nível Tecnológico'], var_name='Ano', value_name='Pessoal')
    df['Nível Tecnológico'] = df['Nível Tecnológico'].map(
        {
            'High-technology':'Alto'
            , 'Medium-high-technology':'Médio-Alto'
            , 'Medium-low-technology':'Médio-Baixo'
            , 'Low-technology':'Baixo'
        }
    )
    df = df[df['Espaço Metropolitano'].isin(list_met)]
    df = df.groupby(['Espaço Metropolitano', 'Nível Tecnológico', 'Ano']).sum().reset_index()
    
    fig = px.line(
        data_frame=df
        , x='Ano'
        , y='Pessoal'
        , color='Nível Tecnológico'
        , color_discrete_map=
        {
            'Alto':'rgb(103,0,31)'
            , 'Médio-Alto':'rgb(178,24,43)'
            , 'Médio-Baixo':'rgb(214,96,77)'
            , 'Baixo':'rgb(244,165,130)'
        }
        , title = title
        , height=height
    )
    
    return fig

