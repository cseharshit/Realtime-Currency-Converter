from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from dotenv import load_dotenv
import requests, json
import os

BASE_DIR = os.path.dirname(__file__)
load_dotenv('.env')

def fetch_currency_list():
    key = os.getenv('API_KEY')
    parameters = {"api_key": key, "format": "json"}
    url = "https://api.getgeoapi.com/api/v2/currency/list"
    response = requests.get(url, parameters)
    currencies=response.json()['currencies']
    return currencies

def create_widgets():
    global variable1,variable2
    currencies = fetch_currency_list()
    currency_list = [(value+" ("+ key+ ")") for key,value in currencies.items()]

    app_label = Label(
        app, text="Realtime Currency Converter!", font=("Comic Sans MS", 30), justify="center",fg="#000000", bg="#FFFFFF")
    app_label.grid(row=1, column=1, pady=10)

    #INPUT AMOUNT
    enter_amount_label = Label(app, text="Enter amount: ", bg="#FFFFFF", fg="#000000", font=("Comic Sans MS", 10), justify="center")
    enter_amount_label.grid(row=3, column=0, padx=20, pady=10)
    
    global amount
    amount = Entry(app, width=25, textvariable=amount1, bg="#FFFFFF", fg="#000000", font=("Comic Sans MS", 10), justify="center", borderwidth=2)
    amount.grid(row=3, column=1, padx=20, pady=10)

    #INPUT CURRENCY
    from_currency_label = Label(app, text="From Currency: ", bg="#FFFFFF", fg="#000000", font=("Comic Sans MS", 10), justify="center")
    from_currency_label.grid(row=4, column=0, padx=20, pady=10)

    variable1 = StringVar(app)
    variable1.set("US Dollar (USD)")
    from_currency_menu = ttk.Combobox(app, textvariable=variable1, values=currency_list, width=25 , font=("Comic Sans MS", 10), justify="center")
    from_currency_menu.grid(row=4, column=1, padx=20, pady=10)

    #Convert CURRENCY
    to_currency_label = Label(app, text="To Currency: ", bg="#FFFFFF", fg="#000000", font=("Comic Sans MS", 10), justify="center")
    to_currency_label.grid(row=5, column=0, padx=20, pady=10)
    
    variable2 = StringVar(app)
    variable2.set("Indian Rupee (INR)")
    to_currency_menu = ttk.Combobox(app, textvariable=variable2, values=currency_list, width=25, font=("Comic Sans MS", 10), justify="center")
    to_currency_menu.grid(row=5, column=1, padx=20, pady=10)

    #BUTTONS
    switch_button = Button(app, width = 2, text = "↑↓", command = switch, justify="center", bg="#FFFFFF", fg="#000000")
    switch_button.grid(row = 5, column = 2, padx=20,pady=10)
    convert_button = Button(app, width=10, text="Convert",
                         command=Convert, bg="#05E8E0", fg="#000000", font=("Comic Sans MS", 12), justify="center")
    convert_button.grid(row=6, column=1, padx=20, pady=10)

    clear_button = Button(app, text="Clear", width=10,
                       command=clear, bg="#05E8E0", fg="#000000", font=("Comic Sans MS", 12), justify="center")
    clear_button.grid(row=7, column=1, padx=20, pady=10)

    #CONVERTED AMOUNT
    converted_currency_label = Label(app, text="Converted Amount: ", bg="#B4E657", fg = '#000000',font=("Comic Sans MS", 12), justify="center")
    converted_currency_label.grid(row=8, column=0, padx=20, pady=10)

    global converted_amount
    converted_amount = Entry(app, width=25, font=("Comic Sans MS", 10), justify="center")
    converted_amount.grid(row=8, column=1, padx=20, pady=10)

def strip_currency(currency):
    return currency.split(' ')[-1].strip('()')

def switch():
     temp= variable2.get()
     variable2.set(variable1.get())
     variable1.set(temp)

def Convert():
    converted_amount.delete(0, END)
    var1 = strip_currency(variable1.get())
    var2 = strip_currency(variable2.get())
    key = os.getenv('API_KEY')
    parameters = {"api_key": key,"from": var1, "to":var2,"amount":float(amount1.get()), "format": "json"}
    url = "https://api.getgeoapi.com/api/v2/currency/convert"
    response = requests.get(url, parameters)
    rates= response.json()['rates']
    rate_for_amount=rates[var2]['rate_for_amount']
    converted_amount.config(bg="#FFFFFF",fg="#000000")
    converted_amount.insert(0,str(rate_for_amount))
    
    global conversion_rate_label, conversion_rate
    conversion_rate_label = Label(app, text=" 1 {} = ".format(var1), bg="#FFFFFF", fg = '#000000', font=("Comic Sans MS", 10), justify="center")
    conversion_rate_label.grid(row=9, column=0, padx=20, pady=10)

    conversion_rate = Entry(app, width=25, font=("Comic Sans MS", 10), justify="center", bg = "#FFFFFF", fg = "#000000")
    conversion_rate.grid(row=9, column=1, padx=20, pady=10)
    conversion_rate.insert(0,str(rates[var2]['rate'])+" {}".format(var2))

def clear():
    amount.delete(0, END)
    converted_amount.delete(0, END)
    converted_amount.config(bg="#000000")
    conversion_rate_label.destroy()
    conversion_rate.destroy()   

if __name__ == "__main__":
    fetch_currency_list()
    app = Tk()
    app.geometry("900x500")
    app.title("Currency Converter")
    filename = ImageTk.PhotoImage(Image.open(os.path.join(BASE_DIR,'bg.jpg')))
    background_label = Label(app, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    amount1 = StringVar()
    create_widgets()
    app.mainloop()
