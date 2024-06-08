#MatPlotLib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#SQL
import sqlite3
import sqlalchemy

#GUI
import PySimpleGUI as sg

#Pandas
import pandas as pd


sg.theme("BlueMono")
sg.set_options(font=("Bahnschrift", 20), text_color='black')

connection = sqlite3.connect("DATABASE.db")
c = connection.execute("Select * from SignUp")

def exercises():

    conn = sqlalchemy.create_engine('sqlite:///DATABASE.db')

    data = pd.read_sql_table("Exercises", conn)

    exnames = []
    excalories = []
    temp11 = data['Exercise_Name']
    temp12 = data['Burnt_Calories']

    for i in temp11:
        exnames.append(str(i))
    for j in temp12:
        excalories.append(int(j))

    exerimage = [
        [sg.Image("tips.png")]
    ]

    exerburnt = [
        [sg.Text("TRACK EXERCISES", pad=(275,0),font=("Bahnschrift", 30), background_color="powder blue",
                 text_color="dark slate Gray")],
        [sg.Text("Calories burnt = "), sg.Text('_', key='-BURNCAL-', background_color="bisque"),
         sg.Text('/300', background_color="bisque", pad=(0, 10))],
        [sg.Text("Saved Exercises:", text_color="PeachPuff1"),
         sg.Combo(values=exnames,
                  size=(40, 10),
                  key='-EXCOMBO-'
                  )
         ],
        [sg.Text("Track Burnt Calories Directly:", text_color="PeachPuff1"), sg.InputText(key='-EXERDIRECT-', size=(5, 10))],
        [sg.Button("Track", button_color="indianred1 on bisque")],
        [sg.Text("Add new exercises:", text_color="PeachPuff1")],
        [sg.Text("Name:", text_color="Lightgoldenrod1"), sg.InputText(key='-NEWEXER-', size=(10, 10)),
         sg.Text("Calories:", text_color="Lightgoldenrod1"), sg.InputText(key='-NEWBURN-', size=(5, 10))],
        [sg.Button("Add", button_color="indianred1 on bisque")]
    ]

    layexer = [
        [sg.Button("B A C K", button_color="pale violet red", pad=(0, 20)),
         sg.Text('CALORIE TRACKING APPLICATION', expand_x=True, text_color="mistyrose",
                 font=("Bahnschrift", 30, "bold"), justification="center", pad=(20, 0))],
        [sg.Frame("",exerimage),sg.Frame("",exerburnt)]
    ]

    exerwin = sg.Window('Exercises',layexer)

    while True:
        event, values = exerwin.read()
        if event == sg.WIN_CLOSED or event == "B A C K":
            break

        exdirect = values['-EXERDIRECT-']
        savedex = values['-EXCOMBO-']

        if event == "Track" and exdirect == '':
            ecalory = 0
            for i in range(0, len(exnames)):
                if savedex == exnames[i]:
                    ecalory = excalories[i]
                    exerwin['-BURNCAL-'].update((ecalory))
                    connection.execute("""update BurntCal set CalorieBurn=? where Date=?""", (ecalory, datelol,))
                    connection.commit()

        elif exdirect and savedex == '':
            exerwin['-BURNCAL-'].update((exdirect))
            connection.execute("""update BurntCal set CalorieBurn=? where Date=?""", (exdirect, datelol,))
            connection.commit()

        elif event == "Track" and exdirect:
            savedex = values['-EXCOMBO-']
            for i in range(0, len(exnames)):
                if savedex == exnames[i]:
                    ecalory = excalories[i]
                    ecalory = int(ecalory) + int(exdirect)
                    exerwin['-BURNCAL-'].update(ecalory)
                    connection.execute("""update BurntCal set CalorieBurn=? where Date=?""", (ecalory, datelol,))
                    connection.commit()

        if event == "Add":
            exname = values['-NEWEXER-']
            burncalories = values['-NEWBURN-']
            try:
                if int(burncalories) > 0 :
                    connection.execute("Insert into Exercises(Exercise_Name, Burnt_Calories) values(?,?)",
                                       (exname, burncalories))
                    connection.commit()
                    sg.popup("Data inserted")
                else:
                    sg.popup_error("Check values")
            except Exception as e:
                print("Error", e)
    exerwin.close()
