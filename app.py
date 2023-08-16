import streamlit as st
import pandas as pd
import requests

from io import BytesIO


#Config Título
st.set_page_config(
    page_title="Webscrap Bets",
    page_icon="♠",
)


#Informações para fingir ser um navegador
header = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

#Get HTML
re = requests.get('https://www.soccerstats.com/matches.asp?matchday=1&listing=1', headers=header)
re2 = requests.get("https://www.soccerstats.com/matches.asp?matchday=1&listing=2", headers=header)

#Read Text > Dataframes
df1 = pd.read_html(re.text)
df2 = pd.read_html(re2.text)

#Pegando data da tabela tomorrow
texto = df1[5][2].values
data = ', '.join(texto)

jogos_hoje1 = df1[7]
jogos_hoje1 = jogos_hoje1[['Country', '2.5+',   '1.5+', 'GA',   'GF',
                           'TG',    'PPG',  'GP', 'Unnamed: 9',
                           'Unnamed: 10', 'Unnamed: 11', 'GP.1',
                           'PPG.1', 'TG.1', 'GF.1', 'GA.1', '1.5+.1',   '2.5+.1']]

jogos_hoje1.columns = ['Pais', 'Over25_H', 'Over15_H', 'g_sofridos_H', 'g_marcados_H',
                       'gmedia_H', 'PPG_H', 'num_partidas_H', 'Home', 'Hora', 'Away',
                       'num_partidas_A', 'PPG_A', 'gmedia_A', 'g_marcados_A',
                       'g_sofridos_A','Over15_A','Over25_A']

jogos_hoje2 = df2[7]
jogos_hoje2 = jogos_hoje2[['BTS',  'W%',  'BTS.1', 'W%.1']]
jogos_hoje2.columns = ['BTTS_H', '%WIN_H', 'BTTS_A', '%WIN_A']

jogos_hoje = pd.concat([jogos_hoje1, jogos_hoje2], axis=1)
jogos_hoje = jogos_hoje[['Pais', 'Hora', 'Home', 'Away', '%WIN_H', '%WIN_A', 'Over15_H', 'Over25_H',
                         'Over15_A', 'Over25_A', 'BTTS_H', 'BTTS_A',
                        'g_sofridos_H', 'g_marcados_H', 'gmedia_H', 'PPG_H', 'num_partidas_H',
                         'g_sofridos_A', 'g_marcados_A','gmedia_A', 'PPG_A', 'num_partidas_A']]


# Ordenando lista/tabela
jogos = jogos_hoje.sort_values('Hora')
# Ajuste de horas por menos 4.
jogos['Hora'] = pd.to_datetime(jogos['Hora']) - pd.DateOffset(hours=4)
# Ajustar o formato de hora e minuto
jogos['Hora'] = pd.to_datetime(jogos['Hora'], format='%H:%M').dt.time
# Eliminar jogos que não possuem dados
jogos = jogos.dropna()

#Reset index
jogos.reset_index(inplace=True, drop=True)


resultado = jogos
# Remover o % dos dados de porcentagem para conversão de type
resultado = resultado.replace('%','', regex=True)
# obs: Regex informa que não é para dar replace em palavras inteiras, mas sim em uma unidade do texto

# Converter type das colunas de porcentagem
resultado['%WIN_H'] = resultado['%WIN_H'].astype(float)
resultado['%WIN_A'] = resultado['%WIN_A'].astype(float)
resultado['Over15_H'] = resultado['Over15_H'].astype(float)
resultado['Over25_H'] = resultado['Over25_H'].astype(float)
resultado['Over15_A'] = resultado['Over15_A'].astype(float)
resultado['Over25_A'] = resultado['Over25_A'].astype(float)
resultado['BTTS_H'] = resultado['BTTS_H'].astype(float)
resultado['BTTS_A'] = resultado['BTTS_A'].astype(float)

