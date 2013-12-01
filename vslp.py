# -*- coding: utf-8 -*-
"""
VS.LP

Very Simple Language Parser
for my Compilers course at Tec de Monterrey, Campus Querétaro

coded by avathar

follow me: @avatharBot
"""

"""
so far, it needs space between tokens in input file
gonna work on that later
may add a feature in the future to expand it's functionality
"""

import re
import sys

class Lexer:
    """
    Lexer class with automatons to accept tokens for grammar using regex
    Pass filename to read tokens for input
    Can add more tokens as a dictionary using add_tokens()
    Can read input from file or stdin (coming soon)
    """

    # token dict with regular expression definitions
    tokens = {}

    def __init__(self,tokens_filename):
        """
        Setting up lexical analysis
        TODO:
            -> use re.compile to check regex syntax
            -> store re objects instead of token : regex pair
        """
        tokens_file = open(tokens_filename, 'r')
        for line in tokens_file:
            token_regex = line.split()
            self.tokens[token_regex[0]] = token_regex[1]
        tokens_file.close()

    def add_tokens(self,more_tokens):
        for key in more_tokens:
            self.tokens[key] = more_tokens[key]

    def show_tokens(self):
        for token in self.tokens:
            print "token name: %s regex: %s" % (token, self.tokens[token])

    def do_lexer_with_file(self, filename):
        input_file = open(filename,'r')
        line_count = 0
        for line in input_file:
            line_count = line_count + 1
            for word in line.split():
                for token in self.tokens:
                    # shame on me, bad way to do this
                    match = False
                    if(re.match(self.tokens[token],word)):
                        match = True
                        print "token %s \t->  %s " % (token,word)
                        break
                # should have an Error Class, maybe later
                if not match:
                    print " ---> Lexical Error on line %d: Undefined token for [ %s ] " % (line_count,word)
        input_file.close()

class Parser:
    def __init__(self, filename):
        """
        Parser object to read grammar and make an syntax parser
        """
        self.grammar = []
        #hard coded for project, don't panic
        self.parsing_table = [
            # 1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27
            [ 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [ 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1,  3, -1, -1,  4,  5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1,  6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1,  7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  8, -1, -1,  9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, 11, -1, 11, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 13, -1, 14, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 15, -1, 15, -1, -1, -1, 16, -1]
        ]
        grammar_file = open("grammar.txt")
        for line in grammar_file:
            # separate rules by arrow symbol
            grammar_rule = line.partition("->")
            # stripping some chars from input file
            self.grammar.append({grammar_rule[0] : grammar_rule[2].strip()})
        grammar_file.close()

    def show_grammar(self):
        """
        so we can take a look at parser grammar
        very straightforward
        """
        print "   Grammar"
        for rule in self.grammar:
            print rule

    def do_parse_from_file(self, filename):
        """
        A modified LL(1) algorithm for string parsing with this language grammar
        Using list index references to match grammar rules and parsing table
        """
        input_file = open(filename)
        for line in input_file:
            print line
        input_file.close()


lex = Lexer('tokens.txt')

#lex.show_tokens()

lex.do_lexer_with_file('input.txt')

parser = Parser("grammar.txt")

parser.show_grammar()


parser.do_parse_from_file("input.txt")