def dinner():
    conn = sqlalchemy.create_engine('sqlite:///DATABASE.db')

    data = pd.read_sql_table("Dinner", conn)
    dnames = []
    dcalories = []
    temp9 = data['Food_Name']
    temp10 = data['Calories']

    for i in temp9:
        dnames.append(str(i))
    for j in temp10:
        dcalories.append(int(j))


    dinlay = [
        [sg.Button("B A C K", button_color="pale violet red", pad=(0, 20)),
         sg.Text('CALORIE TRACKING APPLICATION', expand_x=True, text_color="mistyrose",
                 font=("Bahnschrift", 30, "bold"), justification="center", pad=(20, 0))],
        [sg.Text("TRACK DINNER", pad=(275,0),font=("Bahnschrift", 30), background_color="powder blue",
                 text_color="dark slate Gray")],
        [sg.Text("Calories for Dinner ="),sg.Text('_',key='-DINCAL-',background_color="bisque"),sg.Text('/375',background_color="bisque",pad=(0,10))],
        [sg.Text("Saved Dinners:", text_color="PeachPuff1"),
         sg.Combo(values=dnames,
             size=(40,10),
             key='-DCOMBO-'
        )],
        [sg.Text("Track One-Off dinner:", text_color="PeachPuff1"),sg.InputText(key='-DONEOFF-',size=(5,10))],
        [sg.Button("Track",button_color="indianred1 on bisque")],
        [sg.Text("Add new dinners:", text_color="PeachPuff1")],
        [sg.Text("Name:",text_color="Lightgoldenrod1"),sg.InputText(key='-DNEWNAME-',size=(10,10)),
        sg.Text("Calories:",text_color="Lightgoldenrod1"),sg.InputText(key='-DNEWCAL-',size=(5,10))],
        [sg.Button("Add",button_color="indianred1 on bisque")]

    ]

    dinwin = sg.Window("Dinner",dinlay)

    while True:
        event, values = dinwin.read()
        if event == sg.WIN_CLOSED or event == "B A C K":
            break

        doneoff = values['-DONEOFF-']
        dfood = values['-DCOMBO-']

        if event == "Track" and doneoff == '':
            dcalory = 0
            for i in range(0,len(dnames)):
                if dfood == dnames[i]:
                    dcalory = dcalories[i]
                    dinwin['-DINCAL-'].update((dcalory))
                    connection.execute("""update Intakes set Dinner=? where Date=?""", (dcalory, datelol,))
                    connection.commit()

        elif doneoff and dfood=='':
            dinwin['-DINCAL-'].update((doneoff))
            connection.execute("""update Intakes set Dinner=? where Date=?""", (doneoff, datelol,))
            connection.commit()

        elif event == "Track" and doneoff:
            dfood = values['-DCOMBO-']
            for i in range(0,len(dnames)):
                if dfood == dnames[i]:
                    dcalory = dcalories[i]
                    dcalory = int(dcalory) + int(doneoff)
                    dinwin['-DINCAL-'].update(dcalory)
                    connection.execute("""update Intakes set Dinner=? where Date=?""", (dcalory, datelol,))
                    connection.commit()

        if event == "Add":
            dfoodname = values['-DNEWNAME-']
            dcalorieforfood = values['-DNEWCAL-']
            try:
                if int(dcalorieforfood) > 0 :
                    connection.execute("Insert into Dinner(Food_Name, Calories) values(?,?)",
                                       (dfoodname, dcalorieforfood))
                    connection.commit()
                    sg.popup("Data inserted")
                else:
                    sg.popup_error("Check values")
            except Exception as e:
                print("Error", e)


    dinwin.close()

