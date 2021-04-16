import numpy as np
import os
import pandas as pd
from pandas.api.types import CategoricalDtype
import plotly.express as px
import matplotlib.pyplot as plt
import app_rais.dicts_constants as dc

modulepath = os.path.dirname(__file__)

def ind_level_comparison_table(year, list_ufs, list_territory_exclude=None, exclude_territory_starts_with=None):
    df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_motropolises_{year}.ftd'))
    df = df[df['UF'].isin(list_ufs)]
    df = df[df['technology_industries'] != 'Without Classification']
    df_uf = df.copy()
    if list_territory_exclude != None:
        df = df[~df['Território'].isin(list_territory_exclude)]
    if exclude_territory_starts_with != None:
        df = df[~df['Território'].str.startswith(exclude_territory_starts_with)]
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


def ind_level_comparison_plot(year, ufs, list_territory_exclude=None, exclude_territory_starts_with=None):
    
    df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_motropolises_{year}.ftd'))
    df = df[df['UF'].isin(ufs)]
    df = df[df['technology_industries'] != 'Without Classification']
    if list_territory_exclude != None:
        df = df[~df['Território'].isin(list_territory_exclude)]
    if exclude_territory_starts_with !=None:
        df = df[~df['Território'].str.startswith(exclude_territory_starts_with)]
    df = df.groupby(['UF', 'Território', 'technology_industries'], observed=True).agg(Pessoal_sum=('Pessoal', 'sum'))
    df = df.reset_index()
    df['Território'] = df['Território'].replace(dc.dict_arranjo)
    df['technology_industries'] = df['technology_industries'].map(
        {
        'High-technology':'Alto'
        , 'Medium-high-technology':'Médio-Alto'
        , 'Medium-low-technology':'Médio-Baixo'
        , 'Low-technology':'Baixo'
        }
    )
    df.rename(columns={'Pessoal_sum':'Pessoal', 'technology_industries':'Nível Tecnológico'}, inplace=True)
    fig = px.bar(
        data_frame=df
        , x='Pessoal'
        , y='Território' 
        , color='Nível Tecnológico'
        , orientation='h'
        , color_discrete_map={
            'Alto':'rgb(103,0,31)'
            , 'Médio-Alto':'rgb(178,24,43)'
            , 'Médio-Baixo':'rgb(214,96,77)'
            , 'Baixo':'rgb(244,165,130)'}
        , height=700
        , title=f'Indústrias dos Territórios Selecionados Segundo Nível Tecnológico em {year}'
    )


    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig


def ind_tech_level_evolution_dynamic(list_years, list_ufs, range_x, list_tec_level=None,  relative=False, focus='Baixo', exclude_territory_starts_with=None, list_include_territory=None, height=700):
    
    if focus == 'Baixo':
        focus = ['Manaus','Campinas', 'Curitiba','Belo Horizonte', 'São Paulo', 'Salvador', 'Vitória','Rio de Janeiro', 'Florianópolis', 'Porto Alegre', 'Recife', 'Brasília', 'Goiânia', 'Belém', 'Fortaleza', 'Total']
    elif focus == 'Alto':
        focus = ['Manaus','Campinas', 'Florianópolis', 'São Paulo','Rio de Janeiro', 'Brasília', 'Belo Horizonte', 'Porto Alegre', 'Curitiba', 'Goiânia', 'Fortaleza', 'Recife','Salvador', 'Vitória', 'Belém', 'Total']
    elif focus == 'Médio-Alto':
        focus = ['Manaus','Campinas','Curitiba','São Paulo', 'Belo Horizonte','Salvador', 'Porto Alegre','Florianópolis' ,'Rio de Janeiro','Recife', 'Goiânia', 'Brasília',  'Fortaleza', 'Belém', 'Vitória', 'Total']
    
    
    
    dict_df = dict()
    
    for year in list_years:
        year = str(year)
        df = pd.read_feather(f'app_rais/data/rais_dataframes/ufs_with_motropolises_{year}.ftd')
        df = df[df['UF'].isin(list_ufs)]
        df = df[df['technology_industries'] != 'Without Classification']
        if exclude_territory_starts_with != None:
            df = df[~df['Território'].str.startswith(exclude_territory_starts_with)]
        if list_include_territory != None:
            df = df[~df['Território'].isin(list_include_territory)]
        df = df.groupby(['UF', 'Território', 'technology_industries'], observed=True).agg(Pessoal=('Pessoal', 'sum'))
        df = df.reset_index()
        df['Território'] = df['Território'].replace(dc.dict_arranjo).astype('category')
        df['technology_industries'] = df['technology_industries'].map({
            'High-technology':'Alto'
            , 'Medium-high-technology':'Médio-Alto'
            , 'Medium-low-technology':'Médio-Baixo'
            , 'Low-technology':'Baixo'
        }
        ).astype(dc.type_cat_ind_tec_PT)
        df.rename(columns={'Território':'Espaço Metropolitano', 'technology_industries':'Nível Tecnológico'}, inplace=True)
        if list_tec_level != None:
            df = df[df['Nível Tecnológico'].isin(list_tec_level)]
        
        dict_df[year] = df
        
    df = pd.concat(dict_df.values(),  axis=0, keys=dict_df.keys())
    df = df.reset_index().drop(columns='level_1').rename(columns={'level_0':'Ano'})
    df['Ano'] = df['Ano'].astype(np.int32)
    df['UF'] = df['UF'].astype('category')
    df.sort_values(by=['Ano','Espaço Metropolitano','Nível Tecnológico'],  ascending=True , inplace=True)
