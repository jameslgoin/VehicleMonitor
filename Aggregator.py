import shlex
import subprocess
from threading import Thread

DEBUG_TESTING = True


class Aggregator(object):
    def __init__(self):
        self.content = {}
        self.components = []
        self.thread_pool = []
        pass

    def __str__(self):
        return str(self.components) + '\n' + str(self.content) + '\n' + str(self.thread_pool)

    def register_component(self, command, separator=':'):
        """
        register the command to gather the data generated it by calling it in a subprocess
        :param command: the command user runs
        :param separator: the separator that distinguish key and value
        :param delimiter: the separator that distinguish different kv pairs
        :return: none
        """
        args = shlex.split(command)

        def func():
            proc = subprocess.Popen(args, stdout=subprocess.PIPE)
            while True:
                line = proc.stdout.readline().decode()[:-1]
                kv = line.split(separator)
                self.content[kv[0]] = kv[1]
        self.components.append(func)

    def start_gathering(self):
        """
        start all registered command to gather input data
        :raise RuntimeError: if this function has already been called
        """
        if len(self.thread_pool) > 0:
            raise RuntimeError('already started processes')
        for func in self.components:
            th = Thread(target=func, daemon=True)
            th.start()
            self.thread_pool.append(th)

    def get_content(self):
        return self.content


if __name__ == '__main__' and DEBUG_TESTING:
    agg = Aggregator()
    agg.register_component("python test.py")
    agg.start_gathering()
    import time
    while True:
        print(agg.get_content())
        time.sleep(1)
