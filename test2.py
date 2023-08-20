


import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy
from matplotlib import dates as mpl_dates

conn = sqlalchemy.create_engine('sqlite:///DATABASE.db')

data = pd.read_sql_table("WeightProgress",conn)


unemprate = []
year = []
massdata = data['Mass']
datedata = data['Date']

for i in massdata:
    unemprate.append(float(i))
for j in datedata:
    year.append(j)



def create_plot(year, unemprate):
    plt.plot(year,unemprate,color="teal", marker = 'o')
    plt.title("Unemployment rate vs Year", fontsize = 14)
    plt.xlabel('Year',fontsize = 14)
    plt.ylabel('Unemployment Rate',fontsize = 14)
    plt.grid(True)
    return plt.gcf()

layout = [
    [sg.Text("Line plot")],
    [sg.Canvas(size=(1000,1000), key='CANVAS')],
    [sg.Exit()]
]

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top',fill='both',expand=1)
    return figure_canvas_agg

window = sg.Window("PySimpleGUI + MatPlotLip Line Plot",layout,finalize=True,element_justification='center')

draw_figure(window['CANVAS'].TKCanvas,create_plot(year,unemprate))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
