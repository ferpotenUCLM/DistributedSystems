# server.py
import Ice
import sys
Ice.loadSlice('Calculator.ice')
import Demo

class CalculatorI(Demo.Calculator):
    def sum(self, op1, op2, current=None):
        return op1 + op2

    def sub(self, op1, op2, current=None):
        return op1 - op2

    def mult(self, op1, op2, current=None):
        return op1 * op2

    def div(self, op1, op2, current=None):
        if op2 == 0.0:
            raise Demo.DivisionByZero(reason="Division by zero")
        return op1 / op2

class Server(Ice.Application):
    def run(self, argv):
        adapter = self.communicator().createObjectAdapterWithEndpoints(
            "CalculatorAdapter", "default -p 10000")
        adapter.add(CalculatorI(), self.communicator().stringToIdentity("calculator"))
        adapter.activate()
        print("Calculator service running...")
        self.communicator().waitForShutdown()
        return 0

if __name__ == "__main__":
    app = Server()
    sys.exit(app.main(sys.argv))