

def get_var_value(identifier):
    return identifier.partition(",")[2]

def get_bool_operator(token_name):
    if token_name == "MENOR":
        return "<"
    elif token_name == "MAYOR":
        return ">"

class Quadruples:
    """
    Quadruples generator from intercode
    """


    def __init__(self, filename):
        self.filename = filename
        self.intercode = None
        self.quadruple = ""
        self.inner_vars = 0;

    def assignment(self, tokenizer, current):
        self.quadruple = "%s (=,%s,%s)\n" % (self.quadruple,tokenizer[2], get_var_value(tokenizer[1]) )


    def if_conditional(self, tokenizer, current):
        operador = get_bool_operator(tokenizer[2])
        self.inner_vars = self.inner_vars + 1
        self.quadruple = "%s(%s,%s,%s,T%d)\n"  % ( self.quadruple, operador, get_var_value(tokenizer[1]),tokenizer[3],self.inner_vars)
        self.quadruple = "%s(IF,T%d,_,GOTO[%d])\n"  % ( self.quadruple, self.inner_vars, current + 2)
        self.inner_quadruples("FIN_COND",current+2)

    def while_loop(self, tokenizer, current):
        operador = get_bool_operator(tokenizer[2])
        self.inner_vars = self.inner_vars + 1
        self.quadruple = "%s(%s,%s,%s,T%d)\n"  % ( self.quadruple, operador, get_var_value(tokenizer[1]),tokenizer[3],self.inner_vars)
        self.quadruple = "%s(IF,T%d,_,GOTO[%d])\n"  % ( self.quadruple, self.inner_vars, current + 2)
        self.inner_quadruples("FIN_MIENTRAS",current+2)


    def inner_quadruples(self, delimiter, current):
        token = ""
        while(token != delimiter):
            tokenizer = self.intercode.readline().split()
            token = tokenizer[0]
            if token == "ASIGNACION":
                self.assignment(tokenizer,current + 1)
            elif token == "MIENTRAS":
                self.while_loop(tokenizer,current + 1)
            elif token == "COND_IF":
                self.if_conditional(tokenizer,current + 1)

    def start_quadruples(self):
        self.intercode = open(self.filename, "r")
        self.intercode.readline()
        self.quadruple = "%s (_,_,_INICIO)\n" % self.quadruple
        self.inner_quadruples("FIN",2)
        self.quadruple = "%s (_,_,_FIN)\n" % self.quadruple
        self.intercode.close()




quad = Quadruples("intermedio.txt")
quad.start_quadruples()
print quad.quadruple
