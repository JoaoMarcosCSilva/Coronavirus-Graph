import argparse

parser = argparse.ArgumentParser(
    description="Plots a graph of the current coronavirus spread in the given countries. The data is pulled from the website https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases.")

parser.add_argument('-b','--begin', type = int, metavar = 'N', help = 'Begin plotting from day of case N', default = 100)
parser.add_argument('countries', nargs='+', help = 'List of countries whose information is to be plotted')
parser.add_argument('-U', help = 'Updates data before plotting', action = 'store_true')

parser.add_argument('-l', '--log', help='Plots on a logarithmic scale', action='store_true')

parser.add_argument('--no-cases', help="Disables plotting of the cases graphs", action='store_false')
parser.add_argument('--no-deaths', help="Disables plotting of the deaths graphs", action='store_false')
parser.add_argument('--no-recoveries', help="Disables plotting of the recoveries' graphs", action='store_false')
parser.add_argument('--no-active', help="Disables plotting of the active cases' graphs", action='store_false')

parser.add_argument('--no-daily', help='Disables plotting of the daily graphs', action='store_false')
parser.add_argument('--no-cumulative', help='Disables plotting of the cumulative graphs', action='store_false')

cmd = parser.parse_args()

import visualization
import data

if cmd.U:
    data.download_data()


p,c = data.process_data(*data.load_data())

row_mask = [cmd.no_daily, cmd.no_cumulative]
col_mask = [cmd.no_cases, cmd.no_deaths, cmd.no_recoveries, cmd.no_active]

visualization.main_plot_countries(c, cmd.countries, cmd.begin, cmd.log, row_mask, col_mask)