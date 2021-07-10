def fibonacci(n):
    a = b = 1
    for i in range(n):
        yield a
        a, b = b, a + b
 
for k in fibonacci(10):
    print(k)
