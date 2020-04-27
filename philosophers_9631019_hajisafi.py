import threading
import time 

ph = [threading.Lock(), threading.Lock(), threading.Lock(), threading.Lock(), threading.Lock()] #each philosopher has a corresponding lock
lock = threading.Lock() #we use this lock as mutex for shared data between threads
state = ["thinking", "thinking", "thinking", "thinking", "thinking"] #each philosopher has a state which is in ('thinking', 'hungry', 'eating')
phcount = [0, 0, 0, 0, 0] #each philosopher has a corresponding count which shows the number of activated acquired corresponding lock

def philosopher(i): #this method is what threads will run
    while True:
    #    think()
        print("philosopher ", i, " is thinking")
        time.sleep(2) #delay
        takeForks(i) #attempt to pick up the forks on his left and right
    #    eat()
        print("philosopher ", i, " is eating")
        time.sleep(2)
        print("philosopher ", i, " finished eating")
        time.sleep(2)
        putDownForks(i) #finished eating, so the philosopher puts down the forks
        
        
def takeForks(i): #attempt to pick up forks
    lock.acquire() #same as wait(mutex)
    state[i-1] = "hungry" #current philosopher is now hungry
    test(i) #test whether he can pick up the forks or not
    lock.release() #same as signal(mutex)
    ph[i-1].acquire()
    lock.acquire() #wait(mutex)
    phcount[i-1] += 1 #number of currently active acquired locks for this philosopher increased
    lock.release() #signal(mutex)
    
    
def test(i): #test whether philosopher i can pick up the forks in front of him or not
    if state[i-1] == "hungry" and state[(i-2)%5] != "eating" and state[(i)%5] != "eating": #this means the philosophers on left and right are not eating, so both forks are available on the table to be picked up
        state[i-1] = "eating" #philopher i picked up both forks and he goes to eating state
        if phcount[i-1] > 0: #releasing acquired locks. we use phcount in order to prevent releasing an already released lock
            ph[i-1].release()
            phcount[i-1] -= 1 #number of active acquired locks decreased
    
    
def putDownForks(i): #philosopher i finished eating and he's putting down the forks. He informs both philosophers on his left and right
    lock.acquire()
    state[i-1] = "thinking"
    test((i+1)%5) #left philosopher checks if he can pick up the forks or not
    test((i-1)%5) #right philosopher checks if he can pick up the forks or not
    lock.release()
    
    
def main(): #making threads and calling them with a little delay
    t1 = threading.Thread(target = philosopher, args = (1,))
    t1.start()
    time.sleep(0.5)
    t2 = threading.Thread(target = philosopher, args = (2,))
    t2.start()
    time.sleep(0.5)
    t3 = threading.Thread(target = philosopher, args = (3,))
    t3.start()
    time.sleep(0.5)
    t4 = threading.Thread(target = philosopher, args = (4,))
    t4.start()
    time.sleep(0.5)
    t5 = threading.Thread(target = philosopher, args = (5,))
    t5.start()
    
if __name__ == '__main__':
    main()
