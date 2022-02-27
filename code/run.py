import os

from classes import Job, Shift


def run0():
    js = Shift()

    jobs = {}
    jobs[1] = Job(1, [1, 2, 3], [10, 8, 4])
    jobs[2] = Job(2, [2, 1, 4, 3], [8, 3, 5, 6])
    jobs[3] = Job(3, [1, 2, 4], [4, 7, 3])

    js.addJobs(jobs)
    js.criticalPath()
    js.makespan()
    js.choose_edge(compute_method=js.computeLmax)
    # js.choose_edge(compute_method=js.computeLmaxCarlier) # todo
    # js.output()
    # js.singleMachineLmax()


def run1():
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


def run2():
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


def read_file_to_jobs(filename):
    jobs = {}
    job_num, machine_num = 0, 0  # task num is equal to machine num
    with open(filename, "r") as f:
        job_num, machine_num = f.readline().split()
        job_num, machine_num = int(job_num), int(machine_num)
        for j in range(job_num):
            line_data = f.readline().split()
            task_seq = []
            process_time = []
            for m in range(machine_num):
                task_seq.append(int(line_data[2 * m]))
                process_time.append(int(line_data[2 * m + 1]))
            jobs[j] = Job(j, task_seq, process_time)
    return jobs


if __name__ == "__main__":
    dir_name = "../instances/"
    file_list = os.listdir(dir_name)
    prefix = "dmu"  # "dmu" or 'ta'
    num = range(16, 21)  # range(16, 21) or range(80)
    for p in file_list:
        temp = p.split("/")
        run_flag = False
        for n in num:
            if temp[-1] == prefix + str(n):
                run_flag = True
                break
        if run_flag:
            js = Shift()
            jobs = read_file_to_jobs(os.path.join(dir_name, p))
            js.addJobs(jobs)
            print(js.criticalPath())
            print(js.makespan())
            js.choose_edge()
