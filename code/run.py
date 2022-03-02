import os

from classes import Job, Shift


def read_file_to_jobs(filename):
    jobs = {}
    job_num, machine_num = 0, 0  # task num is equal to machine num
    with open(filename, "r") as f:
        one_line = f.readline().split()
        while one_line[0][0] == "#":
            one_line = f.readline().split()
        job_num, machine_num = one_line
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
    from config import *

    dir_name = "../instances/"
    dataset = dmu_dataset + abz_dataset
    for file_name in dataset:
        js = Shift()
        jobs = read_file_to_jobs(os.path.join(dir_name, file_name))
        js.addJobs(jobs)
        print(js.criticalPath())
        print(js.makespan())
        js.choose_edge()
