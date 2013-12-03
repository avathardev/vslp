
DELIMITERS = r'\s'


#Lexema (nombre, regexp)
TOKENS = (
    ('INISET',  r'\#set'),
    ('NAMETAG', r'\:'),
    ('EQUALS',  r'\='),
    ('SET',     r'set'),
    ('STYLE',   r'style'),
    ('ENDSET',  r'\#endset'),
    ('LPAR',    r'\('),
    ('RPAR',    r'\)'),
    ('COMMA',   r'\,'),
    ('APOS',    r'\''),
    ('DOTCOMMA',r'\;'),
    ('INITEMP', r'\#template'),
    ('ENDTEMP', r'\#endtemplate'),
    ('ININEST', r'\{\%'),
    ('ENDNEST', r'\%\}'),
    ('FOR',     r'for'),
    ('ID',      r'(-|[a-zA-Z])+'),
    ('NUM',     r'[1-9][0-9]*'),
    ('SELE',    r'(\#|\.)?\w+'),
    ('LKEY',    r'\{'),
    ('RKEY',    r'\}'),
)

#r'/\*([^*]|[\s]|(\*+([^*/]|[\s])))*\*+/'


TOKENS_WITH_DELIMITERS = (
#    ('STRING', r'a', r'a'),
    ('COMMENT_BLOCK', r'/\*([^*]|[\s]|(\*+([^/]|[\s])))*\*+/', r'/\*([^*]|[\s]|(\*+([^/]|[\s])))*\*+/'),
    ('COMMENT_BLOCK', r'/\*([^*]|[\s]|(\*+([^/]|[\s])))*\*+/', r'/\*([^*]|[\s]|(\*+([^/]|[\s])))*'),
    ('COMMENT_BLOCK', r'/\*([^*]|[\s]|(\*+([^/]|[\s])))*\*+/', r'/\*'),
#    ('COMMENT_NEW_LINE', r'a', r'a'),

)




GRAMMAR = (
    ('A', 'S C'),
    ('S', 'C'),
    ('S', 'iniset nametag id D'),
    ('D', 'set id equals E D'),
    ('D', 'style id equals Y D'),
    ('D', 'endset'),
    ('E', 'set lpar id J'),
    ('Y', 'style lpar apos sele apos J'),
    ('J', 'comma id nametag id J'),
    ('J', 'rpar dotcomma'),
    ('C', 'initemp nametag id T'),
    ('T', 'B endtemp'),
    ('T', 'endtemp'),
    ('B', 'ininest id I'),
    ('B', 'for lpar num comma num rpar lkey B rkey'),
    ('I', 'B endnest'),
    ('I', 'endnest'),
)


