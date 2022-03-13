from classes import Job, Jobshop

from pulp import *

jobs = {}
jobs[1] = Job(1, [1, 2, 3], [10, 8, 4])
jobs[2] = Job(2, [2, 1, 4, 3], [8, 3, 5, 6])
jobs[3] = Job(3, [1, 2, 4], [4, 7, 3])


def LP(jobs):
    """
    A function that computes the linear programming optimization procedure for the Jobshop Scheduling Problem.
    This is the disjunctive programming formulation.
    Formulation from Pinedo 2009.
    """
    js = Jobshop()
    js.addJobs(jobs)

    prob = LpProblem("Job shop", LpMinimize)

    H = sum(js.nodes[j]["p"] for j in js)
    T = range(H + 1)

    x = LpVariable.dicts("x", [(ij, t) for ij in js for t in T], 0, 1, cat=LpInteger)

    ef = LpVariable.dicts("EF", [ij for ij in js])
    for ij in js:
        prob += ef[ij] == lpSum([t * x[(ij, t)] for t in T])

    prob += ef["V"]

    for ij in js:
        prob += lpSum([x[(ij, t)] for t in T]) == 1

    for ij in js:
        prob += ef[ij] >= js.nodes[ij]["p"]

    for ij in js:
        for k in js.predecessors(ij):
            prob += ef[ij] >= ef[k] + js.nodes[ij]["p"]

    p = lambda ij, t: lpSum([x[(ij, u)] for u in range(t, t + js.nodes[ij]["p"])])

    for i in js.machines:
        for t in T:
            prob += lpSum([p(ij, t) for ij in js.machines[i] if t <= H - js.nodes[ij]["p"] + 1]) <= 1

    prob.solve(GUROBI())
    # prob.solve()

    print("status", LpStatus[prob.status])
    print("objective", value(prob.objective))

    for j in js:
        for t in T:
            if x[j, t].varValue > 0:
                js.add_node(j, EF=t)

    js.output()


if __name__ == "__main__":
    LP(jobs)
