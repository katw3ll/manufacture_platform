from .utilits import cut, pack_to_list


# rests_data = dict( {1180: 10,  length: quantity
#                     1350: 11,
#                     1580: 10,
#                     1370: 10})  # Остатки на складе Stock
#
# cutting_data = [[1220, 40], длинна: количество length: quantity
#                 [1340, 11],
#                 [1550, 200],
#                 [1270, 10]]  # Что нужно распилить Composition
#
# A = pack_to_list(cutting_data)
#
# S = 6000  # Стандартная длинна материалов default_lenght
# L = 500  # Ликвидный остаток good_cut
# W = S * 0.02  # Отходы от материалов (проценты)
#
# result = []
#
# unsuitable_rests = set()


def cutting(rests_data, cutting_data, S, L):

    # print(rests_data)

    # print()

    # print(cutting_data)

    A = pack_to_list(cutting_data)

    W = S * 0.02

    result_old = []
    result_new = []

    unsuitable_rests = set()

    while A and rests_data.keys() and len(unsuitable_rests) != len(rests_data.keys()):
        min_waste = S
        need_rest = None
        for index, r in enumerate(rests_data.keys()):
            if r < A[0]:
                unsuitable_rests.add(r)
                continue
            waste, _ = cut(A, r, W, L, removing=False)
            if waste < min_waste:
                min_waste = waste
                need_rest = r

        if not (need_rest):
            continue

        rest, cutting = cut(A, r, W, L)
        rests_data[r] -= 1
        if rests_data[r] <= 0:
            del rests_data[r]

        result_old.append({"material": r, "rest": rest, "map": cutting})

    while A:
        rest, cutting = cut(A, S, W, L)
        result_new.append({"material": S, "rest": rest, "map": cutting})
    return result_new, result_old

if __name__ == "__main__":
    rests_data = dict({1180: 10,
                       1350: 11,
                       1580: 10,
                       1370: 10})  # Остатки на складе

    cutting_data = [[1220, 40],
                    [1340, 11],
                    [1550, 200],
                    [1270, 10]]

    S = 6000  # Стандартная длинна материалов default_lenght
    L = 500
    print()
    print(cutting(rests_data, cutting_data, S, L))