import streamlit as st
import pandas as pd

import functions.backend.sessionState as sessionState
import functions.frontend.sidebar as sidebar
import functions.utils.columns as columns
import functions.frontend.analise.barChart as barChartAnalise

# Variável de estado que vamos usar nessa página
sessionState.using_state(['downloaded_data'])

# Mostra a sidebar
filtered_df = sidebar.get_sidebar()

# PAGE STARTS HERE
st.markdown("# Análises")

textWarning = 'Nesta seção, convidamos você a realizar uma análise exploratória dos dados de COVID-19. A análise exploratória é uma etapa fundamental para compreender as tendências e padrões nos dados, proporcionando insights valiosos sobre o impacto da pandemia. Para começar, selecione as regiões geográficas de interesse e as variáveis que deseja analisar. Explore os gráficos interativos, personalize a visualização conforme suas preferências e interprete os dados em busca de conclusões relevantes. Compartilhe suas descobertas e insights para contribuir para uma compreensão mais aprofundada da situação da COVID-19'

if sessionState.get_state('downloaded_data') is not True:
    st.markdown(textWarning)
    st.warning("Faça o download dos dados antes de continuar")
elif filtered_df.empty:
    st.markdown(textWarning)
    st.warning("Selecione os filtros antes de continuar")

else:
    defaultVariables = ['confirmed', 'deaths', 'recovered']
    variablesSelected = st.multiselect(
        "Selecione as variáveis que deseja analisar",
        options = columns.getVariableTranslationList(columns.getColumnGroups('variaveis')),
        default = columns.getVariableTranslationList(defaultVariables)
    )

    # Espaçador
    st.text("")

    variablesKeys = columns.getVariableKeyList(variablesSelected)

    barChartColumn, insightsColumn = st.columns(2, gap="large")

    with barChartColumn:
        # st.markdown("### Gráfico de Barras")
        barChartAnalise.draw(filtered_df, variablesKeys)

    with insightsColumn:
        st.markdown("### Insights")
        st.write("Aqui vão os insights")

    st.markdown("### Gráfico de Linha")
    lineChartDf = filtered_df.copy()
    lineChartDf = lineChartDf.rename(columns=columns.getVariableTranslationDict())

    st.line_chart(lineChartDf, x=columns.getVariableTranslation('date'), y=variablesSelected, use_container_width=True)