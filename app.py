#import semua modules
import numpy as np
import dash
from dash import dcc, html, Output, Input, State
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# from main import *

#inisiasi aplikasi
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


#membaca file
sheet_inflow = "inflow"
sheet_outflow = "outflow"
url_inflow = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQWYZulM9HeQR8XmcBD9EHnS2-ZhdO8fnnHqSsPmKqh-qis_y95Ixitz0XVaMDoXm8q8b0e0Ap5xAa-/pub?gid=1924073950&single=true&output=csv&sheet={Air_Masuk}"
url_outflow = url="https://docs.google.com/spreadsheets/d/e/2PACX-1vQWYZulM9HeQR8XmcBD9EHnS2-ZhdO8fnnHqSsPmKqh-qis_y95Ixitz0XVaMDoXm8q8b0e0Ap5xAa-/pub?gid=1925455528&single=true&output=csv&sheet={Air_Keluar}"
df_inflow = pd.read_csv(url_inflow)
df_outflow = pd.read_csv(url_outflow)


#membangun komponen
header = html.H1("Aplikasi Simulasi Kapasitas Embung C ITERA", style={'textAlign': 'center'})
subtitle = html.H2("MK Kapita Selekta Matematika Komputasi (MA4103) Kelompok 1", style={'textAlign': 'center'})
inflow_fig = go.FigureWidget()
inflow_fig.add_scatter(name='Inflow', x=df_inflow['Bulan'], y=df_inflow['Debit Air Hujan (M3/Bulan)'])
inflow_fig.layout.title = 'Debit Air Masuk'

outflow_fig = go.FigureWidget()
outflow_fig.add_scatter(name='Outflow', x=df_outflow['Bulan'], y=df_outflow['Debit Air Menguap (M3/Bulan)'])
outflow_fig.layout.title = 'Debit Air Keluar'

simulation_fig = go.FigureWidget()
#simulation_fig.add_scatter(name='Outflow', x=df_outflow['Bulan'])
simulation_fig.layout.title = 'Simulation'


#layout aplikasi
app.layout = html.Div(
    [
        dbc.Row([header, subtitle]),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=inflow_fig)]), 
                dbc.Col([dcc.Graph(figure=outflow_fig)])
            ]
            ),
        html.Div(
            [
                html.Button('Run', id='run-button', n_clicks=0)
            ],
            style = {'textAlign': 'center'}
        ), 
        html.Div(id='output-container-button', children='Klik run untuk menjalankan simulasi.', style = {'textAlign': 'center'}),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id='simulation-result', figure=simulation_fig)])
            ]
        )
    ]
    
)

#interaksi aplikasi
@app.callback(
    Output(component_id='simulation-result', component_property='figure'),
    Input('run-button', 'n_clicks')
)


def graph_update(n_clicks):
    # filtering based on the slide and dropdown selection
    if n_clicks >=1:
        #program numerik ---start----
        inout = df_inflow['Debit Air Hujan (M3/Bulan)'].values - df_outflow['Debit Air Menguap (M3/Bulan)'].values
        N = len(inout)
        u = np.zeros(N)
        u0 = 58420 # Volume Embung Awal dari UPT Kawasan. Satuan m^3
        u[0] = u0
        dt = 1

        #metode Euler
        for n in range(N-1):
            u[n + 1] = u[n] + dt*inout[n]
        #program numerik ---end----


        # the figure/plot created using the data filtered above 
        simulation_fig = go.FigureWidget()
        simulation_fig.add_scatter(name='Simulation', x=df_outflow['Bulan'], y=u)
        simulation_fig.layout.title = 'Simulation'

        return simulation_fig
    else:
        simulation_fig = go.FigureWidget()
        simulation_fig.layout.title = 'Simulation'

        return simulation_fig

    


#jalankan aplikasi
if __name__ == '__main__':
    app.run_server(debug=True)