def evensnack():
    conn = sqlalchemy.create_engine('sqlite:///DATABASE.db')

    data = pd.read_sql_table("MornSnack", conn)
    e_names = []
    e_calories = []
    temp7 = data['Food_Name']
    temp8 = data['Calories']

    for i in temp7:
        e_names.append(str(i))
    for j in temp8:
        e_calories.append(int(j))

    esnacklay = [
        [sg.Button("B A C K", button_color="pale violet red", pad=(0, 20)),
         sg.Text('CALORIE TRACKING APPLICATION', expand_x=True, text_color="mistyrose",
                 font=("Bahnschrift", 30, "bold"), justification="center", pad=(20, 0)),
         sg.Button("N E X T", button_color="steel blue")],
        [sg.Text("TRACK EVENING SNACK", pad=(275, 0), font=("Bahnschrift", 30), background_color="powder blue",
                 text_color="dark slate Gray")],
        [sg.Text("Calories for Snack ="), sg.Text('_', key='-MCAL-', background_color="bisque"),
         sg.Text('/187', background_color="bisque", pad=(0, 10))],
        [sg.Text("Saved Snacks:", text_color="PeachPuff1"),
         sg.Combo(values=e_names,
                  size=(40, 10),
                  key='-MCOMBO-'
                  )],
        [sg.Text("Track One-Off snack:", text_color="PeachPuff1"), sg.InputText(key='-MONEOFF-', size=(5, 10))],
        [sg.Button("Track", button_color="indianred1 on bisque")],
        [sg.Text("Add new snacks:", text_color="PeachPuff1")],
        [sg.Text("Name:", text_color="Lightgoldenrod1"), sg.InputText(key='-MNEWNAME-', size=(10, 10)),
         sg.Text("Calories:", text_color="Lightgoldenrod1"), sg.InputText(key='-MNEWCAL-', size=(5, 10))],
        [sg.Button("Add", button_color="indianred1 on bisque")]

    ]

    esnackwin = sg.Window("Morning Snack", esnacklay)

    while True:
        event, values = esnackwin.read()
        if event == sg.WIN_CLOSED or event == "B A C K":
            break

        moneoff = values['-MONEOFF-']
        mfood = values['-MCOMBO-']

        if event == "Track" and moneoff == '':
            mcalory = 0
            for i in range(0, len(e_names)):
                if mfood == e_names[i]:
                    mcalory = e_calories[i]
                    esnackwin['-MCAL-'].update((mcalory))
                    connection.execute("""update Intakes set EveningSnack=? where Date=?""", (mcalory, datelol,))
                    connection.commit()
        elif moneoff and mfood == '':
            esnackwin['-MCAL-'].update((moneoff))
            connection.execute("""update Intakes set EveningSnack=? where Date=?""", (moneoff, datelol,))
            connection.commit()
        elif event == "Track" and moneoff:
            food = values['-MCOMBO-']
            for i in range(0, len(e_names)):
                if food == e_names[i]:
                    mcalory = e_calories[i]
                    mcalory = int(mcalory) + int(moneoff)
                    esnackwin['-MCAL-'].update(mcalory)
                    connection.execute("""update Intakes set EveningSnack=? where Date=?""", (mcalory, datelol,))
                    connection.commit()
        if event == "Add":
            mfoodname = values['-MNEWNAME-']
            mcalorieforfood = values['-MNEWCAL-']
            try:
                if int(mcalorieforfood) > 0:
                    connection.execute("Insert into MornSnack(Food_Name, Calories) values(?,?)",
                                       (mfoodname, mcalorieforfood))
                    connection.commit()
                    sg.popup("Data inserted")
                else:
                    sg.popup_error("Check values")
            except Exception as e:
                print("Error", e)
        if event == "N E X T":
            dinner()
    esnackwin.close()

