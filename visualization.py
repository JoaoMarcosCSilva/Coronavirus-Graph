import matplotlib.pyplot as plt
import numpy as np

def apply_smooth(array, days = 4, smoothing = 2):
    for i in range(days, len(array)):
        array[i] = array[i]*(smoothing)/(1+days)
        array[i] += array[i-1]*(1 - (smoothing)/(1+days))
    return array

def apply_window(array, days = 7):
    return np.convolve(array, np.ones(days), 'valid') / days 

def plot(Countries, title = '', rows = 1, cols = 1, pos = 1, log = False, fill_alpha = 0):
    plt.subplot(rows, cols, pos)
    plt.subplots_adjust(wspace = 0.5, hspace = 0.3)
    plt.title(title, fontsize = 6)
    
    if fill_alpha != 0:
        for label in Countries:
            plt.bar(range(len(Countries[label])), Countries[label], width = 1, alpha = fill_alpha)

    for label in Countries:
        plt.plot(Countries[label], label = label)
    
    #plt.legend()
    if log:
        plt.yscale('log')

    plt.grid()
    plt.gca().axhline(y=0, color='k')
    plt.gca().axvline(x=0, color='k')

# Smoothing type can be window or exponential
def plot_minimum(Countries, minimum_dict, minimum_value, title = '', rows = 1, cols = 1, pos = 1, log = False, smooth = {'days' : 0, 'type' : 'window'}, fill_alpha = 0):
    C = Countries.copy()
    for c in C:
        if smooth['days'] != 0:
            if smooth['type'] == 'exponential':
                C[c] = apply_smooth(np.array([v for v,i in zip (Countries[c], minimum_dict[c]) if i > minimum_value]), smooth['days'], smooth['smoothness'])
            else:
                C[c] = apply_window(np.array([v for v,i in zip (Countries[c], minimum_dict[c]) if i > minimum_value]), smooth['days'])
        else:    
            C[c] = np.array([v for v,i in zip (Countries[c], minimum_dict[c]) if i > minimum_value])
    
    plot(C, title, rows, cols, pos, log, fill_alpha)

def main_plot(Countries, minimum_value = 100, minimum_title = 'case', log = False, row_mask = [True, True], col_mask = [True, True, True, True], smooth = {'days' : 0}, fill_alpha = 0):
    
    minimum_dict = {c:Countries[c].cases for c in Countries}

    nrows = row_mask[0] + row_mask[1]
    ncols = col_mask[0] + col_mask[1] + col_mask[2] + col_mask[3]

    count = 1

    if row_mask[0]:
        if col_mask[0]:
            plot_minimum({c:Countries[c].daily_cases for c in Countries}, minimum_dict, minimum_value, 'Daily cases from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log, smooth, fill_alpha)
            count += 1
        if col_mask[1]:
            plot_minimum({c:Countries[c].daily_deaths for c in Countries}, minimum_dict, minimum_value, 'Daily deaths from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log, smooth, fill_alpha)
            count += 1
        if col_mask[2]:
            plot_minimum({c:Countries[c].daily_recover for c in Countries}, minimum_dict, minimum_value, 'Daily recoveries from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log, smooth, fill_alpha)
            count += 1
        if col_mask[3]:
            plot_minimum({c:Countries[c].daily_active for c in Countries}, minimum_dict, minimum_value, 'Daily active cases from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log, smooth, fill_alpha)
            count += 1

    if row_mask[1]:
        if col_mask[0]:
            plot_minimum({c:Countries[c].cases for c in Countries}, minimum_dict, minimum_value, 'Cumulative cases from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log, smooth)
            count += 1
        if col_mask[1]:
            plot_minimum({c:Countries[c].deaths for c in Countries}, minimum_dict, minimum_value, 'Cumulative deaths from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log, smooth)
            count += 1
        if col_mask[2]:
            plot_minimum({c:Countries[c].recover for c in Countries}, minimum_dict, minimum_value, 'Cumulative recoveries from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log, smooth)
            count += 1
        if col_mask[3]:
            plot_minimum({c:Countries[c].active for c in Countries}, minimum_dict, minimum_value, 'Cumulative active cases from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log, smooth)
            count += 1
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.figlegend(handles, labels, loc='upper center')

    plt.show()
    
def main_plot_countries(Countries, names, minimum_value = 100, log = False, row_mask = [], col_mask = [], minimum_title = 'case', smooth = {'days' : 0}, fill_alpha = 0):
     main_plot({i:Countries[i] for i in names}, minimum_value, minimum_title, log, row_mask, col_mask, smooth, fill_alpha)
