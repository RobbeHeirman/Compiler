Naam: Robbe Heirman
Rollnr: 0122834

Bevat de oplossing voor de tussentijdse evaluatie van het vak compilers.

Dependencies:
- Java interpreter (antlr calls om lexer/parser base te genereren)
- Graphviz om .dot files om te zetten naar png -> visualitatie AST
- Antlr 4 python bindings (4.7 gebruikt).


Bevat:
 C_files -> alles voorbeeld & test .C files
 Grammars -> bevat mijn grammatica van small C
 Source -> alle source code

 antlr.jar is de antlr Java .jar gebruikt om lexer/parser ter genereren.
 build.py runt antlr.jar en zet de generated files op de corecte plaats.
 c2llvm.py genereert llvm code.


 Hoe te gebruiken:
 1) run de build file. Deze gebruikt de meegeleverde .jar file om alle generated files op zijn plek te zetten.
 2) run c2llvm.png -> neemt 1 of 2 argumenten
        1 argument : moet de string test zijn. runs test files.
        2 argumenten: 1 c_input_file_name, 2 output_llvm_name

3) Het test argument resulteert in een test_results directory met daarin subdirectories voor iedere C file in de C
   file directory. Deze directories bevatten een .dot en .png file voor de AST een .llvm file met llvm code en een .log
   file met eventuele error messages.

4) Met 2 input argementen zal een een output_llvm_name document gegenereert worden (indien geen syntax/semantic errors)
   er wordt ook een AST.dot en . png bestand gegeneeerd met de AST in.

implementatie tot nu toe:
Grammar: - Done

Semantische analyse: - DOne
 llvm code generatie:
                    - er wordt correcte llvm code gegenereerd met declaraties, Expressies en functies.

 mips code generatie:
                    - /
