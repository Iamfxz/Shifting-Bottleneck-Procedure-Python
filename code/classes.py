import sys
from collections import defaultdict

import networkx as nx
from itertools import permutations

import numpy as np

import carlier


def argmin_kv(d):
    """
    A function that returns the schedule with minimal lateness and the associated lateness.
    """
    return min(d.items(), key=lambda x: x[1])


class Job(object):
    """
    A class that creates jobs.

    Parameters
    ----------
    r: list - A list with the task sequence
    p: list - Processing times for every task
    """

    def __init__(self, Id, route, processing):
        self.Id = Id
        self.r = route  # route
        self.p = processing  # processing times


# class Machine(object):
#     def __init__(self, Id, lateness):
#         self.Id = Id
#         self.l = lateness


class Jobshop(nx.DiGraph):
    """
    A class that creates a directed graph of a jobshop.

    We formulate the tasks of the jobshop as nodes in a directed graph, add the processing
    times of the tasks as attributes to the task nodes. A flag "dirty" was added so when
    some topological changes are carried the method "_update" is called first to update
    the makespan and critical path values. Once the update is finished, the updated
    makespan is returned.

    Methods
    -------
    handleJobRouting(jobs)
        Creates the edges of the graph that represents the given route and also adds
        the origin and finishing nodes.

    handleJobProcessingTimes(jobs)
        Creates the nodes of the graph that represent the tasks of a job.

    makeMachineSubgraphs()
        For every given machine creates a subgraph.

    addJobs(jobs)
        Handles the routine to add a jobs to the graph and the subgraphs.

    output()
        Prints the output.

    _forward

    _backward

    _computeCriticalPath

    _update

    Properties
    ----------
    makespan

    criticalPath

    """

    def __init__(self):
        super().__init__()
        # a dictionary to store machine's id of a subgraph with its jobs and routing
        self.machines = {}
        # start node
        self.add_node("U", p=0)
        # finish node
        self.add_node("V", p=0)
        # set dirty flag
        self._dirty = True
        # set initial makespan
        self._makespan = -1
        # define critical path # todo diff with criticalPath?
        self._criticalPath = None

    def add_node(self, *args, **kwargs):
        # adds dirty flag so the the _update subroutine is called
        self._dirty = True
        super().add_node(*args, **kwargs)

    def add_nodes_from(self, *args, **kwargs):
        # adds dirty flag so the the _update subroutine is called
        self._dirty = True
        super().add_nodes_from(*args, **kwargs)

    def add_edge(self, *args):
        # adds dirty flag so the the _update subroutine is called
        self._dirty = True
        super().add_edge(*args)

    def add_edges_from(self, *args, **kwargs):
        # adds dirty flag so the the _update subroutine is called
        self._dirty = True
        super().add_edges_from(*args, **kwargs)

    def remove_node(self, *args, **kwargs):
        # adds dirty flag so the the _update subroutine is called
        self._dirty = True
        super().remove_node(*args, **kwargs)

    def remove_nodes_from(self, *args, **kwargs):
        # adds dirty flag so the the _update subroutine is called
        self._dirty = True
        super().remove_nodes_from(*args, **kwargs)

    def remove_edge(self, *args):
        # adds dirty flag so the the _update subroutine is called
        self._dirty = True
        super().remove_edge(*args)

    def remove_edges_from(self, *args, **kwargs):
        # adds dirty flag so the the _update subroutine is called
        self._dirty = True
        super().remove_edges_from(*args, **kwargs)

    def handleJobRouting(self, jobs):
        """
            add the edges of tasks
        :param jobs:
        :return:
        """
        for j in jobs.values():
            # add start edge
            self.add_edge("U", (j.r[0], j.Id))
            # add the edges (processing order) routing the nodes (tasks)
            for m, n in zip(j.r[:-1], j.r[1:]):
                self.add_edge((m, j.Id), (n, j.Id))
            # add finishing edge
            self.add_edge((j.r[-1], j.Id), "V")

    def handleJobProcessingTimes(self, jobs):
        """
            add the attribute(process time) of tasks
        :param jobs:
        :return:
        """
        for j in jobs.values():
            # add every task and its corresponding processing time to the graph
            for m, p in zip(j.r, j.p):
                self.add_node((m, j.Id), p=p)

    def makeMachineSubgraph(self):
        # creates a set with machines' ids
        machine_ids = set(node[0] for node in self if node[0] not in ("U", "V"))
        # for every machine in the digraph creates a subgraph linked to the id with the corresponding nodes
        for m in machine_ids:
            self.machines[m] = self.subgraph(node for node in self if node[0] == m and node not in ("U", "V"))
            # self.machines[m].remove_nodes_from(["U", "V"])

    def addJobs(self, jobs):
        # every time a job is inserted: add the jobs' edges (routing), jobs' nodes (tasks),
        # and creates a subgraph for every machine
        self.handleJobRouting(jobs)  # edge: ((task_Id, job_Id), (task_Id, job_Id))
        self.handleJobProcessingTimes(jobs)  # node: ((task_Id, job_Id), p), p is the process time
        self.makeMachineSubgraph()  # subgraph of the Shift to represent the machine

    def output(self):
        # neatly outputs the jobshop digraph
        for m in sorted(self.machines):
            for j in sorted(self.machines[m]):
                print("{}: {}".format(j, self.nodes[j]["EF"]))

    def _forward(self):
        # Calculate the earliest occurrence time of arc according to forward topological ordering
        for n in nx.topological_sort(self):
            ES = max([self.nodes[j]["EF"] for j in self.predecessors(n)], default=0)
            # ES==>earliest start time, EF==>earliest finished time
            self.add_node(n, ES=ES, EF=ES + self.nodes[n]["p"])

    def _backward(self):
        # Calculate the latest occurrence time of arcs according to forward topological ordering
        for n in list(reversed(list(nx.topological_sort(self)))):
            LF = min([self.nodes[j]["LS"] for j in self.successors(n)], default=self._makespan)
            # LS==>latest start time LF==>latest finished time
            self.add_node(n, LS=LF - self.nodes[n]["p"], LF=LF)

    def _computeCriticalPath(self):
        # If earliest finished time == latest finished time,
        # the node is a critical activity on the critical path
        G = set()
        for n in self:
            if self.nodes[n]["EF"] == self.nodes[n]["LF"]:
                G.add(n)
        self._criticalPath = self.subgraph(G)

    def makespan(self):
        if self._dirty:
            self._update()
        return self._makespan

    def criticalPath(self):
        if self._dirty:
            self._update()
        return self._criticalPath

    def _update(self):
        self._forward()
        self._makespan = max(nx.get_node_attributes(self, "EF").values())
        self._backward()
        self._computeCriticalPath()
        self._dirty = False


