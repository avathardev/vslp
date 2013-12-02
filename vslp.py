# -*- coding: utf-8 -*-
"""
VS.LP

Very Simple Language Parser
for my Compilers course at Tec de Monterrey, Campus Querétaro

coded by avathar & grevych

Lexical class for analex
Paser class for anasin
Quadruples for intermediate code
Generator for output code

follow us: @avatharBot @grevych
"""


import sys
import re
import util

from collections import namedtuple

class Lexical:
    def __init__(self, filenames, debugger):
        self.source = None #sources
        self.filenames = filenames
        try:
            self.source = open(self.filenames) # or "a+", whatever you need
        except IOError:
            print "Could not open file!"
            return
            #mandar llamar instancia de error y terminar

        self.line = 0
        self.status = ""
        self.flags = {}
        self.debugger = debugger
        self.terminals = []
        self.nonterminals = []
        self.parsing_table = []
        TokenWithDelimiter = namedtuple('Token', ('name', 'regexp', 'regexp_at_start', ))
        Token = namedtuple('Token', ('name', 'regexp', ))

        self.tokens = [Token(
                            token[0],
                            re.compile(token[1])) for token in util.TOKENS]

        self.tokens_with_del = [TokenWithDelimiter(
                                    token[0],
                                    re.compile(token[1]),
                                    re.compile(token[2])) for token in util.TOKENS_WITH_DELIMITERS]
        self.t = []
        self.d = []

    def get_grammar():
        return self.__grammar

    def run(self):
        with self.source:
            buffer_str = ""
            buffer_str_del = ""
            is_token_with_del = False

            for char in iter(lambda: self.source.read(1), ''):
                if not char.isspace():
                    self.line = (self.line, self.line + 1)[char.count('\n')]
                    buffer_str += char
                    continue
                if is_token_with_del:
                    buffer_str_del += buffer_str + char
                    for token in self.tokens_with_del:
                        match = token.regexp.match(buffer_str_del)
                        if match:
                            print match.group()
                            if token.name == 'ID' or token.name == 'NUM':
                                self.d.append(token.name + "," + match.group())
                            else:
                                self.d.append(token.name)
                            self.t.append(token.name.lower())
                            buffer_str = buffer_str_del.replace(match.group(), '', 1)
                            self.source.seek(- buffer_str.__len__(), 1)
                            buffer_str_del = buffer_str = ""
                            is_token_with_del = False
                            break
                else:
                    for token in self.tokens_with_del:
                        match = token.regexp_at_start.match(buffer_str)
                        if match:
                            print match.group() + " NUEVO EN DELIM"
                            is_token_with_del = True
                            buffer_str_del = buffer_str
                            buffer_str = ""
                            break
                        is_token_with_del = False
                    if not is_token_with_del:
                        while buffer_str:
                            has_match = False
                            for token in self.tokens:
                                match = token.regexp.match(buffer_str)
                                if match:
                                    if token.name == 'ID' or token.name == 'NUM':
                                        self.d.append(token.name + "," + match.group())
                                    else:
                                        self.d.append(token.name)
                                    self.t.append(token.name.lower())
                                    buffer_str = buffer_str.replace(match.group(), '', 1)
                                    print match.group() + "\t\t NUEVO" + buffer_str
                                    has_match = True
                                    break
                            if not has_match:
                                print "NO ACEPTADO"
                                return
            if is_token_with_del:
                buffer_str_del += buffer_str + char
                for token in self.tokens_with_del:
                    match = token.regexp.match(buffer_str_del)
                    if match:
                        print match.group()
                        if token.name == 'ID' or token.name == 'NUM':
                            self.d.append(token.name + "," + match.group())
                        else:
                            self.d.append(token.name)
                        self.t.append(token.name.lower())
                        buffer_str_del = buffer_str = ""
                        is_token_with_del = False
                        break
            else:
                for token in self.tokens_with_del:
                    match = token.regexp_at_start.match(buffer_str)
                    if match:
                        print match.group() + " NUEVO EN DELIM"
                        is_token_with_del = True
                        buffer_str_del = buffer_str
                        buffer_str = ""
                        break
                    is_token_with_del = False
                if not is_token_with_del:
                    while buffer_str:
                        has_match = False
                        for token in self.tokens:
                            match = token.regexp.match(buffer_str)
                            if match:
                                if token.name == 'ID' or token.name == 'NUM':
                                    self.d.append(token.name + "," + match.group())
                                else:
                                    self.d.append(token.name)
                                self.t.append(token.name.lower())
                                buffer_str = buffer_str.replace(match.group(), '', 1)
                                print match.group() + " NUEVO" + buffer_str
                                has_match = True
                                break
                        if not has_match:
                            print "NO ACEPTADO"
                            return
            if buffer_str:
                print buffer_str
                print "NO ACEPTADO"
                return
        print self.t
        print self.d

    def anasin(self):

        if not util.GRAMMAR.__len__():
            print "Error en gramática -> inexistente"
            return

        self.__grammar = [{production[0]: production[1]} for production in util.GRAMMAR]
        self.__next = {}
        self.__first = {}
        self.terminals = []
        self.nonterminals = []
        self.parsing_table = []


        for production in util.GRAMMAR:
            self.__get_first(production[0])
            self.__get_next(production[0])

        self.get_terminals()
        self.get_nonterminals()
        self.__set_parsing_table()


        #print 'GRAMATICA -> ', self.__grammar
        #print 'PRIMEROS -> ', self.__first
        #print 'SIGUIENTES -> ', self.__next
        #print 'TERMINALES -> ', self.terminals
        #print 'NO TERMINALES -> ', self.nonterminals
        #print '\n\n\nTABLA ->'
        for i in  self.parsing_table:
            print i



    def get_terminals(self):
        for production in util.GRAMMAR:
            for element in production[1].split():
                if element.islower() and element not in self.terminals and element.find('epsilon'):
                    self.terminals.append(element)

        self.terminals.append('$')



    def get_nonterminals(self):
        for production in util.GRAMMAR:
            if production[0] not in self.nonterminals:
                self.nonterminals.append(production[0])



    def __set_parsing_table(self):
        for nonterminal in self.nonterminals:
            self.parsing_table.append([-1 for terminal in self.terminals])

        index_table = 0

        for production in util.GRAMMAR:
            x = self.nonterminals.index(production[0])
            element = production[1].split()[0]

            if not element.find('epsilon'):
                y = [self.terminals.index(elem) for elem in self.__next[production[0]] if elem != 'epsilon'] #diferente de epsilon

                for index in y:
                    if self.parsing_table[x][index] == -1:
                        self.parsing_table[x][index] =  'epsilon' #'epsilon'
                    elif self.parsing_table[x][y] != index_table:
                        print "Error en tabla de parsing__ %d" % (index_table, )
                        return

            elif element in self.terminals:
                y = self.terminals.index(element)
                if self.parsing_table[x][y] == -1:
                    self.parsing_table[x][y] =  index_table
                elif self.parsing_table[x][y] != index_table:
                    print "Error en tabla de parsing_ %d %d %d %s" % (index_table, x, y, element)
                    return

            else:
                y = [self.terminals.index(elem) for elem in self.__first[element] if elem != 'epsilon'] #diferente de epsilon

                for index in y:
                    if self.parsing_table[x][index] == -1:
                        self.parsing_table[x][index] = index_table
                    elif self.parsing_table[x][y] != index_table:
                        print "Error en tabla de parsing %d" % (index_table, )
                        return

            index_table = index_table + 1



    def __get_first(self, key):
        if self.__first.has_key(key):
            return self.__first[key]

        self.__first[key] = []

        for production in self.__grammar:
            if production.has_key(key):
                elements = production[key].split()
                if elements[0] != key:
                    if elements[0].islower():
                        self.__first[key].append(elements[0])
                    else:
                        epsilons = 0
                        is_epsilon = False

                        for element in elements:
                            for first in self.__get_first(element):
                                if not first.find('epsilon'):
                                    epsilons = epsilons + 1
                                    is_epsilon = True
                                    continue

                                if not first in self.__first[key]:
                                    self.__first[key].append(first)

                            if not is_epsilon:
                                break

                            is_epsilon = False

                        if epsilons == elements.__len__():
                            if not 'epsilon' in self.__first[key]:
                                self.__first[key].append('epsilon')

        return self.__first[key]



    def __get_next(self, key):
        if self.__next.has_key(key):
            return self.__next[key]

        self.__next[key] = []

        if key == util.GRAMMAR[0][0] and '$' not in self.__next[key]:
            self.__next[key].append('$')

        for production in self.__grammar:
            elements = production.values()[0].split()
            index = 0

            for element in elements:
                if element.__eq__(key):
                    if index == elements.__len__() - 1:
                        if production.keys()[0] != key:
                            for next in self.__get_next(production.keys()[0]):
                                if next not in self.__next[key]:
                                    self.__next[key].append(next)
                    else:
                        if elements[index + 1].islower():
                            self.__next[key].append(elements[index + 1])
                        else:
                            is_epsilon = False
                            for next in self.__get_first(elements[index + 1]):
                                if not next.find('epsilon'):
                                    is_epsilon = True
                                    continue
                                if next not in self.__next[key]:
                                    self.__next[key].append(next)

                            if is_epsilon:
                                for next in self.__get_next(production.keys()[0]):
                                    if next not in self.__next[key]:
                                        self.__next[key].append(next)

                index = index + 1

        return self.__next[key]


