Install QtCreator via 
https://www.qt.io/download-qt-installer
# link to it from /usr/local/bin rather than add to PATH

# install c & opengl libraries for examples
> sudo dnf groupinstall "C Development Tools and Libraries"
> sudo dnf install mesa-libGL-devel

# make the examples directories writable (and backup)
# so they can be launched from the qtcreator ide

/opt/Qt> sudo cp -r Examples/ Examples_BAK
/opt/Qt> sudo chmod -R a+w Examples/
/opt/Qt/AdditionalLibraries/Qt/qt3d-6.0.1> sudo chmod -R a+w Examples/

# install Python bindings 
> pip install PyQt5
> pip install PySide2

# create a project folder 
/home/sdugaro/SRC> mkdir pyqt_ui_from_qtcreator

# use qtcreator to create a simple QMainWindow
File > New Project
Files And Classes = Qt | Qt Designer Form (ui file) [choose]
MainWindow = New Application [Next]

# You will get QtDesigner embedded in QtCreator
# drag in some labels and a push button
# select labels in the Object Inspector and RMB|Layout > horizontally
# RMB(MainWindow) | Layout > Vertically to set the centralwidget
# save -> mainwindow.ui

# This file can be 'loaded' into PyQt or PySide2 using their apis
# main_pyqt5.py: uic.loadUI("mainwindow.ui")
# main_pyside2.py: QUiLoader().load("mainwindow.ui")

# typically you would want to load from inside an existing
# widgets __init__ block. This is not supported in PySide2.
# you can however pass the window object returned by the
# QUiLoader into a module level function to configure it.

# I've always preferred to use the command line utility pyuic5 to 
# convert the .ui file to a MainWindow.py file. This file should
# not be edited, just imported and overwritten as the design changes
# via qtcreator/designer. PySide2 has an equivalent of this called
# pyside2-uic. The two are different and not interchangable.
# Use a code diff utility such as meld to compare them.

> pyuic5 mainwindow.ui -o MainWindow.py
> pyuic5 mainwindow.ui -o MainWindow2.py

# have a look at the resultant file to see the auto-generated
# ui class in the module we wish to import is prefixed with Ui_
# We can now use the QWidget api to load this instead of relying
# on a separate module to compile and load the ui at runtime.

# I prefer to use the __name__=='__main__' idom as in general
# this means these apps can be run as a main program, fed to 
# a python interpreter, and imported into other modules or by
# other applications such as Houdini however you prefer.
# Whats nice about this, is that you can run test of individual
# widget components in different files as standalones and then
# import them all into a main program.

# Ensuring the main program is in the PATH, has its execution 
# flag set and adding a 'shebang' to the top of its module 
# instructs *nix systems to use the specified interpreter when
# it is being run standalone. In our case we rely on the env
# command to locate it as the python interpreter can be 
# installed in different places on different machines while the
# env *nix program is always absolute and in the same place. 

> chmod a+x main.py
> ./main.py

# PyQt and PySide used to be worlds apart, but since qt.io
# took ownership of the opensource PySide, they have begun
# to become more similiar in use and robustness. PyQt was
# implemented by RiverBank Computing far before PySide so
# more of the underlying Qt libraries have been fleshed out.
# qt.io began calling PySide 'Qt for Python' and have aligned
# this with their qt releases as of Qt 6. This means going
# forward one would > pip install pyside6
