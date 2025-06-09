// Calculator.ice
module Demo {
    exception DivisionByZero {
        string reason;
    };

    interface Calculator {
        double sum(double op1, double op2);
        double sub(double op1, double op2);
        double mult(double op1, double op2);
        double div(double op1, double op2) throws DivisionByZero;
    };
};

