
try:
    i = 1
    i = i + "11"
except TypeError as e:
    print(e.args[0])
    print("typeError")

