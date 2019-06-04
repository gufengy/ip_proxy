# 多进程演示

from multiprocessing import Pool
import time

def test(i):
    a = 1
    time.sleep(5)
    print(i)


if __name__ == '__main__':
    # lists = range(100)
    # pool = Pool(8)
    # pool.map(test, lists)
    # pool.close()
    # pool.join()

    import os
    print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))












