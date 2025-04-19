import asyncio
import logging
import logging.handlers
from queue import Queue
from typing import List

class LocalQueueHandler(logging.handlers.QueueHandler):
	def emit(self, record: logging.LogRecord) -> None:
		#remove the call to self.prepare(), handle task cancellation
		try:
			self.enqueue(record)
		except asyncio.CancelledError:
			raise
		except Exception:
			self.handlerError(record)

def setup_logging_queue() -> None:
	#Move log handlers to a separate thread.
	#replace handlers on the root logger with a LocalQueueHandler
	#and start a logging.QueueListener holding the original
	#handlers
	queue = Queue()
	root = logging.getLogger()
	handlers: List[logging.Handler] = []

	handler = LocalQueueHandler(queue)
	for h in root.handlers[:]:
		if h is not handler:
			root.removeHandler(h)
			handlers.append(h)

	listener = logging.handlers.QueueListener(
		queue, *handlers, respect_handler_level=True
		)
	listener.start()

#to be added to logging config in Class section
