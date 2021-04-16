import os
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import app_rais.dicts_constants as dc

modulepath = os.path.dirname(__file__)

def services_knowledge_comparison_table(year, list_ufs):
    df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_motropolises_{year}.ftd'))
    df = df[df['knowledge_services'] != 'Without Classification']
    df = df[df['UF'].isin(list_ufs)]
    df_uf = df.copy()
    df = df[~df['Território'].str.startswith('Demais')]
    df = df.groupby(['UF', 'Território', 'knowledge_services'], observed=True).agg(Pessoal_sum=('Pessoal', 'sum'))
    df = df.reset_index()
    df_uf = df_uf[['UF', 'knowledge_services', 'Pessoal']].groupby(by=['UF', 'knowledge_services'], observed=True).sum()
    df_uf = df_uf.reset_index()
    df_merged = pd.merge(left=df, right=df_uf, on=['UF', 'knowledge_services'])
    df_merged = df_merged.rename(
        columns={'knowledge_services': 'Tipo', 'Pessoal_sum': 'PO', 'Pessoal': 'PO estadual'}
    )
    df_merged = df_merged.sort_values(by=['UF', 'Território', 'Tipo'])
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
    df_merged['Tipo'].replace(
        {
            'Other less knowledge-intensive services':'Serviços Menos Intensivos em Conhecimento'
            ,'Less knowledge-intensive market services': 'Serviços Menos Intensivos em Conhecimento' 
            ,'Other knowledge-intensive services': 'Outros Serviços Intensivos em Conhecimento'
            ,'Knowledge-intensive market services': 'Serviços de Mercado Intensivos em Conhecimento'
            ,'Knowledge-intensive financial services': 'Serviços Financeiros Intensivos em Conhecimento'
            ,'High-tech knowledge-intensive services': 'De Alta Tecnologia Intensivos em Conhecimento'
        }
        , inplace=True
        )

    df_merged['Tipo'] = df_merged['Tipo'].astype(dc.type_cat_knowledge_PT)
    
    df_merged = df_merged.groupby(['UF', 'Território', 'Tipo'], observed=True).sum()
    
    return df_merged

