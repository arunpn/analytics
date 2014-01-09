""" This reads in a csv file of ProblemLog data, e.g.:

[(u'practice', False)]
[]
[(u'mastery.review', False), (u'mastery.mastery', True)]
...

where each column is a list of tuples (task_type, correct) for ProblemLogs
ordered by time_done. This format is subject to change.

We compute a few statistics on the distribution of analytics cards (among
other things).
"""

import ast
import sys
import time

import matplotlib.pyplot as plt
import numpy as np


def read_data(filename=None):
    if filename is None:
        f = sys.stdin
    else:
        f = open(filename, 'r')

    data = []
    for row in f:
        # skip empty rows '[]\n'
        if len(row) <= 3:
            continue
        problems = ast.literal_eval(row)
        data.append(problems)

    return data


def graph_efficiency(n, data):
    correct_by_type = {}
    total_by_type = {}
    for problems in data:
        for i in range(min(n, len(problems))):
            # labels don't like unicode
            task_type = str(problems[i][0])
            if task_type not in correct_by_type:
                correct_by_type[task_type] = np.zeros(n)
                total_by_type[task_type] = np.zeros(n)
            if problems[i][1]:
                correct_by_type[task_type][i] += 1
            total_by_type[task_type][i] += 1

    plt.title('Efficiency Curve: By Task Type')
    plt.xlabel('Problem Number')
    plt.ylabel('Percent Correct')

    for task_type in sorted(correct_by_type):
        if task_type == 'None':
            continue
        correct = correct_by_type[task_type]
        total = total_by_type[task_type]
        eff = np.zeros(n)
        for i in range(n):
            if total[i] > 0:
                eff[i] = 1.0 * correct[i] / total[i]
            else:
                eff[i] = 0.0
        plt.plot(eff, label=task_type)
    plt.legend(loc='lower center', ncol=2)
    plt.show()


def graph_task_type(n, data):
    map_by_type = {}
    for problems in data:
        for i in range(min(n, len(problems))):
            # labels don't like unicode
            task_type = str(problems[i][0])
            if task_type not in map_by_type:
                map_by_type[task_type] = []
            map_by_type[task_type].append(i)

    x = []
    label = []
    for task_type in sorted(map_by_type):
        x.append(map_by_type[task_type])
        label.append(task_type)

    plt.title('Engagement Curve: By Task Type')
    plt.xlabel('Problem Number')
    plt.ylabel('Number of Users (doing at least x problems)')
    plt.hist(x, n, normed=0, histtype='bar', stacked=True, label=label)
    plt.legend()
    plt.show()


def graph_engagement(n, data):
    eng = np.zeros(n)
    for l in data:
        eng[:len(l)] += 1
    plt.title('Engagement Curve')
    plt.xlabel('Problem Number')
    plt.ylabel('Number of Users (doing at least x problems)')
    plt.plot(eng)
    plt.show()


def main():
    start = time.time()
    n = 100
    data = read_data()
    print 'Done reading input, elapsed: %f\n' % (time.time() - start)

    graph_efficiency(n, data)
    print 'Done graphing efficiency, elapsed: %f\n' % (time.time() - start)

    """
    graph_task_type(n, data)
    print 'Done graphing task type, elapsed: %f\n' % (time.time() - start)

    graph_engagement(n, data)
    print 'Done graphing engagement, elapsed: %f\n' % (time.time() - start)
    """

if __name__ == '__main__':
    main()