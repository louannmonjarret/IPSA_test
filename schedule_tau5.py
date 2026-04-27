import itertools
import numpy as np

all_tasks = [
    ("tau1", 3, 10),
    ("tau2", 3, 10),
    ("tau3", 2, 20),
    ("tau4", 2, 20),
    ("tau5", 2, 40),
    ("tau6", 2, 40),
    ("tau7", 3, 80),
]

def lcm(a, b):
    return a * b // np.gcd(a, b)

def hyperperiod(tasks):
    result = 1
    for _, _, T in tasks:
        result = lcm(result, T)
    return result

def generate_jobs(tasks, H):
    jobs = []
    for name, C, T in tasks:
        for k in range(H // T):
            jobs.append((f"{name},{k+1}", k*T, (k+1)*T, C))
    return jobs

def simulate(order):
    time = 0
    total_wait = 0
    for job in order:
        name, release, deadline, duration = job
        if time < release:
            time = release
        wait = time - release
        total_wait += wait
        time += duration
        if time > deadline:
            return False, float('inf')
    return True, total_wait

def schedule_edf(jobs):
    remaining = list(jobs)
    order = []
    time  = 0
    while remaining:
        available = [j for j in remaining if j[1] <= time]
        if not available:
            time = min(j[1] for j in remaining)
            available = [j for j in remaining if j[1] <= time]
        chosen = min(available, key=lambda j: j[2])
        order.append(chosen)
        remaining.remove(chosen)
        time += chosen[3]
    valid, wait = simulate(order)
    return order, wait

def print_schedule(order):
    time = 0
    total_idle = 0
    total_wait = 0
    for job in order:
        name, release, deadline, duration = job
        if time < release:
            idle = release - time
            print(f"  [t={time:3d} -> t={release:3d}] IDLE ({idle} unites)")
            total_idle += idle
            time = release
        wait  = time - release
        start = time
        end   = time + duration
        print(f"  [t={start:3d} -> t={end:3d}] {name:10s} attente={wait} deadline={deadline}")
        total_wait += wait
        time = end
    print(f"\n  Attente totale : {total_wait}")
    print(f"  Idle total     : {total_idle}")


H    = hyperperiod(all_tasks)
jobs = generate_jobs(all_tasks, H)

#Schedule normal
order_normal, wait_normal = schedule_edf(jobs)

#On retire le job 1 de tau5
jobs_reduced = [j for j in jobs if j[0] != "tau5,1"]
order, wait  = schedule_edf(jobs_reduced)

#Résultats
print(f"Comparaison : ")
print(f"Schedule normal                     : attente = {wait_normal}")
print(f"Meilleur schedule en sautant tau5,1 : attente = {wait}")
print(f"\n{'-'*55}")
print(f"Schedule avec tau5,1 sauté (deadline manquée)")
print_schedule(order)
