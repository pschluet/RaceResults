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
    d = dt.timedelta(seconds=float(x))
    return str(d)

if __name__ == "__main__":
    time_cols = ['Swim', 'T1', 'Bike', 'T2', 'Run', 'Time']
    df = pd.read_csv('data.csv', parse_dates=time_cols, date_parser=parse_dates)
    for col in time_cols:
        df[col] = df[col].apply(lambda x: (x - dt.datetime.strptime('0', '%S')).total_seconds())

    sns.set_style('darkgrid')

    formatter = matplotlib.ticker.FuncFormatter(tick_formatter)

    me = df[df['Name'] == 'Paul Schlueter']
    me = me.to_dict(orient='records')[0]

    for cdf in [False, True]:
        fig = plt.figure(figsize=[12,9])
        plt.subplot(321)
        ax = sns.distplot(df['Swim'], kde_kws={"shade": True, "cumulative":cdf}, hist=False, color='green')
        plt.plot([me['Swim']] * 2, [0, ax.get_ylim()[1]], color='black')
        ax.xaxis.set_major_formatter(formatter)
        plt.subplot(322)
        ax = sns.distplot(df['T1'], kde_kws={"shade": True, "cumulative":cdf}, hist=False, color='blue')
        plt.plot([me['T1']] * 2, [0, ax.get_ylim()[1]], color='black')
        ax.xaxis.set_major_formatter(formatter)
        plt.subplot(323)
        ax = sns.distplot(df['Bike'], kde_kws={"shade": True, "cumulative":cdf}, hist=False, color='purple')
        plt.plot([me['Bike']] * 2, [0, ax.get_ylim()[1]], color='black')
        ax.xaxis.set_major_formatter(formatter)
        plt.subplot(324)
        ax = sns.distplot(df['T2'], kde_kws={"shade": True, "cumulative":cdf}, hist=False, color='red')
        plt.plot([me['T2']] * 2, [0, ax.get_ylim()[1]], color='black')
        ax.xaxis.set_major_formatter(formatter)
        plt.subplot(325)
        ax = sns.distplot(df['Run'], kde_kws={"shade": True, "cumulative":cdf}, hist=False, color='orange')
        plt.plot([me['Run']] * 2, [0, ax.get_ylim()[1]], color='black')
        ax.xaxis.set_major_formatter(formatter)
        plt.subplot(326)
        ax = sns.distplot(df['Time'], kde_kws={"shade": True, "cumulative":cdf}, hist=False, color='cyan')
        plt.plot([me['Time']] * 2, [0, ax.get_ylim()[1]], color='black')
        plt.xlabel('Overall')
        ax.xaxis.set_major_formatter(formatter)

        plt.tight_layout()
        txt = 'cdf' if cdf else 'pdf'
        plt.savefig('stages_' + txt + '.svg')

    plt.figure(figsize=[10,10])
    ax = sns.boxplot(x='Time', y='Div', data=df)
    sns.swarmplot(x='Time', y='Div', data=df, size=2, color=".3", linewidth=0)
    plt.title('Total Time by Division')
    plt.xlabel('Total Time')
    ax.xaxis.set_major_formatter(formatter)
    plt.savefig('time_by_div.svg')

    df['Sex'] = df['Div'].map(lambda x: 'F' in x or 'ATH' in x)

    plt.figure(figsize=[10,6])
    ax = sns.distplot(df.loc[df['Sex'] == 1, 'Time'], kde_kws={"shade": True}, hist=False)
    ax = sns.distplot(df.loc[df['Sex'] == 0, 'Time'], kde_kws={"shade": True}, hist=False)
    plt.legend(['Women', 'Men'])
    plt.plot([me['Time']] * 2, [0, ax.get_ylim()[1]], color='black')
    plt.title('Total Time PDFs')
    plt.xlabel('Total Time')
    ax.xaxis.set_major_formatter(formatter)
    plt.savefig('sex_pdfs.svg')

    plt.figure(figsize=[10,10])
    ax = sns.barplot(x='counts', y='Div', data=df.groupby(['Div']).size().reset_index(name='counts').sort_values('counts', ascending=False))
    plt.xlabel('Number of Competitors')
    plt.ylabel('Division')
    plt.title('Number of Competitors by Division')
    plt.savefig('num_racers.svg')

    plt.show()