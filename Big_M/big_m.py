import numpy as np

M = 1000000
variables = ['x1', 'x2', 'x3', 's1', 's2', 'a2', 'a3']
A = np.array([
    [2, 1, 3, 1,  0, 0, 0],
    [1, 2, 1, 0, -1, 1, 0],
    [1, 1, 1, 0,  0, 0, 1]
], dtype=float)
b = np.array([120, 80, 50], dtype=float)
c = np.array([50, 40, 70, 0, 0, -M, -M], dtype=float)
tableau = np.zeros((4, 8))
tableau[:3, :7] = A
tableau[:3, 7] = b
tableau[3, :7] = -c
tableau[3] -= M * tableau[1]
tableau[3] -= M * tableau[2]
basis = [3, 5, 6]
def display_tableau(tableau, basis, iteration):
    print("\n" + "=" * 70)
    print("Iteration", iteration)
    print("=" * 70)
    header = variables + ["RHS"]
    print("Basic\t" + "\t".join(f"{x:>10}" for x in header))
    for i in range(3):
        row = [f"{tableau[i, j]:10.2f}" for j in range(8)]
        print(f"{variables[basis[i]]:>5}\t" + "\t".join(row))
    row = [f"{tableau[3, j]:10.2f}" for j in range(8)]
    print(f"{'Z':>5}\t" + "\t".join(row))
iteration = 0
display_tableau(tableau, basis, iteration)
while True:
    entering = np.argmin(tableau[3, :-1])
    if tableau[3, entering] >= -1e-9:
        break
    ratios = []

    for i in range(3):

        if tableau[i, entering] > 1e-9:
            ratio = tableau[i, -1] / tableau[i, entering]
        else:
            ratio = np.inf

        ratios.append(ratio)
    leaving = np.argmin(ratios)

    if ratios[leaving] == np.inf:
        print("The problem is unbounded.")
        break
    pivot = tableau[leaving, entering]

    tableau[leaving] = tableau[leaving] / pivot
    for i in range(4):

        if i != leaving:
            tableau[i] -= tableau[i, entering] * tableau[leaving]

    basis[leaving] = entering

    iteration += 1

    display_tableau(tableau, basis, iteration)

solution = np.zeros(7)

for i in range(3):
    solution[basis[i]] = tableau[i, -1]

print("\n" + "=" * 70)
print("OPTIMAL SOLUTION")
print("=" * 70)

for i in range(3):
    print(f"{variables[i]} = {solution[i]:.2f}")

print(f"\nMaximum Profit (Z) = {tableau[3, -1]:.2f}")
print("\nArtificial Variables:")
print(f"a2 = {solution[5]:.2f}")
print(f"a3 = {solution[6]:.2f}")

if abs(solution[5]) < 1e-6 and abs(solution[6]) < 1e-6:
    print("\nBoth artificial variables are zero.")
    print("Hence, the solution is feasible and optimal.")
else:
    print("\nArtificial variable is non-zero.")
    print("The problem has no feasible solution.")