def lunch():
    conn = sqlalchemy.create_engine('sqlite:///DATABASE.db')

    data = pd.read_sql_table("Lunch", conn)
    lnames = []
    lcalories = []
    temp5 = data['Food_Name']
    temp6 = data['Calories']

    for i in temp5:
        lnames.append(str(i))
    for j in temp6:
        lcalories.append(int(j))

    lunchlay = [
        [sg.Button("B A C K", button_color="pale violet red", pad=(0, 20)),
         sg.Text('CALORIE TRACKING APPLICATION', expand_x=True, text_color="mistyrose",
                 font=("Bahnschrift", 30, "bold"), justification="center", pad=(20, 0)),
         sg.Button("N E X T", button_color="steel blue")],
        [sg.Text("TRACK LUNCH", pad=(275, 0), font=("Bahnschrift", 30), background_color="powder blue",
                 text_color="dark slate Gray")],
        [sg.Text("Calories for Lunch ="), sg.Text('_', key='-LUNCHCAL-', background_color="bisque"),
         sg.Text('/375', background_color="bisque", pad=(0, 10))],
        [sg.Text("Saved Lunches:", text_color="PeachPuff1"),
         sg.Combo(values=lnames,
                  size=(40, 10),
                  key='-LCOMBO-'
                  )],
        [sg.Text("Track One-Off Lunch:", text_color="PeachPuff1"), sg.InputText(key='-LONEOFF-', size=(5, 10))],
        [sg.Button("Track", button_color="indianred1 on bisque")],
        [sg.Text("Add new lunches:", text_color="PeachPuff1")],
        [sg.Text("Name:", text_color="Lightgoldenrod1"), sg.InputText(key='-LNEWNAME-', size=(10, 10)),
         sg.Text("Calories:", text_color="Lightgoldenrod1"), sg.InputText(key='-LNEWCAL-', size=(5, 10))],
        [sg.Button("Add", button_color="indianred1 on bisque")]

    ]

    lunchwin = sg.Window("Lunch", lunchlay)

    while True:
        event, values = lunchwin.read()
        if event == sg.WIN_CLOSED or event == "B A C K":
            break

        loneoff = values['-LONEOFF-']
        lfood = values['-LCOMBO-']

        if event == "Track" and loneoff == '':
            lcalory = 0
            for i in range(0, len(lnames)):
                if lfood == lnames[i]:
                    lcalory = lcalories[i]
                    lunchwin['-LUNCHCAL-'].update((lcalory))
                    connection.execute("""update Intakes set Lunch=? where Date=?""", (lcalory, datelol,))
                    connection.commit()

        elif loneoff and lfood == '':
            lunchwin['-LUNCHCAL-'].update((loneoff))
            connection.execute("""update Intakes set Lunch=? where Date=?""", (loneoff, datelol,))
            connection.commit()

        elif event == "Track" and loneoff:
            lfood = values['-LCOMBO-']
            for i in range(0, len(lnames)):
                if lfood == lnames[i]:
                    lcalory = lcalories[i]
                    lcalory = int(lcalory) + int(loneoff)
                    lunchwin['-LUNCHCAL-'].update(lcalory)
                    connection.execute("""update Intakes set Lunch=? where Date=?""", (lcalory, datelol,))
                    connection.commit()
        if event == "Add":
            lfoodname = values['-LNEWNAME-']
            lcalorieforfood = values['-LNEWCAL-']
            try:
                if int(lcalorieforfood) > 0:
                    connection.execute("Insert into Lunch(Food_Name, Calories) values(?,?)",
                                       (lfoodname, lcalorieforfood))
                    connection.commit()
                    sg.popup("Data inserted")
                else:
                    sg.popup_error("Check values")
            except Exception as e:
                print("Error", e)

        if event == "N E X T":
            evensnack()

    lunchwin.close()
