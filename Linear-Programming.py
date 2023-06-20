from scipy.optimize import linprog

if __name__ == '__main__':
    select = input("max/min?: ") # hàm mục tiêu là max hay min
    n = int(input("Number of variables = ")) # số lượng biến
    k = int(input("Number of binding functions = ")) # số lượng hàm ràng buộc
    obj = input("Objective function: ").split() # Nhập hàm mục tiêu
    obj = [(int(x) if select == 'min' else -int(x)) for x in obj] # xử lí hàm mục tiêu

    # các mảng để lưu
    lhs = []
    rhs = []
    lhs_eq = []
    rhs_eq = []
    bnd = []

    # xử lí
    for i in range (0, k):
        print("Binding function", i + 1, end = ": ")
        arr = input().split()

        lst_element = []
        for j in range (0, n):
            lst_element.append(int(arr[j]))

        if arr[n] == '>=':
            for j in range(0, n):
                lst_element[j] = -lst_element[j]
            arr[n + 1] = -int(arr[n + 1])

        if arr[n] == '=':
            lhs_eq.append(lst_element)
            rhs_eq.append(int(arr[n + 1]))
        else:
            lhs.append(lst_element)
            rhs.append(int(arr[n + 1]))

    if not lhs:
        lst = []
        for i in range (0, n):
            lst.append(1)

        lhs.append(lst)
        rhs.append(0)

    if not lhs_eq:
        lst = []
        for i in range (0, n):
            lst.append(0)

        lhs_eq.append(lst)
        rhs_eq.append(0)

    for i in range (0, n):
        print("Binding condition of variable", i + 1, end = ": ")
        lst = input().split()
        lst[0] = int(lst[0]) if lst[0] != 'none' else None
        lst[1] = int(lst[1]) if lst[1] != 'none' else None

        bnd.append(lst)

    # đáp án của bài toán
    optimal_result = linprog(c = obj, A_ub = lhs, b_ub = rhs, A_eq = lhs_eq, b_eq = rhs_eq, bounds = bnd)

    print("The result for the objective function is", optimal_result.fun if select == 'min' else -optimal_result.fun)
    print("The value of the variables x:", optimal_result.x)