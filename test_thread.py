import threading
import time


class SomeClass(object):
	def __init__(self):
		self.thread_stop = threading.Event()
		self.thread = threading.Thread(target=self.print_arg, args=['foobar'])
		self.thread.daemon = True

	def start_thread(self):
		if not self.thread.is_alive():
			self.thread.start()
		else:
			self.thread_stop.clear()

	def stop_thread(self):
		return self.thread_stop.set()

	def print_arg(self, arg1):
		while True:
			if not self.thread_stop.isSet():
				print(arg1)
				time.sleep(1)

sc = SomeClass()
sc.start_thread()
for i in range(0,10):
	print(i)
	time.sleep(1)
sc.stop_thread()
for i in range(0,10):
	print(i)
	time.sleep(1)
sc.start_thread()
for i in range(0,10):
	print(i)
	time.sleep(1)