def knowledge_evolution_dynamic(list_years, list_ufs, range_x,  relative=False, focus = 'relative'):    
    
    if relative == True:
        range_x = 100
    dict_df = dict()
    
    for year in list_years:
        year = str(year)
        df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_motropolises_{year}.ftd'))
        df = df[df['UF'].isin(list_ufs)]
        df = df[df['knowledge_services'] != 'Without Classification']
        df = df[~df['Território'].str.startswith('Demais')]
        df = df.groupby(['UF', 'Território', 'knowledge_services'], observed=True).agg(Pessoal=('Pessoal', 'sum'))
        df = df.reset_index()
        df['Território'] = df['Território'].map(dc.dict_arranjo)
        
        
        df['knowledge_services'].replace(
            {
                'Other less knowledge-intensive services':'Serviços Menos Intensivos em Conhecimento'
                ,'Less knowledge-intensive market services': 'Serviços Menos Intensivos em Conhecimento' 
                ,'Other knowledge-intensive services': 'Outros Serviços Intensivos em Conhecimento'
                ,'Knowledge-intensive market services': 'Serviços de Mercado Intensivos em Conhecimento'
                ,'Knowledge-intensive financial services': 'Serviços Financeiros Intensivos em Conhecimento'
                ,'High-tech knowledge-intensive services': 'De Alta Tecnologia Intensivos em Conhecimento'
            }
            , inplace=True
        )
        
        
        df.rename(columns={'Território':'Espaço Metropolitano', 'knowledge_services':'Tipo'}, inplace=True)
        
        dict_df[year] = df
        
    df = pd.concat(dict_df.values(),  axis=0, keys=dict_df.keys())
    df = df.reset_index().drop(columns='level_1').rename(columns={'level_0':'Ano'})
    df.sort_values(by=['Ano', 'UF', 'Espaço Metropolitano'], inplace=True)

    if focus == 'relative':
        met_order = [ 'Brasília', 'Belém','Manaus', 'Salvador','Goiânia', 'Fortaleza', 'Recife', 'Florianópolis', 'Porto Alegre','Belo Horizonte', 'Curitiba','Rio de Janeiro', 'Vitória','São Paulo', 'Campinas', 'Total']
    elif focus == 'absolut':
        met_order = ['São Paulo','Rio de Janeiro', 'Belo Horizonte','Brasília', 'Porto Alegre', 'Salvador', 'Curitiba', 'Recife', 'Fortaleza','Goiânia', 'Belém','Manaus', 'Vitória', 'Florianópolis', 'Campinas', 'Total']


    if relative == True:
        # Preparing Total for Brazilian Metropolises
        df_total = df.groupby(['Ano', 'Tipo']).agg(Pessoal=('Pessoal', 'sum')).reset_index()
        df_total['Espaço Metropolitano'] = 'Total'
        df_total['UF'] = 'BR'
        df_total = df_total[['Ano', 'Espaço Metropolitano', 'Tipo', 'Pessoal']]

        df_total = pd.merge(
            left=df_total
            ,right=df_total.groupby(['Ano']).sum().reset_index()
            , on=['Ano']
            , suffixes=('', ' Total')
        )

        # Preparing the relative data for Brasilia
        df_bras = df[df['Espaço Metropolitano'] == 'Brasília']
        df_bras = pd.merge(
            left=df_bras.groupby(['Ano', 'Espaço Metropolitano', 'Tipo']).agg(Pessoal=('Pessoal', 'sum')).reset_index()
            ,right=df_bras.groupby(['Ano', 'Espaço Metropolitano']).agg(Pessoal_total=('Pessoal', 'sum'))
            ,on=['Ano', 'Espaço Metropolitano']
        ).rename(columns={'Pessoal_total': 'Pessoal Total'})

        # Preparing the relative data for the remaining metropolitan areas
        df = df[df['Espaço Metropolitano'] != 'Brasília']
        df = pd.merge(
            left=df.groupby(['Ano', 'Espaço Metropolitano', 'Tipo']).agg(Pessoal=('Pessoal', 'sum')).reset_index()
            ,right=df.groupby(['Ano', 'Espaço Metropolitano']).agg(Pessoal_total=('Pessoal', 'sum'))
            ,on=['Ano', 'Espaço Metropolitano']
        ).rename(columns={'Pessoal_total': 'Pessoal Total'})
        
        # concatenating everything

        df = pd.concat([df, df_bras, df_total])

        # calculating the relative values
        df['Pessoal %'] = df['Pessoal'] / df['Pessoal Total'] *100 
        df.drop(columns=['Pessoal', 'Pessoal Total'], inplace=True)

    fig = px.bar(
        data_frame=df
        , x=df.columns[-1]
        , y='Espaço Metropolitano' 
        , color='Tipo'
        , animation_frame='Ano'
        , orientation='h'
        , category_orders={
            'Tipo': [
                'Serviços Menos Intensivos em Conhecimento'
                , 'Outros Serviços Intensivos em Conhecimento'
                , 'Serviços de Mercado Intensivos em Conhecimento'
                ,'Serviços Financeiros Intensivos em Conhecimento'
                ,'De Alta Tecnologia Intensivos em Conhecimento'
            ]
            , 'Espaço Metropolitano': met_order
        }        

        , color_discrete_map={
            'Serviços Menos Intensivos em Conhecimento':'rgb(204,204,204)'
            , 'Outros Serviços Intensivos em Conhecimento':'rgb(55,166,165)'
            , 'Serviços de Mercado Intensivos em Conhecimento':'#4C78A8'
            ,'Serviços Financeiros Intensivos em Conhecimento':'rgb(255,242,174)'
            ,'De Alta Tecnologia Intensivos em Conhecimento':'rgb(228,26,28)'
        }
        , height=750
        , title=f'Serviços no Espaços Metropolitanos Segundo Intensidade de Conhecimento entre {list_years[0]} e {list_years[-1]}'
        , range_x=(0,range_x)
        , barmode='relative'
    )

    if relative != True:
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
    fig.update_layout(
        legend=dict(
            orientation="h"
            , yanchor="bottom"
            , y=-0.45
            , xanchor="left"
            , x=0)
        , title=dict(
            yanchor="top"
            , y=0.91
            , xanchor="left"
            , x=0)
    )   

    return fig

