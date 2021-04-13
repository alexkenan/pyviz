"""
Use Matplotlib and Tkinter together
"""
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
import pandas as pd
#import matplotlib
#matplotlib.use("TkAgg")


def _quit(main: tk.Tk):
    main.quit()
    main.destroy()


def tsa(path: str) -> pd.DataFrame:
    """
    Load the TSA Passenger Throughput data
    :param path: str of path to TSA spreadsheet
    :return: pd.DataFrame of the TSA Passenger throughput results
    """
    dataframe = pd.read_csv(path,
                            names=['Date', '2020', '2019'],
                            header=0, parse_dates=['Date'])
    dataframe['yoy'] = (dataframe['2020'] / dataframe['2019']) * 100
    return dataframe


def plot_new_canvas(figure: plt.figure, main: tk.Tk) -> None:
    """
    Plot the new figure on the Tk canvas
    :param figure: fig object that is the plot figure
    :param main: tk.Tk() instance
    :return: None
    """
    figure.set_size_inches((9, 6))
    canvas = FigureCanvasTkAgg(figure, master=main)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=0, columnspan=2, rowspan=8)


def plot_choice(num: int, plot: plt, df1: pd.DataFrame) -> None:
    """
    Function to re-draw the canvas
    :param num: int of the RadioButton selection
    :param plot: plt Matplotlib.pyplot instance
    :param df1: pd.DataFrame of the TSA data
    :return: None
    """
    plot.clf()
    blue = "#327ff6"
    gray = "#bdb8b6"
    if num == 1:
        # Daily raw pax numbers
        fig, axis = plt.subplots()
        axis.plot(df1['Date'], df1['2020'], color=blue, linestyle='-', label="2020")
        axis.plot(df1['Date'], df1['2019'], color=gray, linestyle='-', label="2019")
        plot.legend()
        plot.xlabel('Date')
        plot.ylabel('Passengers')
        plot.title('TSA Passenger Daily Throughput 2019 and 2020')
        axis.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))

        plot_new_canvas(fig, root)

    elif num == 2:
        # Weekly raw pax numbers
        weekly_data = df1.resample('W-Mon', label='right', closed='right',
                                   on='Date').sum().reset_index().sort_values(by='Date')
        fig, axis = plt.subplots()
        axis.plot(weekly_data['Date'], weekly_data['2020'], color=blue, linestyle='-',
                  label="2020")
        axis.plot(weekly_data['Date'], weekly_data['2019'], color=gray, linestyle='-',
                  label="2019")
        axis.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
        plot.xlabel('Date')
        plot.ylabel('Passengers')
        plot.legend()
        plot.ylim(0, 20E6)
        plot.title('TSA Passenger Weekly Throughput 2019 and 2020')

        plot_new_canvas(fig, root)

    elif num == 3:
        # Daily YoY percentage
        fig, axis = plt.subplots()
        axis.plot(df1['Date'], df1['yoy'], color=blue, linestyle='-', label="2020")
        plot.legend()
        plot.xlabel('Date')
        plot.ylabel('Passenger Load Factor (%)')
        plot.title('TSA Passenger Daily Throughput in 2020 as a Percentage of 2019')

        plot_new_canvas(fig, root)

    elif num == 4:
        # Weekly YoY percentage
        weekly_data = df1.resample('W-Mon', label='right', closed='right',
                                   on='Date').sum().reset_index().sort_values(by='Date')
        weekly_data['yoy'] = (weekly_data['2020']/weekly_data['2019'])*100
        fig, axis = plt.subplots()
        axis.plot(weekly_data['Date'], weekly_data['yoy'], color=blue, linestyle='-',
                  label="2020")
        plot.xlabel('Date')
        plot.ylabel('Passenger Load Factor (%)')
        plot.legend()
        plot.title('TSA Passenger Daily Throughput in 2020 as a Percentage of 2019')

        plot_new_canvas(fig, root)


root = tk.Tk()
root.geometry("1100x750")
root.wm_title("TSA Passenger Throughput")

selection = tk.IntVar()
selection.set(1)
tk.Radiobutton(root, text="Daily", variable=selection, value=1,
                                 command=lambda: plot_choice(selection.get(), plt, df)).grid(row=1, column=3)
tk.Radiobutton(root, text="Weekly", variable=selection, value=2,
                                 command=lambda: plot_choice(selection.get(), plt, df)).grid(row=2, column=3)
tk.Radiobutton(root, text="Daily % YoY", variable=selection, value=3,
                                 command=lambda: plot_choice(selection.get(), plt, df)).grid(row=3, column=3)
tk.Radiobutton(root, text="Weekly % YoY", variable=selection, value=4,
                                 command=lambda: plot_choice(selection.get(), plt, df)).grid(row=4, column=3)


button = tk.Button(master=root, text="Quit", command=lambda: _quit(root))
button.grid(row=5, column=3)


df = tsa('https://raw.githubusercontent.com/alexkenan/pyviz/main/datasets/tsa_pax.csv')
plot_choice(1, plt, df)

tk.mainloop()
