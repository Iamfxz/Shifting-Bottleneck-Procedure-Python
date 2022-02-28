"""
@project:RL-Job-Shop-Scheduling
@author: fxz
@contact: fxz.fzu@gmail.com
@file:tests.py
@version: alpha
@time:2022/2/27 23:56
@desc:
    创建者请写入文件说明
"""
from classes import Shift, Job


def test0():
    js = Shift()

    jobs = {}
    jobs[1] = Job(1, [1, 2, 3], [10, 8, 4])
    jobs[2] = Job(2, [2, 1, 4, 3], [8, 3, 5, 6])
    jobs[3] = Job(3, [1, 2, 4], [4, 7, 3])

    js.addJobs(jobs)
    js.criticalPath()
    js.makespan()
    js.choose_edge()
    # js.choose_edge(compute_method=js.computeLmaxCarlier) # todo
    # js.output()
    # js.singleMachineLmax()


def test1():
    js = Shift()

    jobs = {}
    jobs[1] = Job(1, [1, 2, 3], [10, 8, 4])
    jobs[2] = Job(2, [2, 1, 4, 3], [8, 3, 5, 6])
    jobs[3] = Job(3, [1, 2, 4], [4, 7, 3])

    js.addJobs(jobs)
    js.criticalPath()
    js.makespan()
    js.output()

    js.computeLmax()
    # choose for machine 1
    js.add_edges_from([((1, 1), (1, 2)), ((1, 2), (1, 3))])

    js.criticalPath()
    js.makespan()

    js.output()

    js.computeLmax()
    # choose for machine 2
    js.add_edges_from([((2, 2), (2, 1)), ((2, 1), (2, 3))])

    js.output()

    js.computeLmax()
    # choose for machine 3 and machine 4
    js.add_edges_from([((3, 1), (3, 2))])
    js.add_edges_from([((4, 2), (4, 3))])

    js.output()
    js.computeLmax()


def test2():
    js = Shift()
    jobs = {}
    jobs[1] = Job(1, [1, 2], [3, 4])
    jobs[2] = Job(2, [1, 2], [6, 5])
    jobs[3] = Job(3, [1, 2], [4, 5])
    jobs[4] = Job(4, [1, 2], [3, 2])
    jobs[11] = Job(11, [1, 2], [12, 2])

    js.addJobs(jobs)
    js.criticalPath()
    js.makespan()
    js.output()
    print(sum(js.nodes[ij]["p"] for ij in js.machines[1]))
    print(sum(js.nodes[ij]["p"] for ij in js.machines[2]))

    seq = (3, 2, 1, 11, 4)
    for j1, j2 in zip(seq[:-1], seq[1:]):
        js.add_edge((1, j1), (1, j2))

    js.criticalPath()
    js.makespan()
    js.output()
