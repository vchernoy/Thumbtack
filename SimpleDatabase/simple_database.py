# Author: Viacheslav CHernoy
# Email: vchernoy@gmail.com
# 
# The solution of Problem 3: Simple Database
# See http://www.thumbtack.com/challenges


class SimpleDB:
    def __init__(self):
        self._var_transactions = {}
        self._database = [{}]
        self._cur_transaction = 0

    # checks consistency of self._database
    # for debugging purposes only.
    def check(self):
        assert(self._cur_transaction >= 0)
        assert(self._cur_transaction == len(self._database) - 1)
        if self._cur_transaction == 0:
            assert(len(self._var_transactions) == 0)
        else:
            for (name, transactions) in self._var_transactions.items():
                transactions = self._var_transactions[name]
                for i in xrange(len(transactions)):
                    transaction = transactions[i]
                    assert(transaction > (transactions[i-1] if i > 0 else 0))
                    assert(transaction <= self._cur_transaction)

            for transaction in xrange(1, self._cur_transaction+1):
                for name in self._database[transaction]:
                    assert(transaction in self._var_transactions[name])

    # Time = O(1).
    def begin(self):
        self._database.append({})
        self._cur_transaction += 1
        assert(self._cur_transaction == len(self._database) - 1)

    # Time = O(the number of variables that were changed in the transaction).
    def rollback(self):
        valid = self._cur_transaction > 0
        if valid:
            for name in self._database[self._cur_transaction]:
                transactions = self._var_transactions[name]
                assert(transactions[-1] == self._cur_transaction)
                transactions.pop()  
                if not transactions:
                    del self._var_transactions[name]

            self._database.pop()
            self._cur_transaction -= 1 
            assert(self._cur_transaction == len(self._database) - 1)

        return valid

    # Time = O(the number of variables that were set/unset in all the transactions).
    def commit(self):
        for (name, transactions) in self._var_transactions.items():
            transaction = transactions[-1]
            assert(transaction > 0)
            val = self._database[transaction].get(name, None)
            if val == None:
                self._database[0].pop(name, None)
            else:
                self._database[0][name] = val
                
            del self._var_transactions[name]

        del self._database[1:]
        self._cur_transaction = 0

    # Time = O(1).
    def get(self, name):
        return self._database[self._var_transactions.get(name, [0])[-1]].get(name, None)

    # Time = O(1).
    def set(self, name, val):
        if self._cur_transaction > 0:
            transactions = self._var_transactions.get(name, [])
            prev_transaction = 0                if not transactions else \
                               transactions[-1] if transactions[-1] != self._cur_transaction else \
                               transactions[-2] if len(transactions) >= 2 else \
                               0

            if self._database[prev_transaction].get(name, None) == val:
                self._database[self._cur_transaction].pop(name, None)
                if transactions and (transactions[-1] == self._cur_transaction):
                    transactions.pop()
                    if not transactions:
                        del self._var_transactions[name]

            else:
                if not transactions:
                    self._var_transactions[name] = [self._cur_transaction]
                elif transactions[-1] != self._cur_transaction:
                    transactions.append(self._cur_transaction)

                self._database[self._cur_transaction][name] = val

        elif val != None:
            self._database[self._cur_transaction][name] = val
        else:
            self._database[self._cur_transaction].pop(name, None)


    # Time = O(1).
    def unset(self, name):
        self.set(name, None)


def main():
    db = SimpleDB()
    s = raw_input()
    while s != "END":
        #print s
        db.check()
        
        if s == "BEGIN":
            db.begin()
        elif s == "ROLLBACK":
            if not db.rollback():
                print "INVALID ROLLBACK"

        elif s == "COMMIT":
            db.commit()
        elif s.startswith("GET"):
            _, name = s.split()
            val = db.get(name)
            print val if val != None else "NULL"
        elif s.startswith("SET"):
            _, name, val = s.split()
            db.set(name, val)
        elif s.startswith("UNSET"):
            _, name = s.split()
            db.unset(name)
        else:
            print "UNKNOWN COMMAND"
            assert(False)

        s = raw_input()

if __name__ == '__main__':
    main()

