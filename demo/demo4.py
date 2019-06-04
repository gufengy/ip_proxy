# 测试python 反射


class demo:

    role = "abc"

    def func(self):
        print("*"*self)


print(hasattr(demo, "role1"))    # hasattr方法，判断role属性是否在A的命名空间里
print(getattr(demo, "role"))    #  getattr方法，从A的命名空间里找一个属性，直接就可以找到这个属性
# print(setattr(demo, "func"))    #  判断func是否在A的命名空间
print(getattr(demo, "func"))
aa = getattr(demo, "func")
aa(15)

# get_proxy_1 = get_proxy.get_proxy().proxy_list
#
# for proxy in get_proxy_1:
#     func = getattr(get_proxy.get_proxy, proxy)
#     func(1, 1)

i = iter(range(3))
print(next(i))
print(next(i))
print(next(i))
i = iter(range(3))
print(next(i))