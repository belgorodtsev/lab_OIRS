"""
Лабораторная работа N 1
С помощью python обработать данные из файла и нарисовать два графика:
тенденция по годам по всем странам и тенденция по топ-5 странам по годам.
Вариант 2. Выбросы углекислого газа
"""

import pandas
import matplotlib.pyplot as plt


co2e_kt = 'CO2E.KT.csv'
co2e_pc = 'CO2E.PC.csv'


def analysis(filename: str, type_name: str):
    cols = pandas.read_csv(filename, header=2).columns
    cols = cols[cols.str.contains(r'Country Name|\d{4}', regex=True)].tolist()
    df = pandas.read_csv(filename, header=2, usecols=cols, error_bad_lines=False)

    df.dropna(axis='columns', how='all', inplace=True)
    df.dropna(axis='index', thresh=len(df.columns), inplace=True)

    _, ax = plt.subplots(1, 2, figsize=(12, 4))
    mean_val = df.mean(axis='index', numeric_only=True)
    mean_val.plot(ax=ax[0], style='b.-', alpha=0.6, grid=True, title=type_name)

    top_5 = df.loc[df.sum(axis='columns').sort_values(ascending=False)[:5].index].transpose()
    top_5[1:].plot(ax=ax[1], grid=True, title='Top 5 counties from 1960 to 2020')
    ax[1].legend(top_5.iloc[0])

    plt.show()


if __name__ == "__main__":
    analysis(co2e_pc, 'World CO2 emissions (metric tons per capita)')
    analysis(co2e_kt, 'World CO2 emissions (kt)')
