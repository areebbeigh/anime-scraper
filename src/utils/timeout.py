import time

def call_till_true(func, timeout,*args):
    """
        Calls given function with given args until the value returned is truthy or
        it exceeds the timeout. 
        
        Returns the value returned by the given function and number of calls made in
        a tuple with the third value as True in case of success else returns (False, False, False).
    """
    start = time.time()
    calls = 0
    while True:
        res = func(*args)
        calls += 1
        if res:
            break
        if (time.time() - start) > timeout:
            return (False, False, False)
        
    return (res, calls, True)
