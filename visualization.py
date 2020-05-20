import matplotlib.pyplot as plt
import numpy as np

def plot(Countries, title = '', rows = 1, cols = 1, pos = 1, log = False):
    plt.subplot(rows, cols, pos)
    plt.subplots_adjust(wspace = 0.5, hspace = 0.3)
    plt.title(title, fontsize = 6)
    for label in Countries:
        plt.plot(Countries[label], label = label)
    
    plt.legend()
    if log:
        plt.yscale('log')

def plot_minimum(Countries, minimum_dict, minimum_value, title = '', rows = 1, cols = 1, pos = 1, log = False):
    C = Countries.copy()
    for c in C:
        C[c] = np.array([v for v,i in zip (Countries[c], minimum_dict[c]) if i > minimum_value])
    
    plot(C, title, rows, cols, pos, log)

def main_plot(Countries, minimum_value = 100, minimum_title = 'case', log = False, row_mask = [True, True], col_mask = [True, True, True, True]):
    
    minimum_dict = {c:Countries[c].cases for c in Countries}

    nrows = row_mask[0] + row_mask[1]
    ncols = col_mask[0] + col_mask[1] + col_mask[2] + col_mask[3]

    count = 1

    if row_mask[0]:
        if col_mask[0]:
            plot_minimum({c:Countries[c].daily_cases for c in Countries}, minimum_dict, minimum_value, 'Daily cases from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log)
            count += 1
        if col_mask[1]:
            plot_minimum({c:Countries[c].daily_deaths for c in Countries}, minimum_dict, minimum_value, 'Daily deaths from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log)
            count += 1
        if col_mask[2]:
            plot_minimum({c:Countries[c].daily_recover for c in Countries}, minimum_dict, minimum_value, 'Daily recoveries from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log)
            count += 1
        if col_mask[3]:
            plot_minimum({c:Countries[c].daily_active for c in Countries}, minimum_dict, minimum_value, 'Daily active cases from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log)
            count += 1

    if row_mask[1]:
        if col_mask[0]:
            plot_minimum({c:Countries[c].cases for c in Countries}, minimum_dict, minimum_value, 'Cumulative cases from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log)
            count += 1
        if col_mask[1]:
            plot_minimum({c:Countries[c].deaths for c in Countries}, minimum_dict, minimum_value, 'Cumulative deaths from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log)
            count += 1
        if col_mask[2]:
            plot_minimum({c:Countries[c].recover for c in Countries}, minimum_dict, minimum_value, 'Cumulative recoveries from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log)
            count += 1
        if col_mask[3]:
            plot_minimum({c:Countries[c].active for c in Countries}, minimum_dict, minimum_value, 'Cumulative active cases from day of %s %d' % (minimum_title, minimum_value), nrows, ncols, count, log)
            count += 1
            
    plt.show()
    
def main_plot_countries(Countries, names, minimum_value = 100, log = False, row_mask = [], col_mask = [], minimum_title = 'case'):
     main_plot({i:Countries[i] for i in names}, minimum_value, minimum_title, log, row_mask, col_mask)
