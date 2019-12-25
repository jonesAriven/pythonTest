import re
from datetime import datetime
import calendar
import time


# 题目一：企业发放的奖金根据利润提成。利润(I)低于或等于10万元时，奖金可提10%；
# 利润高于10万元，低于20万元时，低于10万元的部分按10%提成，高于10万元的部分，可提成7.5%；
# 20万到40万之间时，高于20万元的部分，可提成5%；40万到60万之间时高于40万元的部分，可提成3%；
# 60万到100万之间时，高于60万元的部分，可提成1.5%；
# 高于100万元时，超过100万元的部分按1%提成，从键盘输入当月利润I，求应发放奖金总数？
def caculateBonus():
    profit = int(input('Show me the money: '))
    bonus = 0
    thresholds = [100000, 100000, 200000, 200000, 400000]
    rates = [0.1, 0.075, 0.05, 0.03, 0.015, 0.01]
    for i in range(len(thresholds)):
        if profit <= thresholds[i]:
            bonus += profit * rates[i]
            profit = 0
            break
        else:
            bonus += thresholds[i] * rates[i]
            profit -= thresholds[i]
    bonus += profit * rates[-1]
    print(bonus)


# 题目2：一个整数，它加上100后是一个完全平方数，再加上168又是一个完全平方数，请问该数是多少？


def func1():
    n = 0
    while (n + 1) ** 2 - n * n <= 168:
        # print(n)
        n += 1
    for i in range((n + 1) ** 2):
        if i ** 0.5 == int(i ** 0.5) and (i + 168) ** 0.5 == int((i + 168) ** 0.5):
            print(i - 100)


# 题目二：输入某年某月某日，判断这一天是这一年的第几天？
# 特殊情况，闰年时需考虑二月多加一天
def func2():
    dateStr = input("请输入yyyy-mm-dd的日期格式:")

    def formatDate():
        # 判断输入的日期格式是否正确
        group = re.search(r'\d{4}-\d{1,2}-\d{1,2}', dateStr)
        # print(group)
        if not bool(group):
            print("日期格式不准确，请重新输入")
        else:
            # 通过引入datetime模块，把字符串转为date并获取天数
            dateTemp = datetime.strptime(group[0], "%Y-%m-%d").date()
            first_date_of_This_Year = datetime(dateTemp.year, 1, 1).date()
            print(dateTemp - first_date_of_This_Year)

    formatDate()


# 冒泡排序
def bubbleSort(arr):
    # arr = [1, 2, 19, 18, 10, 20]
    for i in range(0, len(arr) - 1):
        for j in range(0, len(arr) - i - 1):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    print(arr)


# 斐波那契数列（Fibonacci sequence），从1,1开始，后面每一项等于前面两项之和。图方便就递归实现，图性能就用循环。这里使用递归实现
# 递归实现
def Fib(n):
    return 1 if n <= 2 else Fib(n - 1) + Fib(n - 2)


# 乘法口诀
def fun3():
    for i in range(1, 10):
        for j in range(1, i + 1):
            # if i != j:
            #     print(i, "*", j, "=", (i * j), end=" ")
            # else:
            #     print(i, "*", j, "=", (i * j))
            # 或者使用以下方式
            print('%d*%d=%2ld ' % (i, j, i * j), end='')
    pass


# 暂停1秒输出
def fun4():
    for i in range(1, 10):
        time.sleep(2)
        print(i)


# 秒表，每隔1秒输出当前时间
def fun5():
    while datetime.now() < datetime(2019, 12, 17, 18, 13):
        time.sleep(1)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 以__开头的方法是魔术方法，是object的方法，
# __name__ 方法在主程序中调用，返回的是“__main__”，不是在主程序中调用，返回的是当前模块名
if __name__ == "__main__":
    # func1()
    # func2()
    # bubbleSort([1, 2, 20, 19, 78, 1999, 111, 29])
    # print(Fib(int(input("输入想求数列中的第几位数："))))
    # fun3()
    # fun4()
    fun5()
