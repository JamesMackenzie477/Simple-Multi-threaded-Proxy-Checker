from contextlib import suppress
from multiprocessing.pool import ThreadPool
import threading
import requests


class ProxyChecker:
    """Class used to check a proxy list for validity"""
    def __init__(self, proxylist, savefile, threads=200, timeout=25):
        # declares variables
        self.proxylist = proxylist
        self.savefile = savefile
        self.threads = threads
        self.timeout = timeout
		# creates a file I/O lock
		self.flock = threading.Lock()

    def start_check(self):
        # multi-threaded processes
        p = ThreadPool(processes=self.threads)  # creates a pool of workers
        p.map(self.check_proxy, self.proxylist)  # calls check_proxy with the proxy as parameter
        p.close()  # closes the multi-threaded processes

    def check_proxy(self, proxy):
        # adds proxy to the proxies dict to be used with requests
        proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
        # suppresses any exceptions, such as proxy timeout
        with suppress(Exception):
            # makes request to google using the proxy
            requests.get('https://www.google.com', proxies=proxies, timeout=self.timeout)
            # if request does not timeout then proxy is printed and written to file
            print(proxy)
			with self.flock():
            	with open(self.savefile, 'a') as f:
                	f.write(proxy + '\n')


def main():
    # gets filename from user
    filename = input('please enter the name of the proxy list: ')

    # tries to open file
    try:
        with open(filename, 'r') as f:
            proxies = f.read().split('\n')
    except IOError:
        print('invalid file')
        main()

    # initalizes ProxyChecker with the proxy list and the savefile name
    c = ProxyChecker(proxylist=proxies, savefile='available.txt')
    # starts the check
    c.start_check()

if __name__ == '__main__':
    main()