class Parser:
    def __init__(self, lex):
        """
        Parser object to read grammar and make an syntax parser
        """

        self.lex = lex
        self.grammar = [production[1].split() for production in util.GRAMMAR]
        self.intercode = lex.d
        self.did_pass_syntax_analysis = False
        self.string = []
        self.terminal = lex.terminals
        self.non_terminal = lex.nonterminals
        self.non_terminal.extend(self.terminal)
        #hard coded for project, don't panic
        self.parsing_table = lex.parsing_table

    def show_grammar(self):
        """
        so we can take a look at parser grammar
        very straightforward
        """
        print " --> Grammar <-- "
        for rule in self.grammar:
            print rule

    def start_parser(self):

        """
        A modified LL(1) algorithm for string parsing with this language grammar
        Using list indexes references to match grammar rules and parsing table
        """
        # starting symbol
        stack = ["A"]
        # non_terminal list representing user input
        self.string = lex.t
        self.string.reverse()
        while len(self.string) > 0:
            print stack
            # getting input and stack top elements
            token = self.string.pop()
            token_index = self.terminal.index(token)

            top = stack.pop( )
            top_index = self.non_terminal.index(top)

            # accept token , build intermediate code and continue analysis
            if top == token:
                self.build_intercode(token)
                continue
            # return token to input string
            if top != token:
                self.string.append(token)
            # get grammar rule from parsing table
            try:
                production = self.parsing_table[top_index][token_index]
            except IndexError:
                print " --> Syntax error: expecting ->  %s  " % top
                exit( )
            # report error and exit
            if production == -1:
                print " --> Syntax error on grammar rule -> %s " % self.grammar[top_index]
                exit( )
            # add grammar rule elements to stack
            else:
                rule = self.grammar[production]
                rule.reverse( )
                for r in rule: stack.append(r)
                rule.reverse()
        print "\nAnalisis Sintactico: Cadena Aceptada\n"
        self.did_pass_syntax_analysis = True

    def build_intercode(self,token):
        pass

    def show_intercode(self):
        print self.intercode