def morningsnack():
    conn = sqlalchemy.create_engine('sqlite:///DATABASE.db')

    data = pd.read_sql_table("MornSnack", conn)
    m_names = []
    m_calories = []
    temp3 = data['Food_Name']
    temp4 = data['Calories']

    for i in temp3:
        m_names.append(str(i))
    for j in temp4:
        m_calories.append(int(j))

    msnacklay = [
        [sg.Button("B A C K", button_color="pale violet red", pad=(0, 20)),
         sg.Text('CALORIE TRACKING APPLICATION', expand_x=True, text_color="mistyrose",
                 font=("Bahnschrift", 30, "bold"), justification="center", pad=(20, 0)),
         sg.Button("N E X T", button_color="steel blue")],
        [sg.Text("TRACK MORNING SNACK", pad=(275, 0), font=("Bahnschrift", 30), background_color="powder blue",
                 text_color="dark slate Gray")],
        [sg.Text("Calories for Snack ="), sg.Text('_', key='-MCAL-', background_color="bisque"),
         sg.Text('/188', background_color="bisque", pad=(0, 10))],
        [sg.Text("Saved Snacks:", text_color="PeachPuff1"),
         sg.Combo(values=m_names,
                  size=(40, 10),
                  key='-MCOMBO-'
                  )],
        [sg.Text("Track One-Off snack:", text_color="PeachPuff1"), sg.InputText(key='-MONEOFF-', size=(5, 10))],
        [sg.Button("Track", button_color="indianred1 on bisque")],
        [sg.Text("Add new snacks:", text_color="PeachPuff1")],
        [sg.Text("Name:", text_color="Lightgoldenrod1"), sg.InputText(key='-MNEWNAME-', size=(10, 10)),
         sg.Text("Calories:", text_color="Lightgoldenrod1"), sg.InputText(key='-MNEWCAL-', size=(5, 10))],
        [sg.Button("Add", button_color="indianred1 on bisque")]

    ]

    msnackwin = sg.Window("Morning Snack", msnacklay)

    while True:
        event, values = msnackwin.read()
        if event == sg.WIN_CLOSED or event == "B A C K":
            break

        moneoff = values['-MONEOFF-']
        mfood = values['-MCOMBO-']

        if event == "Track" and moneoff == '':
            mcalory = 0
            for i in range(0, len(m_names)):
                if mfood == m_names[i]:
                    mcalory = m_calories[i]
                    msnackwin['-MCAL-'].update((mcalory))
                    connection.execute("""update Intakes set MorningSnack=? where Date=?""", (mcalory, datelol,))
                    connection.commit()

        elif moneoff and mfood == '':
            msnackwin['-MCAL-'].update((moneoff))
            connection.execute("""update Intakes set MorningSnack=? where Date=?""", (moneoff, datelol,))
            connection.commit()

        elif event == "Track" and moneoff:
            for i in range(0, len(m_names)):
                if mfood == m_names[i]:
                    mcalory = m_calories[i]
                    mcalory = int(mcalory) + int(moneoff)
                    msnackwin['-MCAL-'].update(mcalory)
                    connection.execute("""update Intakes set MorningSnack=? where Date=?""", (mcalory, datelol,))
                    connection.commit()

        if event == "Add":
            mfoodname = values['-MNEWNAME-']
            mcalorieforfood = values['-MNEWCAL-']
            try:
                if int(mcalorieforfood) > 0:
                    connection.execute("Insert into MornSnack(Food_Name, Calories) values(?,?)",
                                       (mfoodname, mcalorieforfood))
                    connection.commit()
                    sg.popup("Data inserted")
                else:
                    sg.popup_error("Check values")
            except Exception as e:
                print("Error", e)
        if event == "N E X T":
            lunch()
    msnackwin.close()

