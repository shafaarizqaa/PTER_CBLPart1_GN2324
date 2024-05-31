import timeit


def fib(n) :
   if n < 2 :
      return n
   else :
      return fib(n-1) + fib(n-2)

number = int(input("Number: "))
start_time = timeit.default_timer()
number = fib(number)
time = (timeit.default_timer() - start_time)

print("Output : ", number)
print("Time : ", format(time, '.10f'))