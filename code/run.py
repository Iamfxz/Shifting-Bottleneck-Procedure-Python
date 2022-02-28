import os

from classes import Job, Shift


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
    prefix = "ta"  # "dmu" or 'ta'
    num = range(1, 5)  # range(16, 21) or range(80)
    for p in file_list:
        temp = p.split("/")
        run_flag = False
        for n in num:
            if n < 10:
                n = "0" + str(n)
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
