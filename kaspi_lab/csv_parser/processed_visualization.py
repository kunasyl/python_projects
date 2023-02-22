
import pandas as pd
import cx_Oracle
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"


# DB connection

conn = cx_Oracle.connect(
    user = "connie",
    password = "connie",
    dsn = "localhost/xepdb1"
)

cur = conn.cursor()
cur.execute("SELECT * FROM V_PROCESSED")
res = cur.fetchall()
cur.close()


# V_PROCESSED dataframe creation

df = pd.DataFrame.from_records(res)
df.columns = ['Region','Year','Month','Max open price','Min low price']
df['Date'] = pd.to_datetime(df[['Year','Month']].assign(day=1))


# Visualization

regions = list(df['Region'].unique())

fig = go.Figure()

fig.add_trace(
    go.Scatter(x=df['Date'], y=df[df['Region'] == regions[0]]['Max open price'], name='Max open price', visible=True),
)

fig.add_trace(
    go.Scatter(x=df['Date'], y=df[df['Region'] == regions[0]]['Min low price'], name='Min low price', visible=True)
)

buttons = []
for region in regions:
    buttons.append(dict(method='restyle',
                        label=region,
                        visible=True,
                        args=[{'y':[df[df['Region'] == region]['Max open price'],
                                    df[df['Region'] == region]['Min low price']],
                               'x':[df['Date']],
                               'type':'scatter'}]))

updatemenu = []
menu = dict()
updatemenu.append(menu)
updatemenu[0]['buttons'] = buttons
updatemenu[0]['direction'] = 'down'
updatemenu[0]['showactive'] = True

fig.update_layout(updatemenus=updatemenu)

fig.show()