def services_knowledge_evolution_table(list_years, total=True, save_feather=False):

    dict_years = dict()

    for year in list_years:
        df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_motropolises_{year}.ftd'))

        dict_years[year] = df

    df = pd.concat(objs=dict_years.values(), keys=dict_years.keys())


#    df = pd.read_feather(os.path.join(modulepath, f'data/rais_dataframes/ufs_with_motropolises_07to17.ftd'))
    
    df = df[df['knowledge_services'] != 'Without Classification']
    
    df.rename(columns={'Território':'Espaço Metropolitano', 'knowledge_services': 'Tipo'}, inplace=True)

    df = df.reset_index().rename(columns={'level_0': 'Ano'}).drop(columns=['level_1'])

    df = df.groupby(by=['Espaço Metropolitano', 'Tipo', 'Ano'], observed=True).agg(Pessoal=('Pessoal', 'sum'))

    df = df.reset_index()

    df = df[~df['Espaço Metropolitano'].str.startswith('Demais')]

    df['Espaço Metropolitano'] = df['Espaço Metropolitano'].replace(dc.dict_arranjo)

    df = df.pivot_table(values='Pessoal', columns='Ano', index=['Espaço Metropolitano', 'Tipo'], fill_value=0)
    df.rename_axis(columns={'Ano':''}, inplace=True)
    df = df.reset_index()
    
    df['Tipo'].replace(
        {
            'Other less knowledge-intensive services':'Serviços Menos Intensivos em Conhecimento'
            ,'Less knowledge-intensive market services': 'Serviços Menos Intensivos em Conhecimento' 
            ,'Other knowledge-intensive services': 'Outros Serviços Intensivos em Conhecimento'
            ,'Knowledge-intensive market services': 'Serviços de Mercado Intensivos em Conhecimento'
            ,'Knowledge-intensive financial services': 'Serviços Financeiros Intensivos em Conhecimento'
            ,'High-tech knowledge-intensive services': 'De Alta Tecnologia Intensivos em Conhecimento'
        }
        , inplace=True
    )
    
    if total == True:
        df_total = df.reset_index().groupby(['Tipo'], observed=True).sum().reset_index()
        df_total.insert(0, 'Espaço Metropolitano', 'Total')
        df = pd.concat([df.reset_index(), df_total])
        df.set_index(['Espaço Metropolitano', 'Tipo'], inplace=True)
        df = df.drop(columns='index')
        
    if save_feather == True:
        df.columns = df.columns.astype('str')
        df.reset_index().to_feather(os.path.join(modulepath,'data/rais_dataframes/metro_areas_serv_knowledge_evolution_07to17.ftd'))
    
    return df


def serv_knowledge_evolution_line_plot(met='Total', height=700):
    
    if met == 'Total':
        title = 'SIC no Conjunto dos Espaços Metropolitano entre 2007 e 2018'
        
    else:
        title = f'SIC no Espaço Metropolitano de {met} entre 2007 e 2018'
    
    df = pd.read_feather(os.path.join(modulepath, 'data/rais_dataframes/metro_areas_serv_knowledge_evolution_07to17.ftd'))
    df = df.melt(id_vars=['Espaço Metropolitano', 'Tipo'], var_name='Ano', value_name='Pessoal')
    df = df[df['Espaço Metropolitano'] == met]
    df = df.groupby(['Espaço Metropolitano', 'Tipo', 'Ano']).sum().reset_index()
    
    fig = px.line(
        data_frame=df
        , x='Ano'
        , y='Pessoal'
        , color='Tipo'
        , color_discrete_map=
        {
            'Serviços Menos Intensivos em Conhecimento':'rgb(204,204,204)'
            , 'Outros Serviços Intensivos em Conhecimento':'rgb(55,166,165)'
            , 'Serviços de Mercado Intensivos em Conhecimento':'#4C78A8'
            ,'Serviços Financeiros Intensivos em Conhecimento':'rgb(255,242,174)'
            ,'De Alta Tecnologia Intensivos em Conhecimento':'rgb(228,26,28)'
        }
        , title = title
        , height=height
    )
    fig.update_layout(
        legend=dict(
            orientation="h"
            , yanchor="bottom"
            , y=-0.25
            , xanchor="left"
            , x=0)
        , title=dict(
            yanchor="top"
            , y=0.91
            , xanchor="left"
            , x=0)
    )
    
    return fig