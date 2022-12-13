from Pyro4 import expose
from os import stat
import random
from heapq import merge

class Solver:

    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        n = self.read_input()
        step = n / len(self.workers)
        mapped = []
        lastElementI = len(self.workers) - 1

        for i in range(0, lastElementI):
            mapped.append(self.workers[i].mymap(i * step, i * step + step))
        mapped.append(self.workers[lastElementI].mymap(lastElementI * step, n))
        reduced = self.myreduce(mapped)
        self.write_output(reduced)


    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    @staticmethod
    def power(x, y, p):

        # Initialize result
        res = 1;

        # Update x if it is more than or
        # equal to p
        x = x % p;
        while (y > 0):

            # If y is odd, multiply
            # x with result
            if (y & 1):
                res = (res * x) % p;

            # y must be even now
            y = y >> 1;  # y = y/2
            x = (x * x) % p;

        return res;
    
    @staticmethod
    def miillerTest(d, n):

        # Pick a random number in [2..n-2]
        # Corner cases make sure that n > 4
        a = 2 + random.randint(1, n - 4);

        # Compute a^d % n
        x = Solver.power(a, d, n);

        if (x == 1 or x == n - 1):
            return True;

        # Keep squaring x while one
        # of the following doesn't
        # happen
        # (i) d does not reach n-1
        # (ii) (x^2) % n is not 1
        # (iii) (x^2) % n is not n-1
        while (d != n - 1):
            x = (x * x) % n;
            d *= 2;

            if (x == 1):
                return False;
            if (x == n - 1):
                return True;

        # Return composite
        return False;

    @staticmethod
    def isPrime(n, k):

        # Corner cases
        if (n <= 1 or n == 4):
            return False;
        if (n <= 3):
            return True;

        # Find r such that n =
        # 2^d * r + 1 for some r >= 1
        d = n - 1;
        while (d % 2 == 0):
            d //= 2;

        # Iterate given number of 'k' times
        for i in range(k):
            if Solver.miillerTest(d, n) == False:
                return False;

        return True;
    
    @staticmethod
    @expose
    def mymap(a, b):
        res_arr = []
        for n in range(a,b):
            if (Solver.isPrime(n, 50)):
                res_arr.append(n)
        return res_arr
 
    @staticmethod
    def myreduce(mapped):
        result = []
        wnum = len(mapped)
        result = mapped[0].value
        for i in range(1, wnum):
            result = list(merge(result, list(mapped[i].value)))
        return result
    

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        primalSum = 0
        for a in output:
            primalSum = primalSum + 1
        f.write(str(primalSum))
        f.close()
