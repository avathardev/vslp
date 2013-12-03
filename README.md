
Very Simple Language Parser
====

Descripción del Lenguaje
Define en una sola sintaxis elementos de HTML y CSS
Detecta errores de token inválidos, errores de sintaxis y uso invalido de objetos no definidos

Descripción del compilador/intérprete
Lenguajes y utilerías especiales utilizadas para el desarrollo del proyecto
    Python 2.7 con los modulos de expresiones regulares
    No se utilizan librerías externas.

Descripción de análisis léxico
Patrones de construcción
    INISET   =  \#set
    NAMETAG  =  \:
    SET      =  set
    STYLE    =  style
    EQUALS   =  \=
    ENDSET   =  \#endset
    LPAR     =  \(
    RPAR     =  \)
    COMMA    =  \,
    APOS     =  \'
    DOTCOMMA =  \;
    INITEMP  =  \#template
    ENDTEMP  =  \#endtemplate
    ININEST  =  \{\%
    ENDNEST  =  \%\}
    FOR      =  for
    SELE     =  \#|\.\w+
    NUM      =  [1-9][0-9]*
    ID       =  (-|\w)+
    LKEY     =  \{
    RKEY     =  \}

Descripción de análisis sintáctico
    Gramática Formal
    A -> S C
    S -> C
    S -> #set : id D
    D -> set id = E D
    D -> style = id Y D
    D -> #endset
    E -> set ( id J
    Y -> style ( ' selector ' J
    J -> , id : id J
    J -> ) ;
    C -> #template : id T
    T -> B #endtemplate
    T -> #endtemplate
    B -> {% id I
    B -> for ( num , num ) { B }
    I -> B %}
    I -> %}


Descripción de análisis semántico y generación de código intermedio

Luego del análisis sintáctico, pasamos a código intermedio, en donde se lleva un control de las variables declaradas
Se diseñaron cuadruplos para la representacion intermedia del código de entrada


Descripción del ejecutor
Lenguajes y utilerías especiales usadas para la generación del ejecutor
Manejo de Memoria / Tabla de símbolos
Pruebas de Funcionamiento


