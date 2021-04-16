
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
pd.options.display.float_format = '{:,.2f}'.format
pd.options.display.max_rows = 200
import plotly.express as px
import app_rais.dicts_constants as dc
import app_rais.analytics_industries as ind
import json
import geopandas as gpd
import bamboolib as bam
import streamlit as st;

@st.cache
def ind_tech():
    fig, df = ind.ind_tech_level_evolution_dynamic(
        list_years=list(range(2000,2019))
        , list_ufs=['PR']
        , range_x=220_000
        , list_tec_level=None  
        , relative=False
        , focus='Médio-Alto'     
    #    , exclude_territory_starts_with='Demais'
        , list_include_territory=None
        , height=550
    )
    return fig

@st.cache
def ind_tech_relative():
    fig, df = ind.ind_tech_level_evolution_dynamic(
        list_years=list(range(2000,2019))
        , list_ufs=['PR']
        , range_x=220_000
        , list_tec_level=None  
        , relative=True
    #    , focus='Médio-Alto'     
    #    , exclude_territory_starts_with='Demais'
        , list_include_territory=None
        , height=550
    )

    return fig

def get_df_concentration():
    df_ind = pd.read_pickle('df_inds_rms.pkl')
    rms = st.multiselect(
        "Escolhas RMs"
        , list(df_ind['Território'].unique())
        , df_ind['Território'].unique()
        )
    data = df_ind.loc[df_ind['Território'].isin(rms)]

    return data


st.title('Nome do meu APP')

st.sidebar.title("Painel de Navegação")
selection = st.sidebar.radio("Componente", ['Empregados da Indústria por Nível Tecnológico', 'Empregados da Indústria por Nível Tecnológico (%)', 'Concentração Metropolitana dos Níveis Tecnológicos'])

if selection == 'Empregados da Indústria por Nível Tecnológico':

    fig = ind_tech()
    st.plotly_chart(fig)

elif selection == 'Empregados da Indústria por Nível Tecnológico (%)':

    fig2 = ind_tech_relative()

    st.plotly_chart(fig2)

else:

    df = get_df_concentration()
            
    st.write(df)