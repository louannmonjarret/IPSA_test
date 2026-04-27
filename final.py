import os
import numpy as np
import matplotlib.pyplot as plt

N = 100

open("output.txt", "w").close()

#Lance multiply N fois et mesure son temps d'execution
for i in range(N):
    os.system("{ time ./multiply;} 2>&1 | grep -oP '^[\\d.]+(?=user)' >>output.txt")

#Lecture des résultats dans le fichier texte "output"
with open("output.txt", "r") as f:
    times = [float(line.strip()) for line in f.readlines()]

print(f"Nombre de runs : {N}")

#Calcul de Q1,Q2,Q3 et du min et max puis C1 grâce au max
Q1, Q2, Q3 = np.quantile(times, [0.25, 0.5, 0.75])
min = np.min(times)
max = np.max(times)
WCET = max *1.2

#Affichage des valeurs
print(f"min : {min} s")
print(f"Q1 : {Q1} s")
print(f"Q2 : {Q2} s")
print(f"Q3 : {Q3} s")
print(f"Max : {max} s")
print(f"WCET : {WCET} s")

#Affichage d'un histogram représentant ces valeurs
fig, ax = plt.subplots(figsize=(10, 5))
 
ax.hist(times, bins=20, color="steelblue", edgecolor="white", alpha=0.85)
 
ax.axvline(min, color="green",   linestyle="--", linewidth=1.5, label=f"Min  = {min:.3f} s")
ax.axvline(Q1,    color="orange",  linestyle="--", linewidth=1.5, label=f"Q1   = {Q1:.3f} s")
ax.axvline(Q2,    color="gold",    linestyle="-",  linewidth=2.0, label=f"Q2   = {Q2:.3f} s")
ax.axvline(Q3,    color="orange",  linestyle="--", linewidth=1.5, label=f"Q3   = {Q3:.3f} s")
ax.axvline(max, color="red",     linestyle="--", linewidth=1.5, label=f"Max  = {max:.3f} s")
ax.axvline(WCET,  color="darkred", linestyle="-",  linewidth=2.0, label=f"WCET C1 = {WCET:.3f} s")
 
ax.set_title("Distribution des temps d'exécution de τ1", fontsize=14)
ax.set_xlabel("Temps d'exécution (s)")
ax.set_ylabel("Nombre de mesures")
ax.legend()
plt.tight_layout()
plt.savefig("wcet_histogram.png", dpi=150)
plt.show()
print("\nHistogramme sauvegardé dans wcet_histogram.png")


