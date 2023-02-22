import plotly.graph_objs as go
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime
# conda install -c anaconda scikit-learn
from sklearn.linear_model import LinearRegression #(conda install -c anaconda scikit-learn)

# data sample
nperiods=200
np.random.seed(123)
df = pd.DataFrame(np.random.randint(-10,12,size=(nperiods, 4)), columns=list('ABCD'))
datelist = pd.date_range(datetime(2020, 1, 1).strftime('%Y-%m-%d'), periods=nperiods).tolist()
df['dates'] = datelist
df = df.set_index(['dates'])
df.index = pd.to_datetime(df.index)
df.iloc[0]=0
df=df.cumsum()

# build dataframe df_reg with linear models using sklearn
# for each column in df
df_reg = pd.DataFrame()
# regression
for col in df:
    #print(col)
    reg = LinearRegression().fit(np.vstack(np.arange(0, len(df))), df[col].values)
    df_reg[col+'_model'] = reg.predict(np.vstack(np.arange(0, len(df))))


#plotly
fig=go.Figure()

# set up one trace for source data in df
# and one trace for each linear model in df_reg
fig.add_trace(go.Scatter(x=df.index,
                             y=df[df.columns[0]],
                             visible=True))

fig.add_trace(go.Scatter(x=df.index,
                             y=df_reg[df_reg.columns[0]],
                             visible=True))
# Define updatemenus
updatemenu=[]
buttons=[]

# add buttons to select column in df
# and the associated linear model in df_reg
for col in df.columns:
    buttons.append(dict(method='restyle',
                        label=col,
                        visible=True,
                        args=[{'y':[df[col], df_reg[col+'_model']],
                               'x':[df.index],
                               'type':'scatter'}],
                        )
                  )

# some adjustments to the updatemenus
updatemenu=[]
your_menu=dict()
updatemenu.append(your_menu)

updatemenu[0]['buttons']=buttons
updatemenu[0]['direction']='down'
updatemenu[0]['showactive']=True

# add dropdown menus to the figure
fig.update_layout(showlegend=False, updatemenus=updatemenu)
fig.show()