# -*- coding: utf-8 -*-\

import multiprocessing
import time
# from ctypes import c_bool, c_int

class multipy():

    def __init__(self, max_cpu, cb_func=None, show_processbar=True):
        # condition of processbar
        self.bar_cond = multiprocessing.Condition()
        self.bar_que = multiprocessing.Queue()
        self.show_processbar = show_processbar

        self.__max_cpu = max_cpu
        self.__runing = multiprocessing.Value('I', 0)
        self.__close = multiprocessing.Value('I', 0)
        # 进程计数
        self.__count = multiprocessing.Value('I', 0)
        # 结束条件变量
        self.__finish_cond = multiprocessing.Condition()
        # 单个进程结束条件变量
        self.__count_cond = multiprocessing.Condition()
        
        self.task_que = multiprocessing.Queue()
        self.que_data = multiprocessing.Queue()

        #
        # if show_processbar:
        #     processbar_p = multiprocessing.Process(target=self.show_bar, args=(len(nodes_on_surface), 
        #             self.bar_que, self.bar_cond))

    # 添加进程列表
    def add_task(self, func, args=()):
        # 未关闭时
        if self.__close.value == 0:
            self.task_que.put({'func':func, 'args':tuple(args)})
        return self.task_que.qsize()

    # 关闭进程列表添加功能
    def close(self):
        self.__close.value = 1

    def start(self):
        # 未关闭时返回
        if self.__close.value == 0:
            return
        # 已经运行返回
        if self.__runing.value == 1:
            return
        self.__runing = 1
        process_task_p = multiprocessing.Process(target=self.process_task_list, args=(
            self.task_que, self.__count, self.__max_cpu, self.__finish_cond, self.__count_cond,
            self.process_task
        ))
        process_task_p.start()

        # while not self.task_que.empty():
            
        #     while (self.__count > self.__max_cpu):
        #         time.sleep(0.05)
            
        #     task_info = self.task_que.get()
        #     self.__count = self.__count + 1
        #     thread = multiprocessing.Process(target=self.process_task, args=(task_info['func'], task_info['args'], self.__count))
        #     thread.start()
            # threads.append(thread)
            # process_task_p = multiprocessing.Process(target=self.process_task_list)
            
    def process_task_list(self, task_que, count, max_cpu, finish_cond, count_cond, process_task):
        # 超过最大进程数，等待进程退出
        while not task_que.empty():
            count.value = count.value + 1
            # 取出队列
            while count.value > max_cpu:
                if count_cond.acquire():
                    count_cond.wait()
                    count_cond.release()
            task_info = task_que.get()       
            thread = multiprocessing.Process(target=process_task, args=(task_info['func'], task_info['args'], 
                count, count_cond))
            thread.start()
        with finish_cond:
            finish_cond.notify_all()
    
    def join(self):
        # 超过最大进程数，等待进程入列完毕
        while not self.task_que.empty():
            if self.__finish_cond.acquire():
                self.__finish_cond.wait()
                self.__finish_cond.release()
        print("que empty")
        # 等待进程计数器清零
        while not self.__count.value == 0:
            if self.__count_cond.acquire():
                self.__count_cond.wait()
                self.__count_cond.release()

    def process_task(self, func, args, count, count_cond):
        try:
            func(*args)
        except Exception as e:
            print(e)      
        count.value = count.value - 1
        with count_cond:
            count_cond.notify_all()

    def processbar_process(self):
        pass