# Filtrando
filtro_over25 = ((resultado.g_sofridos_H + resultado.g_marcados_H + resultado.g_sofridos_A + resultado.g_marcados_A) / 2 >= 3) & (
                            (resultado.Over25_H + resultado.Over25_A) / 2 >= 60)
over25 = resultado[filtro_over25]
over25.reset_index(inplace=True, drop=True)

filtro_over15 = ((resultado.Over15_H + resultado.Over15_A)/2 >= 74) & ((resultado.Over25_H + resultado.Over25_A)/2 >= 50)
over15 = resultado[filtro_over25]
over15.reset_index(inplace=True, drop=True)

filtro_btts = (((resultado.g_marcados_H + resultado.g_sofridos_A)/2 >=1.5) & (resultado.g_sofridos_H + resultado.g_marcados_A)/2 >=1.5)

overbtts = resultado[filtro_btts]
overbtts.reset_index(inplace=True, drop=True)

from datetime import date
st.write('Dados para os jogos de hoje')
st.caption(date.today())

@st.cache
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

# Para função save xslx funcionar
def convert_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        resultado.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'})
        worksheet.set_column('A:A', None, format1)
        writer.close() #Correção: usa-se writer.close() e não save()
        processed_data = output.getvalue()
        return processed_data

st.sidebar.caption('Clique para iniciar')
if st.sidebar.button('Over2.5'):

    resultado = over25
    st.dataframe(data=resultado)

    col1, col2 = st.columns(2)
    with col1:
        download = convert_df(resultado)
        st.download_button("DOWNLOAD CSV", download, "file.csv",
                           "text/csv", key='download-csv')

    with col2:

        #Chamando botão de download para Excel
        df_xlsx = convert_excel(resultado)
        st.download_button(label='DOWNLOAD EXCEL',
                           data=df_xlsx,
                           file_name='df_test.xlsx')

if st.sidebar.button('Over1.5'):
    resultado = over15
    st.dataframe(data=resultado)

    col1, col2 = st.columns(2)
    with col1:
        download = convert_df(resultado)
        st.download_button("DOWNLOAD CSV", download, "file.csv",
                           "text/csv", key='download-csv')

    with col2:
        # Chamando botão de download para Excel
        df_xlsx = convert_excel(resultado)
        st.download_button(label='DOWNLOAD EXCEL',
                           data=df_xlsx,
                           file_name='df_test.xlsx')

if st.sidebar.button('BTTS'):
    resultado = overbtts
    st.dataframe(data=resultado)

    col1, col2 = st.columns(2)
    with col1:
        download = convert_df(resultado)
        st.download_button("DOWNLOAD CSV", download, "file.csv",
                           "text/csv", key='download-csv')

    with col2:
        # Chamando botão de download para Excel
        df_xlsx = convert_excel(resultado)
        st.download_button(label='DOWNLOAD EXCEL',
                           data=df_xlsx,
                           file_name='df_test.xlsx')



from streamlit_tags import * #Para importar os dois modos de colocar keywords

#Keyword na pág lateral
keywords = st_tags_sidebar(
    label='# Remover dados que contenham:',
    text='Clique para adicionar mais',
    #Valores devem ser passados em formato de lista
    value=[' W'],
    suggestions=['five', 'six', 'seven'],
    maxtags = 1,
    key='1')


if st.sidebar.button('FILTRAR'):
    filtrar = [keywords]
    if filtrar[0]:
        df1 = resultado[~resultado.Home.str.contains('|'.join(filtrar[0]))]
        st.dataframe(data=df1)

        col1, col2 = st.columns(2)
        with col1:
            download = convert_df(df1)
            st.download_button("DOWNLOAD CSV", download, "file.csv",
                               "text/csv", key='download-csv')

        with col2:
            # Chamando botão de download para Excel
            df_xlsx = convert_excel(df1)
            st.download_button(label='DOWNLOAD EXCEL',
                               data=df_xlsx,
                               file_name='df_test.xlsx')


    else:
        st.write('Filtro Vazio!')


st.sidebar.write(keywords)

