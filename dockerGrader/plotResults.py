import argparse

import pandas as pd
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, statsfile):
        self.stats_file = statsfile

    def show(self):
        data = pd.read_pickle(self.stats_file)
        columns = list(data)
        grades = data.sum(axis=1)/len(columns)*100
        plt.subplot(1, 2, 1)
        grades.plot.hist(bins=10)
        plt.title('Distribution of grades')
        plt.subplot(1, 2, 2)
        plt.bar(range(len(columns)), data.mean(axis=0))
        plt.title('Distribution of tests')
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot results of Autograder')
    parser.add_argument('-sf', '--statsfile', type=str, default='stats4.pkl',
                        help='file to read in dataframe from', required=False)
    args = parser.parse_args()
    p = Plotter(**vars(args))
    p.show()
