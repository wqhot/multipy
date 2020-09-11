#!/usr/bin/env python3
# -*- coding: utf-8 -*-\

from multipy import multipy
import time
import os


mmm = multipy(max_cpu=3)

def test_func(ttt):
    print(str(os.getpid()) + " start")
    for i in range(2):
        time.sleep(ttt)
    print(str(os.getpid()) + " over")

def main():
    
    mmm.add_task(test_func,(4,))
    mmm.add_task(test_func,(3.5,))
    mmm.add_task(test_func,(8,))
    mmm.add_task(test_func,(5,))
    mmm.add_task(test_func,(6,))

    mmm.close()
    mmm.start()
    mmm.join()
    print("FINISH")


if __name__ =='__main__':
    main()