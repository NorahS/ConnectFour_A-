### AI Project - MiniMax ConnectFour
### Fall'17, PSU  Dana AlHenaki and Norah ALsabti
###Copied From the skelton code to run ID

from threading import Thread
from time import time


class ContinuousThread(Thread):
    """
    A thread that runs a function continuously,
    with an incrementing 'depth' kwarg, until
    a specified timeout has been exceeded
    """

    def __init__(self, timeout=5, target=None, group=None, name=None, args=(), kwargs={}):
        """
        Store the various values that we use from the constructor args,
        then let the superclass's constructor do its thing
        """
        self._timeout = timeout
        self._target = target
        self._args = args
        self._kwargs = kwargs
        Thread.__init__(self, args=args, kwargs=kwargs, group=group, target=target, name=name)

    def run(self):
        """ Run until the specified time limit has been exceeded """
        depth = 1

        timeout = self._timeout**(1/2.0)  # Times grow exponentially, and we don't want to
                                          # start a new depth search when we won't have
                                          # enough time to finish it

        end_time = time() + timeout
        
        while time() < end_time:
            self._kwargs['depth'] = depth
            self._most_recent_val = self._target(*self._args, **self._kwargs)
            depth += 1

    def get_most_recent_val(self):
        """ Return the most-recent return value of the thread function """
        try:
            return self._most_recent_val
        except AttributeError:
            print "Error: You ran the search function for so short a time that it couldn't even come up with any answer at all!  Returning a random column choice..."
            import random
            return random.randint(0, 6)
    
def run_search_function(board, search_fn, eval_fn, timeout = 5):
    """
    Run the specified search function "search_fn" to increasing depths
    until "time" has expired; then return the most recent available return value

    "search_fn" must take the following arguments:
    board -- the ConnectFourBoard to search
    depth -- the depth to estimate to
    eval_fn -- the evaluation function to use to rank nodes

    "eval_fn" must take the following arguments:
    board -- the ConnectFourBoard to rank
    """

    eval_t = ContinuousThread(timeout=timeout, target=search_fn, kwargs={ 'board': board,
                                                                          'eval_fn': eval_fn })

    eval_t.setDaemon(True)
    eval_t.start()
    
    eval_t.join(timeout)

    # Note that the thread may not actually be done eating CPU cycles yet;
    # Python doesn't allow threads to be killed meaningfully...
    ret = eval_t.get_most_recent_val()
    return (int(ret[0]),str(ret[1]))