def get_var_value(identifier):
    return identifier.partition(",")[2]


class Quadruples:
    """
    Quadruples generator from intermediate code
    """
    def __init__(self, intercode):
        self.intercode = intercode
        self.intercode.reverse()
        self.quadruple = ""
        self.inner_vars = 0;
        self.line = 0

    def add_quadruple(self, one = "_", two = "_", three = "_", four = "_"):
        self.quadruple = "%s (%s, %s, %s, %s)\n" % (self.quadruple, one, two, three, four)
        self.line = self.line + 1
        print self.quadruple


    def inner_quadruples(self, delimiter, current):
        token = self.intercode.pop()
        while(token != delimiter):
            if token == "SET" or token == "STYLE":
                next = self.intercode.pop()
                if next == "RPAR":
                    self.constructor(token)
                else:
                    self.assignment(token, next)
            elif token == "COMMA":
                    self.comma()
            elif token == "LPAR":
                # consume symbol
                dot_comma = self.intercode.pop()
            elif token == "ININEST":
                self.inner_quadruples("ENDNEST",current + 1)
            elif token == "FOR":
                self.for_loop(token)
            else:
                self.id(token)
            token = self.intercode.pop()

    def id(self, token):
        self.add_quadruple("{% %}",get_var_value(token),four="#template")

    def for_loop(self, token):
        inipar = self.intercode.pop()
        num1 = self.intercode.pop()
        comma = self.intercode.pop()
        num2 = self.intercode.pop()
        endpar = self.intercode.pop()
        inikey = self.intercode.pop()
        self.add_quadruple("for",num1,num2,token)
        self.inner_quadruples("LKEY", 1)

    def comma(self):
        attr = self.intercode.pop()
        two_dots = self.intercode.pop()
        value = self.intercode.pop()
        self.add_quadruple(":", value, four=attr)

    def constructor(self, obj_type):
        name = self.intercode.pop()
        self.add_quadruple("()",name,four=obj_type)

    def assignment(self, obj_type, var_name):
        # consuming equals symbol
        self.intercode.pop()
        self.add_quadruple("=",get_var_value(var_name),four=obj_type)

    def start_quadruples(self):
        token = self.intercode.pop()
        # full input
        if token == "INISET":
            self.add_quadruple(four = "#set")
            nametag = self.intercode.pop()
            name = get_var_value(self.intercode.pop())
            self.add_quadruple(":", name, four = "#set" )
            self.inner_quadruples("ENDSET",3)
            self.add_quadruple(four = "#endset")
            # full input so we have template section
            token = self.intercode.pop()
            self.add_quadruple(four = "#template" )
            nametag = self.intercode.pop()
            name = get_var_value(self.intercode.pop())
            self.add_quadruple(":", name, four = "#set" )
            self.inner_quadruples("ENDTEMP",3)
            self.add_quadruple(four = "#endtemplate")
        else:
            self.add_quadruple(four="#template")
            nametag = self.intercode.pop()
            name = get_var_value(self.intercode.pop())
            self.add_quadruple(":",name,four="#template")
            self.inner_quadruples("ENDTEMP",3)
            self.add_quadruple(four="#endtemplate")


class Generator:
    """docstring for Generator"""
    def __init__(self, arg):
        self.arg = arg

# Lexical object
lex = Lexical("prueba", None)
lex.run()
lex.anasin()

# Parser object
parser = Parser( lex )
parser.show_grammar()
print " --> Start parsing <-- "
parser.start_parser()

# Quadruples object

quad = Quadruples( parser.intercode )
quad.start_quadruples()
print quad.quadruple