class Shift(Jobshop):
    def __init__(self):
        super().__init__()
        self.scheduled_machine = defaultdict(bool)
        self.lateness_max = sys.maxsize
        self.node_sequence = None

    def output(self):
        print("makespan: ", self.makespan)
        for i in self.machines:
            print("Machine: " + str(i))
            s = "{0:<7s}".format("jobs:")
            for ij in sorted(self.machines[i]):
                if ij in ("U", "V"):
                    continue
                s += "{0:>5d}".format(ij[1])
            print(s)
            s = "{0:<7s}".format("p:")
            for ij in sorted(self.machines[i]):
                if ij in ("U", "V"):
                    continue
                s += "{0:>5d}".format(self.nodes[ij]["p"])
            print(s)
            s = "{0:<7s}".format("r:")
            for ij in sorted(self.machines[i]):
                if ij in ("U", "V"):
                    continue
                s += "{0:>5d}".format(self.nodes[ij]["ES"])
            print(s)
            s = "{0:<7s}".format("d:")
            for ij in sorted(self.machines[i]):
                if ij in ("U", "V"):
                    continue
                s += "{0:>5d}".format(self.nodes[ij]["LF"])
            print(s)
            print("\n")

    def choose_edge(self):
        while 1:
            self.computeLmax()
            sorted_machines = sorted(self.machines.items(), key=lambda x: x[1].lateness_max)
            if sorted_machines[-1][1].lateness_max == 0:
                finished_machine = set(self.scheduled_machine.keys())
                all_machine = set(self.machines.keys())
                remain_machine = all_machine - finished_machine
                for m in remain_machine:
                    seq = self.machines[m].node_sequence
                    edges_seq = list(zip(seq[:-1], seq[1:]))
                    self.add_edges_from(edges_seq)
                    print(f"Choose machine: {m}, Choose seq: {seq}")
                self.criticalPath()
                self.makespan()
                print("completed")
                return True
            # 可能需要分支搜索相同的解
            machine = sorted_machines[-1][0]
            seq = sorted_machines[-1][1].node_sequence
            edges_seq = list(zip(seq[:-1], seq[1:]))
            self.add_edges_from(edges_seq)
            self.scheduled_machine[machine] = True
            print(self.criticalPath())
            print(self.makespan())
            print(f"Choose machine: {machine}, Choose seq: {seq}")

    def computeLmax(self):
        machine_lateness_seq = dict()
        for m in self.machines:
            lateness = {}
            # todo 1 rj Lmax
            for seq in permutations(self.machines[m]):
                release = [self.nodes[j]["ES"] for j in seq]
                due = [self.nodes[j]["LF"] for j in seq]
                finish = [0] * len(release)
                for i, j in enumerate(seq):
                    finish[i] = max(finish[i - 1], release[i]) + self.nodes[j]["p"]
                late = max([f - d for d, f in zip(due, finish)])
                lateness[seq] = late
            s, l = argmin_kv(lateness)
            print("Machine: {}, lateness: {}, optimal seq: {}".format(m, l, s))
            # machine_lateness_seq[m] = (l, s)
            self.machines[m].lateness_max = l
            self.machines[m].node_sequence = s
        return machine_lateness_seq

    def computeLmaxCarlier(self):
        machine_lateness_seq = dict()
        for m in self.machines:
            tasks = []
            nodes = []
            for j in self.machines[m]:
                tasks.append(
                    [
                        self.nodes[j]["ES"],
                        self.nodes[j]["p"],
                        self.nodes[j]["LF"],
                    ]
                )
                nodes.append(j)
            # tasks = np.array(tasks)
            carlier.UB = 9999999
            LB, UB, seq = carlier.Carlier_Elim(tasks)
            node_seq = [nodes[j] for j in seq]
            due = [self.nodes[j]["LF"] for j in node_seq]
            finish = [0] * len(node_seq)
            for i, j in enumerate(node_seq):
                finish[i] = max(finish[i - 1], self.nodes[j]["ES"]) + self.nodes[j]["p"]
            late = max([f - d for d, f in zip(due, finish)])
            if late > 0 or not self.scheduled_machine[m]:
                print("Machine: {}, lateness: {}, optimal seq: {}".format(m, late, node_seq))
                machine_lateness_seq[m] = (late, node_seq)
        return machine_lateness_seq
