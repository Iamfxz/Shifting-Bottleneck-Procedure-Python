import os

from ray import method

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

    dir_name = "instances/"
    all_dataset = (
        abz_dataset + dmu_dataset + ft_dataset + la_dataset + orb_dataset + swv_dataset + ta_dataset[:50] + yn_dataset
    )
    dataset = ["la11"]  # la_dataset
    # method = {""}
    for file_name in all_dataset:
        try:
            js = Shift()
            jobs = read_file_to_jobs(os.path.join(dir_name, file_name))
            js.addJobs(jobs)
            js.criticalPath()
            print(file_name)
            print("start:", js.makespan())
            js.shiftting_bottleneck()
        except:
            print("error:{}", file_name)
