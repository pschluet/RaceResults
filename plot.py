import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import datetime as dt

def parse_dates(x):
    if isinstance(x, float):
        return dt.datetime.strptime('0:0', '%M:%S')
    return dt.datetime.strptime(x, '%M:%S') if len(x) <= 5 else dt.datetime.strptime(x, '%H:%M:%S')

def tick_formatter(x,pos):
    d = dt.timedelta(seconds=x)
    return str(d)

if __name__ == "__main__":
    time_cols = ['Swim', 'T1', 'Bike', 'T2', 'Run', 'Time']
    df = pd.read_csv('data.csv', parse_dates=time_cols, date_parser=parse_dates)
    for col in time_cols:
        df[col] = df[col].apply(lambda x: (x - dt.datetime.strptime('0', '%S')).total_seconds())

    formatter = matplotlib.ticker.FuncFormatter(tick_formatter)

    me = df[df['Name'] == 'Paul Schlueter']
    me = me.to_dict(orient='records')[0]

    plt.figure()
    plt.subplot(321)
    ax = sns.distplot(df['Swim'], kde_kws={"shade": True}, hist=False, color='green')
    plt.plot([me['Swim']] * 2, [0, ax.get_ylim()[1]], color='black')
    ax.xaxis.set_major_formatter(formatter)
    plt.subplot(322)
    ax = sns.distplot(df['T1'], kde_kws={"shade": True}, hist=False, color='blue')
    plt.plot([me['T1']] * 2, [0, ax.get_ylim()[1]], color='black')
    ax.xaxis.set_major_formatter(formatter)
    plt.subplot(323)
    ax = sns.distplot(df['Bike'], kde_kws={"shade": True}, hist=False, color='purple')
    plt.plot([me['Bike']] * 2, [0, ax.get_ylim()[1]], color='black')
    ax.xaxis.set_major_formatter(formatter)
    plt.subplot(324)
    ax = sns.distplot(df['T2'], kde_kws={"shade": True}, hist=False, color='red')
    plt.plot([me['T2']] * 2, [0, ax.get_ylim()[1]], color='black')
    ax.xaxis.set_major_formatter(formatter)
    plt.subplot(325)
    ax = sns.distplot(df['Run'], kde_kws={"shade": True}, hist=False, color='purple')
    plt.plot([me['Run']] * 2, [0, ax.get_ylim()[1]], color='black')
    ax.xaxis.set_major_formatter(formatter)
    plt.subplot(326)
    ax = sns.distplot(df['Time'], kde_kws={"shade": True}, hist=False, color='purple')
    plt.plot([me['Time']] * 2, [0, ax.get_ylim()[1]], color='black')
    plt.xlabel('Overall')
    ax.xaxis.set_major_formatter(formatter)

    plt.tight_layout()
    plt.show()