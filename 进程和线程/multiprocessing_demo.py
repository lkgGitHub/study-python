"""多进程"""
import subprocess
from multiprocessing import Process, Pool
import os, time, random


# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))


def run_proc_main():
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()  # 用start()方法启动
    p.join()  # join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步。
    print('Child process end.')


def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


def process_pool():
    print('Parent process %s.' % os.getpid())
    p = Pool(4)  # 由于Pool的默认大小是CPU的核数
    for i in range(9):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()  # 调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process
    p.join()  # 对Pool对象调用join()方法会等待所有子进程执行完毕
    print('All subprocesses done.')


if __name__ == '__main__':
    print('$ nslookup')
    p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
    print(output.decode('utf-8'))
    print('Exit code:', p.returncode)