def breakfasttrack():
    conn = sqlalchemy.create_engine('sqlite:///DATABASE.db')

    data = pd.read_sql_table("Breakfasts", conn)
    names = []
    calories = []
    temp1 = data['Food_Name']
    temp2 = data['Calories']

    for i in temp1:
        names.append(str(i))
    for j in temp2:
        calories.append(int(j))


    breaklay = [
        [sg.Button("B A C K", button_color="pale violet red", pad=(0, 20)),
         sg.Text('CALORIE TRACKING APPLICATION', expand_x=True, text_color="mistyrose",
                 font=("Bahnschrift", 30, "bold"), justification="center", pad=(20, 0)),
         sg.Button("N E X T", button_color="steel blue")],
        [sg.Text("TRACK BREAKFAST", pad=(275,0),font=("Bahnschrift", 30), background_color="powder blue",
                 text_color="dark slate Gray")],
        [sg.Text("Calories for Breakfast ="),sg.Text('_',key='-BREAKCAL-',background_color="bisque"),sg.Text('/375',background_color="bisque",pad=(0,10))],
        [sg.Text("Saved Breakfasts:", text_color="PeachPuff1"),
         sg.Combo(values=names,
             size=(40,10),
             key='-COMBO-'
        )],
        [sg.Text("Track One-Off breakfast:", text_color="PeachPuff1"),sg.InputText(key='-ONEOFF-',size=(5,10))],
        [sg.Button("Track",button_color="indianred1 on bisque")],
        [sg.Text("Add new breakfasts:", text_color="PeachPuff1")],
        [sg.Text("Name:",text_color="Lightgoldenrod1"),sg.InputText(key='-NEWNAME-',size=(10,10)),
        sg.Text("Calories:",text_color="Lightgoldenrod1"),sg.InputText(key='-NEWCAL-',size=(5,10))],
        [sg.Button("Add",button_color="indianred1 on bisque")]

    ]

    breakwin = sg.Window("Breakfast",breaklay)

    while True:
        event, values = breakwin.read()
        if event == sg.WIN_CLOSED or event == "B A C K":
            break

        oneoff = values['-ONEOFF-']
        food = values['-COMBO-']

        if event == "Track" and oneoff == '':
            calory = 0
            for i in range(0,len(names)):
                if food == names[i]:
                    calory = calories[i]
                    breakwin['-BREAKCAL-'].update((calory))
                    connection.execute("""update Intakes set Breakfast=? where Date=?""", (calory, datelol,))
                    connection.commit()

        elif oneoff and food=='':
            breakwin['-BREAKCAL-'].update((oneoff))
            connection.execute("""update Intakes set Breakfast=? where Date=?""", (oneoff, datelol,))
            connection.commit()

        elif event == "Track" and oneoff:
            food = values['-COMBO-']
            for i in range(0,len(names)):
                if food == names[i]:
                    calory = calories[i]
                    calory = int(calory) + int(oneoff)
                    breakwin['-BREAKCAL-'].update(calory)
                    connection.execute("""update Intakes set Breakfast=? where Date=?""", (calory, datelol,))
                    connection.commit()
        if event == "Add":
            foodname = values['-NEWNAME-']
            calorieforfood = values['-NEWCAL-']
            try:
                if int(calorieforfood) > 0 :
                    connection.execute("Insert into Breakfasts(Food_Name, Calories) values(?,?)",
                                       (foodname, calorieforfood))
                    connection.commit()
                    sg.popup("Data inserted")
                else:
                    sg.popup_error("Check values")
            except Exception as e:
                print("Error", e)

        if event == "N E X T":
            morningsnack()

    breakwin.close()

def graphprogress():
    conn = sqlalchemy.create_engine('sqlite:///DATABASE.db')

    data = pd.read_sql_table("WeightProgress", conn)

    massreal = []
    datereal = []
    massdata = data['Mass']
    datedata = data['Date']

    for i in massdata:
        massreal.append(float(i))
    for j in datedata:
        datereal.append(j)

    def create_plot(datereal, massreal):

        plt.plot(datereal, massreal, color="teal", marker='o')
        plt.title("Mass vs Date", fontsize=14)
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Mass', fontsize=14)
        plt.gcf().autofmt_xdate()



        plt.grid(True)
        return plt.gcf()

    graphlay = [
        [sg.Text("Progress Graph")],
        [sg.Canvas(size=(1000, 1000), key='CANVAS')],
        [sg.Button("Exit",button_color="pale violet red")]
    ]

    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    window = sg.Window("PySimpleGUI + MatPlotLip Line Plot", graphlay, finalize=True, element_justification='center')

    draw_figure(window['CANVAS'].TKCanvas, create_plot(datereal, massreal))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break

    window.close()

