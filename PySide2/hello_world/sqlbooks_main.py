
import sys

from PySide2.QtCore import Qt
from PySide2.QtSql import QSqlQueryModel
from PySide2.QtWidgets import QTableView, QApplication

import sqlbooks_createDB
from sqlbooks_delegate import BookDelegate


"""
#include "bookwindow.h"
#include <QtWidgets>

int main(int argc, char * argv[])
{
        Q_INIT_RESOURCE(books);

        QApplication app(argc, argv);

        BookWindow win;
        win.show();

        return app.exec();
}
"""

if __name__ == "__main__":
    app = QApplication()
    app.setApplicationName("Setting a Window Title When we are just showing a Widget")

    # create the db from records initialized in sqlbooks_createDB module
    sqlbooks_createDB.init_db()

    model = QSqlQueryModel()
    #model.setQuery("select * from books")
    #model.setQuery("select * from authors")
    #model.setQuery("select * from genres")
    model.setQuery("select title, author, genre, year, rating from books")
    #NB: this model requires headers to be set individually
    #model.setHorizontalHeaderLabels(["Title", "Author ID", "GenreID", "Year", "Ratring"])
    model.setHeaderData(0, Qt.Horizontal, "Title")
    model.setHeaderData(1, Qt.Horizontal, "Author ID")
    model.setHeaderData(2, Qt.Horizontal, "Genre ID")
    model.setHeaderData(3, Qt.Horizontal, "Year")
    model.setHeaderData(4, Qt.Horizontal, "Rating")

    table_view = QTableView()
    table_view.setModel(model)
    table_view.setItemDelegate(BookDelegate())
    table_view.resize(800, 600)
    table_view.show()
    sys.exit(app.exec_())
