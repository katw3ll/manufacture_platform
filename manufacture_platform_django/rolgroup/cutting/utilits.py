def knapsack(A, S):
    F = [1] + [0] * S
    Prev = [-1] * (S + 1)

    for j in range(len(A)):
        for i in range(S, A[j] - 1, -1):
            if F[i - A[j]] == 1:
                F[i] = 1
                Prev[i] = A[j]
    
    i = S
    while F[i] == 0:
        i -= 1

    Cutting = []
    curr = i
    while curr > 0:
        Cutting.append(Prev[curr])
        curr -= Prev[curr]
    
    return S - i, Cutting

def cut(A, S, Waste, Lecvide, removing=True):
    R, cutting = knapsack(A, S)
    if R <= Lecvide and R >= Waste:
        R, cutting = knapsack(A, S-Lecvide)
        R += Lecvide

    if removing:
        for x in cutting:
            A.remove(x)
    
    return R, cutting

def pack_to_list(data):
    A = []
    for d in data:
        # print(d)
        A.extend([d[0]]*d[1])
    A.sort()
    return A