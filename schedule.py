import itertools
import numpy as np

#Définition des tâches
all_tasks = [
    ("tau1", 3, 10), #C1 = 3 déterminé grâce aux fichiers multiply.c et final.py
    ("tau2", 3, 10),
    ("tau3", 2, 20),
    ("tau4", 2, 20),
    ("tau5", 2, 40),
    ("tau6", 2, 40),
    ("tau7", 3, 80),
]

#Calcule le plus petit commun multiple (permet de determiner H ensuite)
def lcm(a, b):
    return a * b // np.gcd(a, b)

#Calcule l'hyperpériode : comme je fais le choix d'ajouter une par une les taches --> obligé de calculer H à chaque fois car peut changer
def hyperperiod(tasks):
    result = 1
    for _, _, T in tasks:
        result = lcm(result, T)
    return result

#Génére les jobs sur l'hyperpériode H déterminéejuste avant 
def generate_jobs(tasks, H):
    jobs = []
    for name, C, T in tasks:
        for k in range(H // T): #nombre de jobs possible de cette taches
            jobs.append((f"{name},{k+1}", k*T, (k+1)*T, C)) 
    return jobs

#Simule l'execution des jobs dans un certain ordre
#renvoie True si aucune deadline manquée et attente_totale pour savoir combien chaque job attend
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

#Determination du schedule optimal avec itertools.permutations
#qui permet de tester toutes les permutations possibles et garder celle avec le moins d'attente totale + sans deadline manquée
#MAIS ne fonctionne que pour un nombre limité de taches sinon c'est trop long
def schedule_permu(jobs):
    best_order  = None
    best_wait   = float('inf')
    valid_count = 0

    for perm in itertools.permutations(jobs):
        valid, wait = simulate(perm)
        if valid:
            valid_count += 1
            if wait < best_wait:
                best_wait  = wait
                best_order = perm
    return best_order, best_wait, valid_count

#Determination du schedule optimale avec Earliest Deadline First
#permet de trouver, parmi les jobs disponibles, celui avec la deadline la plus proche
#sur de ne pas rater de deadline si système schedulable + fonctionne pour les 7 taches de manières plus rapide
def schedule_edf(jobs):

    remaining = list(jobs)
    order = []
    time  = 0
    while remaining:
	#jobs disponibles 
        available = [j for j in remaining if j[1] <= time]
        if not available:
	    #Aucun jobs disponibles --> on attend jusqu'au prochaine "release time"
            time = min(j[1] for j in remaining)
            available = [j for j in remaining if j[1] <= time]
        # Choisir la deadline la plus proche
        chosen = min(available, key=lambda j: j[2])
        order.append(chosen)
        remaining.remove(chosen)
        time += chosen[3]
    valid, wait = simulate(order)
    return order, wait if valid else float('inf'), valid

#Affichage du schedule
def print_schedule(order):
    time = 0
    total_idle = 0
    total_wait = 0
    for job in order:
        name, release, deadline, duration = job
        if time < release:
            idle = release - time
            print(f"  [t_début={time:3d} -> t_fin={release:3d}] IDLE ({idle} unites)")
	    total_idle += idle
            time = release
        wait  = time - release
        start = time
        end   = time + duration
        missed = "DEADLINE MISSED" if end > deadline else ""
        print(f"  [t_début={start:3d} -> t_fin={end:3d}] {name:10s} attente={wait} deadline={deadline}{missed}")
        total_wait += wait
        time = end
    print(f"\n  Attente totale : {total_wait}")
    print(f"  Idle total     : {total_idle}")

#Étapes (boucle principale)
#On ajoute les taches une par une pour voir quel algo fonctionne le mieux
for i in range(1, len(all_tasks) + 1):
    tasks = all_tasks[:i]
    H     = hyperperiod(tasks) #plus grande période
    jobs  = generate_jobs(tasks, H)
    U     = sum(C/T for _, C, T in tasks) #Vérification de la schedulabilité à chaque fois

    print("-" * 50)
    print(f"Tasks analysed : {[t[0] for t in tasks]}")
    print(f"Hyperperiode : {H}")
    print(f"Jobs : {len(jobs)}")
    if U > 1:
        print(f"Non schedulable : U = {U:.4f} > 1)")
        break
    else:
        print(f"Schedulable : U = {U:.4f} <= 1")

    if len(jobs) <= 7: #méthode itetools fonctionne seulement pour un petit nombre de jobs et garantit un schedule optimal dans ce cas
        print(f"  Methode : itertools permutations")
        order, wait, valid_count = schedule_permu(jobs)
        print(f"  Permutations valides : {valid_count}")
    else: #trop de jobs pour que itertools soit efficace --> utilisation de EDF
        print(f"  Methode : Earliest Deadline First (EDF)")
        order, wait, valid = schedule_edf(jobs)

    if order and wait != float('inf'):
        print(f"\n  Schedule (attente totale={wait}) :")
        print_schedule(order)
    else:
        print("  Aucun schedule valide trouve")
    print()
