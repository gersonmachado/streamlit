import streamlit as st
import pandas as pd
#############
# Anotações #
#############
# pip install streamlit
# streamlit run NomeDoProjeto.py
# pip install streamlit-tags Para importar os módulos de tags/categorias no filtro
# pip install altair<5  Para instalar versão inferior a 5, tratando o erro que deu.



st.write('Hello world!')
st.header('Tabela Teste')

# Dataframe
df = pd.DataFrame({'team': ['Team 1', 'Team 1', 'Team 2',
                            'Team 3', 'Team 2', 'Team 3'],
                   'Subject': ['Math', 'Science', 'Science',
                               'Math', 'Science', 'Math'],
                   'points': [10, 8, 10, 6, 6, 5]})

# display
st.dataframe(data=df)
st.table(data=df)

st.metric(label="Temperatura", value="32 °C", delta="1.2 °C")

st.header('Criando gráfico')
import numpy as np
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.area_chart(chart_data)


st.button('Botão')

st.sidebar.header('Lendo arquivo JSON')

st.sidebar.json({
    'foo': 'bar',
    'baz': 'boz',
    'stuff': [
        'stuff 1',
        'stuff 2',
        'stuff 3',
        'stuff 5',
    ],
})

st.markdown('## Teste Markdown. st.markdown')
st.write('Hello, *World!*  :sunglasses:')

st.caption('Esta é uma string que explica algo acima. com <st.caption>')

st.write('st.code Para adicionar códigos')
code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language='python')


# from streamlit_tags import st_tags
# from streamlit_tags import st_tags_sidebar
from streamlit_tags import * #Para importar os dois modos de colocar keywords

#Keyword na pág principal
keywords = st_tags(
    label='# Enter Keywords:',
    text='Press enter to add more',
    value=['Zero', 'One', 'Two'],
    suggestions=['five', 'six', 'seven', 'eight', 'nine', 'three', 'eleven', 'ten', 'four'],
    maxtags = 4,
    key='1')

#Keyword na pág lateral
keywords = st_tags_sidebar(
    label='# Enter Keywords:',
    text='Press enter to add more',
    #Valores devem ser passados em formato de lista
    value=['Zero', 'One', 'Two'],
    suggestions=['five', 'six', 'seven', 'eight', 'nine', 'three', 'eleven', 'ten', 'four'],
    maxtags = 4,
    key='2')

st.header('Testando variável:')
st.caption('Como captar texto digitado e aplicar ao código/função')

var = st.text_input('Adicione um valor:')
st.write(f'Valor inserido: {var}')


st.header('Testando mapa:')

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(df)


# Yfinance com gráfico para comparação de ativos
import yfinance as yf

from datetime import datetime, timedelta

# Lista de tickers para comparar
tickers = ['VINO11.SA', 'MXRF11.SA', 'PETR3.SA', 'VALE3.SA']

# Função para baixar dados de múltiplos tickers
def get_data(tickers, start_date, end_date):
    data = {}
    for ticker in tickers:
        df = yf.download(ticker, start=start_date, end=end_date)
        data[ticker] = df['Close']
    return pd.DataFrame(data)

# Definir o intervalo de datas
end_date = datetime.today().strftime('%Y-%m-%d')  # Data de hoje
start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')  # Data um ano atrás

# Obter os dados
data = get_data(tickers, start_date, end_date)

# Verificar se os dados foram baixados corretamente
if data.empty:
    st.error("Não foram encontrados dados para os tickers fornecidos.")
else:
    # Mostrar os dados em uma tabela
    st.write(data.head())

    # Adicionar título ao gráfico
    st.subheader('Comparação de Preços de Fechamento')

    # Plotar o gráfico de linha para vários ativos
    st.line_chart(data)