# credit to https://jakevdp.github.io/PythonDataScienceHandbook/04.09-text-and-annotation.html
import configparser
from itertools import chain, cycle
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
import os
import pandas as pd
import sys


def read_config(filename='timeline.ini'):
    '''Read config from timeline.ini file'''
    config = configparser.ConfigParser()
    try:
        filename = os.path.join(os.getcwd(), filename)
        config.read(filename)
    except FileNotFoundError:
        print('Config file not found: ', config['files']['input'])
        sys.exit()
    return config

def read_data(config):
    '''Read data from csv file into dataframe, sorted by date'''
    # pylint: disable=E1101
    try:
        filename = os.path.join(os.getcwd(), config['files']['input'])
        data = pd.read_csv(filename)
    except FileNotFoundError:
        print('Data input file not found: ', config['files']['input'])
        sys.exit()
    data.date = pd.to_datetime(data.date)
    data = data.sort_values(by='date')
    return data

def set_up_figure(config):
    '''Set up the figure, the axis, and the plot element we want to animate'''
    fig = plt.figure(figsize=(config['figure'].getint('size_hor'),
                              config['figure'].getint('size_ver')))
    y_s, m_s, d_s = map(int, config['dates']['start'].split('-'))
    fig_start = pd.datetime(y_s, m_s, d_s)
    y_e, m_e, d_e = map(int, config['dates']['end'].split('-'))
    fig_end = pd.datetime(y_e, m_e, d_e)
    fig.suptitle(config['figure']['title'],
                 fontsize=config['figure'].getint('title_font_size'))
    ax = plt.axes(xlim=(fig_start, fig_end), ylim=(-200, 200))
    ax.grid(False)
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_color('none')
    plt.xticks(rotation=config['figure'].getint('tick_rotation'))

    delta = (fig_end - fig_start).days
    tick_interval, tick_type = config['figure']['tick_interval'].split(' ')
    tick_interval = int(tick_interval)
    if tick_type == 'years':
        ax.xaxis.set_ticks([fig_start + pd.DateOffset(years=x)
                            for x in range(0, int(delta/365)+1, tick_interval)])
        ax.xaxis.set_major_formatter(DateFormatter('%Y'))
    if tick_type == 'months':
        ax.xaxis.set_ticks([fig_start + pd.DateOffset(months=x)
                            for x in range(0, int(delta/30)+1, tick_interval)])
        ax.xaxis.set_major_formatter(DateFormatter('%Y - %m'))
    if tick_type == 'days':
        ax.xaxis.set_ticks([fig_start + pd.DateOffset(days=x)
                            for x in range(0, int(delta/1)+1, tick_interval)])
        ax.xaxis.set_major_formatter(DateFormatter('%Y - %m - %d'))

    fig.axes[0].get_yaxis().set_visible(False)
    fig.axes[0].get_xaxis().set_visible(True)

    return fig, ax

def add_annotations(config, data, ax):
    '''Add annotations to figure'''
    stack_size = config['figure'].getint('stack_size')
    stack_interval = int(140 / (stack_size-1))
    height_iterator = cycle([x for x in chain(
        range(60, 200, stack_interval),
        range(60 + int(stack_interval/2), 200, stack_interval))])

    colors_above = config['figure']['colors_above'].split(',')
    colors_below = config['figure']['colors_below'].split(',')

    for _, row in data.iterrows():
        flip_side = True if row.color in colors_below else False
        flip = -1 if flip_side else 1

        height = next(height_iterator)
        # conn_style = "angle3,angleA=-15,angleB=90"
        # conn_style = "angle,angleA=0,angleB=80,rad=20"
        if row.type == 'right':
            row.type = 'left'
            if flip_side:
                conn_style = "angle,angleA=0,angleB=100,rad=20"
            else:
                conn_style = "angle,angleA=180,angleB=80,rad=20"
        elif row.type == 'left':
            row.type = 'right'
            if flip_side:
                conn_style = "angle,angleA=0,angleB=80,rad=20"
            else:
                conn_style = "angle,angleA=0,angleB=100,rad=20"
        else:
            conn_style = "angle,angleA=0,angleB=100,rad=20"
        offset_factor = -1 if row.type == 'right' else 1

        ax.annotate(row.text,
                    xy=(row.date, 0),
                    xycoords='data',
                    xytext=(offset_factor*25, flip * height),
                    textcoords='offset points',
                    arrowprops=dict(arrowstyle=row.style,
                                    connectionstyle=conn_style,
                                    color=row.color),
                    color=row.color,
                    ha=row.type)

    return ax,

def save_figure(config, fig):
    '''Save figure locally'''
    filename = os.path.join(os.getcwd(), config['files']['output'])
    fig.savefig(filename)
    return

def show_figure():
    '''Show plot to user'''
    plt.show()
    return

def main():
    '''Create a timeline chart with annotations from input data'''
    config = read_config()
    data = read_data(config)
    figure, axes = set_up_figure(config)
    axes = add_annotations(config, data, axes)
    save_figure(config, figure)
    show_figure()

if __name__ == '__main__':
    main()
