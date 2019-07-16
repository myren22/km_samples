For java projects, add one of the project dirs in this folder.

In each projct dir you will find:
        PROJECTDIR/
            src/
                projectname/            <--package names must be all lowercase. 
                    aJavaFile.java


If using eclipse, upon creating a project using PROJECTDIR, it will
create some setting files[.classpath, .project] and a bin dir.
The bin dir will contain a .class of each java file, and is necessary to 
run the related java file it is a copy of.

=========
=    Remaking bin package files from terminal, using src.
=========   
    If your packages get renamed, or you lose the bin folder and
eclipse doesn't remake, you can remake the classes in bin using the 
java compiler from terminal

Reference file struct:
        PROJECTDIR/
            src/
                projectname/                <--possible extra dir layers depending on package structure
                    aJavaFile.java
            bin/
                projectname/
                    aJavaFile.class
    
First, verify/look over the description of the terminal commands
>javac [-options] <source files>
>java  [-options] class

If all checks are done, then compile/build[same thing in java]. 
PROCJECTDIR>javac    -d bin     src/*.java

... at this point bin should now have all packages and classes.
Now you will want to test running the class files. This may fail if the
java files have errors ir mismatching package names.

PROCJECTDIR/bin>>java projectname.aJavaFile


... If it printed and ran then everything is good.