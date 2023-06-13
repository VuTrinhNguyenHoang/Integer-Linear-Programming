from scipy.optimize import linprog
from queue import Queue
import os, time

class IntegerLP:
    def __init__(self, obj, lhs, rhs, lhs_eq, rhs_eq, bnd):
        self.obj = obj # các hệ số của hàm mục tiêu
        self.lhs = lhs # các hệ số của vế trái hàm ràng buộc (Ax <=, => b)
        self.rhs = rhs # các hệ số của vế phải hàm ràng buộc (Ax <=, => b)
        self.lhs_eq = lhs_eq # các hệ số của vế trái hàm ràng buộc (Ax = b)
        self.rhs_eq = rhs_eq # các hệ số của vế phải hàm ràng buộc (Ax = b)
        self.bnd = bnd # giới hạn của các biến
    
    def linear_programming(self, answer, times = 0):
        """Đây là hàm xử lí vấn đề tối ưu với số nguyên"""
        
        q = Queue(-1) # tạo hàng đợi q không giới hạn phần tử
        q.put(self.bnd) # thêm ràng buộc vào hàng đợi

        """Vòng lặp while sẽ thực hiện xử lí các kết quả của hàm linprog(),
           vòng lặp sẽ dừng khi trong hàng đợi không còn phẩn tử hoặc đã vượt
           quá số lần lặp"""
        while (not q.empty()) and times <= 10000:
            times += 1 # tăng số lần lặp lên 1 đơn vị
            bounds = q.get() # lấy phần tử trong hàng đợi
            flag = 1 # biến dùng để kiểm tra tính nguyên của các biến

            # optimization là kết quả của hàm linprog() trả về
            optimization = linprog(c = self.obj, A_ub = self.lhs, b_ub = self.rhs, 
                                   A_eq = self.lhs_eq, b_eq = self.rhs_eq, bounds = bounds)

            # nếu trạng thái trả về khác 0, nghĩa là không có kết quả của bài toán thì bỏ qua không xử lí
            if optimization.status: 
                continue

            """Duyệt hết các phần tử trong mảng kết quả của biến x để kiểm tra tính nguyên"""
            for i in range (0, len(optimization.x)):
                if optimization.x[i].is_integer() == False: 
                    """nếu giá trị tại vị trí i không nguyên"""
                    flag = 0 # biến flag = 0 nghĩa là có phần tử trong mảng không là số nguyên

                    # giải quyết vấn đề bằng phương pháp nhánh cận
                    # nhánh 1
                    new_bnd1 = list(bounds) 
                    new_bnd1[i] = [bounds[i][0], int(optimization.x[i])]
                    q.put(new_bnd1) # thêm nhánh 1 vào hàng đợi

                    # nhánh 2
                    new_bnd2 = list(bounds)
                    new_bnd2[i] = [int(optimization.x[i]) + 1, bounds[i][1]]
                    q.put(new_bnd2) # thêm nhánh 2 vào hàng đợi
 

            # nếu biến flag = 1 nghĩa là kết quả của tất cả các biến đều là nguyên
            # ta kiểm tra xem nếu kết quả của hàm mục tiêu lớn hơn giá trị hiện tại
            if flag and optimization.fun < answer[0]:
                answer[0] = optimization.fun
                answer[1] = optimization.x

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

    # khởi tạo đáp án ban đầu
    answer = [float('inf'), []]
    optimal_result = IntegerLP(obj, lhs, rhs, lhs_eq, rhs_eq, bnd).linear_programming(answer)

    if len(answer[1]) == 0:
        print("The result for the objective function is infinite")
    else:
        print("The result for the objective function is", answer[0] if select == 'min' else -answer[0])
        print("The value of the variables x:", answer[1])