def intake():
    intakelay = [
        [sg.Text("Your intake for today was:", text_color="indianred1",background_color="bisque"), sg.InputText(key='-INTAKE-',size=(5,10))]
    ]

    caloriesum = connection.execute(
        "Select Breakfast + MorningSnack + Lunch + EveningSnack + Dinner As totalcal From Intakes Where Date=?",
        (datelol,))
    tempsum = caloriesum.fetchall()
    caloriesum = []
    for i in tempsum:
        caloriesum.append((i[0]))

    intakewin = sg.Window('Intake',intakelay,finalize=True)

    intakewin['-INTAKE-'].update(caloriesum[0])

    while True:
        event, values = intakewin.read()
        if event == sg.WIN_CLOSED:
            break

def homepage():

    bmi_col = [
        [sg.Text("BMI CALCULATOR", pad=(55, 10),font=("Bahnschrift", 30), background_color="powder blue", text_color="dark slate Gray")],
        [sg.Text("HEIGHT", text_color="PeachPuff1", pad=(55, 0)), sg.InputText(key='-HEIGHT-', size=(5, 40)),
         sg.Text('(in cm)', text_color="PeachPuff1",pad=(20,0))],
        [sg.VPush()],
        [sg.Text("MASS", text_color="PeachPuff1", pad=(55, 0)), sg.InputText(key='-MASS-', size=(5, 40),pad=(22,0)),
         sg.Text('(in kg)', text_color="PeachPuff1")],
        [sg.Button("C A L C U L A T E", pad=(115, 10), button_color="indianred1 on bisque")],
        [sg.Text("Your BMI:", text_color="burlywood1",pad=(10,20)), sg.InputText(key='-BMI-', size=(5, 40)), sg.Text(key='-CHECK-',text_color="Dark slate gray")]
    ]

    intake_col = [
        [sg.Text("TRACK INTAKE",font=("Bahnschrift", 30), pad=(85, 5), background_color="powder blue", text_color="dark slate Gray")],
        [sg.Button("Breakfast",pad=(5,0),button_color="lightgoldenrod1 on SteelBlue1"),
         sg.Button("Morning Snack",pad=(5,0),button_color="lightgoldenrod1 on SteelBlue1")
        ,sg.Button("Lunch",button_color="lightgoldenrod1 on SteelBlue1")],
        [sg.Button("Evening Snack",button_color="indianred1 on bisque"),sg.Button("Dinner",button_color="indianred2 on bisque")],
        [sg.Image("caloricintake.png",expand_x=True)]
    ]


    calories_imagecol = [
        [sg.Image("calories.png")]
    ]

    calories_colsub = [
        [sg.Text("CALORIES", pad=(120, 20), font=("Bahnschrift", 30), background_color="powder blue",
                 text_color="dark slate Gray")],
        [sg.Text("To stay within your goal of 8 weeks:",pad=(0,10))],
        [sg.Text("Eat upto"),sg.Text("1500 kcal",background_color="bisque",pad=(0,10)),sg.Text("daily")],
        [sg.Text("Burn at least"),sg.Text("300 kcal",background_color="bisque",pad=(0,10)),sg.Text("daily")],
        [sg.Button("View your caloric intake", pad=(20, 10), button_color="indianred1 on papayawhip")],
        [sg.Button("Track your burnt calories", pad=(20, 10), button_color="indianred1 on papayawhip")]

    ]

    calories_colmain = [
        [sg.Frame("", calories_colsub),sg.Frame("",calories_imagecol)]
    ]
    mass_col = [
        [sg.Text("PROGRESS", pad=(75, 10), font=("Bahnschrift", 30), background_color="powder blue",
                 text_color="dark slate Gray")],
        [sg.Text("Select Today's date", text_color="LightGoldenrod2")],
        [sg.InputText(size=(10,0),key='-DATE-'),sg.CalendarButton("Date",target="-DATE-",format="%Y-%m-%d")],
        [sg.Text("Enter Mass:", text_color="PeachPuff1",pad=(5,10)),sg.InputText(key='-CURRENT-', size=(5, 40),pad=(10,0))],
        [sg.Text("Your Target Mass is:",pad=(5,10), text_color="PeachPuff1"),sg.Text("   65   ",background_color="White")],
        [sg.Button("Submit Today's Data", pad=(20, 10), button_color="bisque on indianred1")],
        [sg.Button("View Graph of Progress",pad=(20,10), button_color="indianred1 on bisque")]
    ]

    homelay = [
        [sg.Button("B A C K", button_color="pale violet red", pad=(0, 20)),
         sg.Text('CALORIE TRACKING APPLICATION', expand_x=True, text_color="mistyrose",
                 font=("Bahnschrift", 30, "bold"), justification="center", pad=(20, 0)),
         sg.Button("N E X T", button_color="steel blue")],

        [sg.Frame("",bmi_col),sg.Frame("",intake_col)],
        [sg.Frame("",mass_col),sg.Frame("",calories_colmain)]

    ]

    homewin = sg.Window("Home Page",homelay)
    while True:
        event, values = homewin.read()
        global datelol
        datelol = values['-DATE-']
        if event == sg.WIN_CLOSED or event == "B A C K":
            break

        if event == "C A L C U L A T E":
            masz = float(values["-MASS-"])
            heiz = float(values["-HEIGHT-"])
            if masz<0 or heiz<0:
                sg.popup_error("Please enter correct values")
            else:
                heiz = heiz/100
                bmlol = masz/(heiz*heiz)
                if bmlol < 18.5:
                    checkbm = "Underweight"
                elif (bmlol >= 18.5 and bmlol <=24.9):
                    checkbm = "Normal"
                elif (bmlol >= 25 and bmlol <=29.9):
                    checkbm = "Overweight"
                elif (bmlol >= 30 and bmlol <= 34.9):
                    checkbm = "Obese"
                else:
                    checkbm = "Morbidly Obese"
                bmlol=round(bmlol,1)
            homewin['-BMI-'].update(bmlol)
            homewin['-CHECK-'].update(checkbm)

        if event == "Submit Today's Data":
            thedate = values['-DATE-']
            masss = values['-CURRENT-']
            try:
                    connection.execute("Insert into WeightProgress(Mass,Date) values(?,?)",
                                       (masss,thedate))
                    connection.commit()
                    sg.popup("Data inserted")
            except Exception as e:
                print("Error", e)
            try:
                connection.execute("Insert into Intakes(Date) values(?)",(thedate,))
                connection.commit()
            except Exception as e:
                print("error",e)
            try:
                connection.execute("Insert into BurntCal(Date) values(?)",(thedate,))
                connection.commit()
            except Exception as e:
                print("error",e)
        if event == "View Graph of Progress":
            graphprogress()
        if event == "Breakfast":
            breakfasttrack()
        if event == "Morning Snack":
            morningsnack()
        if event == "Lunch":
            lunch()
        if event == "Evening Snack":
            evensnack()
        if event == "Dinner":
            dinner()
        if event == "View your caloric intake":
            intake()
        if event == "Track your burnt calories" or event == "N E X T":
            exercises()

    homewin.close()


flag = False

layout = [
    [sg.Text("CALORIE TRACKING APPLICATION",expand_x=True, text_color="mistyrose",font=("Bahnschrift",40,"bold"),justification="center",pad=(0,20))],
    [sg.Text("Username",text_color="PeachPuff1"), sg.InputText(key='-USERNAME-')],
    [sg.Text('Password',text_color="PeachPuff1"), sg.InputText(key='-PASSWORD-')],
    [sg.Button("L O G I N",expand_x=True,button_color="sea green")],
    [sg.Button("C A N C E L",expand_x=True,button_color="pale violet red")]
]


win = sg.Window("Login Form", layout)

while True:
    event, values = win.read()
    if event == sg.WIN_CLOSED or event == "C A N C E L":
        break
    if event == "L O G I N":
        try:
            alldatadb = connection.execute("select Username, Password from SignUp")
            loginname = values['-USERNAME-']
            loginpass = values['-PASSWORD-']

            for eachrow in alldatadb:
                if loginname == eachrow[0] and loginpass == eachrow[1]:
                    flag = True
                    homepage()
            if flag == False:
                sg.popup_error("Check Username or Password.")

        except Exception as e:
            print(f"Error in sql: {e}")

    win.close()