#    df.sort_values(by=['Nível Tecnológico','Ano', ], inplace=True)

#    df = df.reset_index().drop(columns='Index')

    territories_order = list()

    if relative == True:

        df_total = df.groupby(['Ano', 'Nível Tecnológico'], observed=True).agg(Pessoal=('Pessoal', 'sum')).reset_index()
        df_total['Espaço Metropolitano'] = 'Total'
        df_total['UF'] = 'BR'
        df_total = df_total[['Ano', 'Espaço Metropolitano', 'Nível Tecnológico', 'Pessoal']]

        df_total = pd.merge(
            left=df_total
            ,right=df_total.groupby(['Ano'], observed=True).sum().reset_index()
            , on=['Ano']
            , suffixes=('', ' Total')
        )

        df = pd.merge(
            left=df.groupby(['Ano', 'Espaço Metropolitano', 'Nível Tecnológico'], observed=True).agg(Pessoal=('Pessoal', 'sum')).reset_index()
            ,right=df.groupby(['Ano', 'Espaço Metropolitano'], observed=True).agg(Pessoal_total=('Pessoal', 'sum'))
            ,on=['Ano', 'Espaço Metropolitano']
        ).rename(columns={'Pessoal_total': 'Pessoal Total'})


        df = pd.concat([df, df_total])
        df['Pessoal %'] = df['Pessoal'] / df['Pessoal Total'] *100 
        df.drop(columns=['Pessoal', 'Pessoal Total'], inplace=True)
        df['Ano'] = df['Ano'].astype('category')
        df['Espaço Metropolitano'] = df['Espaço Metropolitano'].astype('category')
        df['Nível Tecnológico'] = df['Nível Tecnológico'].astype(dc.type_cat_ind_tec_PT)
        df.sort_values(by=['Ano', 'Espaço Metropolitano', 'Nível Tecnológico'], inplace=True)

        territories_order = list(df[(df.Ano == df.Ano.astype(np.int32).max()) & (df['Nível Tecnológico'].isin(['Alto', 'Médio-Alto'])) & (df['Espaço Metropolitano'] != 'Total')].groupby('Espaço Metropolitano', observed=True).sum().sort_values('Pessoal %', ascending=False).index)
        territories_order.extend(['Total'])

        range_x = 100
        
    

    fig = px.bar(
        data_frame=df
        , x=df.columns[-1]
        , y='Espaço Metropolitano' 
        , color='Nível Tecnológico'
        , animation_frame='Ano'
        , orientation='h'
        , category_orders={
#            'Nível Tecnológico': ['Alto', 'Médio-Alto', 'Médio-Baixo', 'Baixo']
             'Espaço Metropolitano': territories_order
        }
        , color_discrete_map={
            'Alto':'rgb(103,0,31)'
            , 'Médio-Alto':'rgb(178,24,43)'
            , 'Médio-Baixo':'rgb(214,96,77)'
            , 'Baixo':'rgb(244,165,130)'}
        , height=height
        , title=f'Indústrias no Espaços Metropolitanos Segundo Nível Tecnológico entre {list_years[0]} e {list_years[-1]}'
        , range_x=(0,range_x)
        , barmode='relative'
    )
    
    
#    fig.update_layout(transition = {'duration': 20000})

    if relative != True:
        fig.update_layout(yaxis={'categoryorder':"sum ascending"})
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000    
   

    return fig, df

def ind_tech_level_evolution_table(list_years, total=True, save_feather=False):
    dict_years = dict()

    for year in list_years:
        df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_motropolises_{year}.ftd'))

        dict_years[year] = df

    df = pd.concat(objs=dict_years.values(), keys=dict_years.keys())
    
#    df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_motropolises_07to17.ftd'))
    
    df = df[df['technology_industries'] != 'Without Classification']
    
    df.rename(columns={'Território':'Espaço Metropolitano', 'technology_industries': 'Nível Tecnológico'}, inplace=True)

    df['Nível Tecnológico'] = df['Nível Tecnológico'].map({
        'High-technology':'Alto'
        , 'Medium-high-technology':'Médio-Alto'
        , 'Medium-low-technology':'Médio-Baixo'
        , 'Low-technology':'Baixo'
        }).astype(dc.type_cat_ind_tec_PT)

    df = df.reset_index().rename(columns={'level_0': 'Ano'}).drop(columns=['level_1'])

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
        df.columns = df.columns.astype('str')
        df.reset_index().to_feather('app_rais/data/rais_dataframes/metro_areas_ind_tec_evolution_00to18.ftd')
    
    return df


def ind_tech_level_evolution_line_plot(title, list_met=['Total'], height=700):
    df = pd.read_feather(os.path.join(modulepath,'data/rais_dataframes/metro_areas_ind_tec_evolution_00to18.ftd'))
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
        , category_orders=
        {
            'Nível Tecnológico':
            [
                'Alto'
                , 'Médio-Alto'
                , 'Médio-Baixo'
                , 'Baixo'
            ]
        }
        , title = title
        , height=height
    )
    
    return fig

