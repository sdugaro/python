import os
import copy
from PySide2.QtSql import QSqlRelationalDelegate
from PySide2.QtWidgets import (QItemDelegate, QSpinBox, QStyledItemDelegate,
                               QStyle, QStyleOptionViewItem)
from PySide2.QtGui import QMouseEvent, QPixmap, QPalette, QImage
from PySide2.QtCore import QEvent, QSize, Qt, QUrl



"""
ReImplement a few functions:
ie paint stars to represent the rating for each book in the table
C++ Constructor: Initialize the QSqlRelationalDelegate and QPixMap instance

BookDelegate::BookDelegate(QObject *parent)
    : QSqlRelationalDelegate(parent), star(QPixmap(":images/star.png"))
    {
    }

void BookDelegate::paint(QPainter *painter, const QStyleOptionViewItem &option,
                           const QModelIndex &index) const
{
    if (index.column() != 5) {
        QStyleOptionViewItem opt = option;
        // Since we draw the grid ourselves:
        opt.rect.adjust(0, 0, -1, -1);
        QSqlRelationalDelegate::paint(painter, opt, index);
    } else {
        const QAbstractItemModel *model = index.model();
        QPalette::ColorGroup cg = (option.state & QStyle::State_Enabled) ?
            (option.state & QStyle::State_Active) ?
                        QPalette::Normal :
                        QPalette::Inactive :
                        QPalette::Disabled;

        if (option.state & QStyle::State_Selected)
            painter->fillRect(
                        option.rect,
                        option.palette.color(cg, QPalette::Highlight));

        int rating = model->data(index, Qt::DisplayRole).toInt();
        int width = star.width();
        int height = star.height();
        int x = option.rect.x();
        int y = option.rect.y() + (option.rect.height() / 2) - (height / 2);
        for (int i = 0; i < rating; ++i) {
            painter->drawPixmap(x, y, star);
            x += width;
        }
        // Since we draw the grid ourselves:
        drawFocus(painter, option, option.rect.adjusted(0, 0, -1, -1));
    }

    QPen pen = painter->pen();
    painter->setPen(option.palette.color(QPalette::Mid));
    painter->drawLine(option.rect.bottomLeft(), option.rect.bottomRight());
    painter->drawLine(option.rect.topRight(), option.rect.bottomRight());
    painter->setPen(pen);
}

QSize BookDelegate::sizeHint(const QStyleOptionViewItem &option,
                                 const QModelIndex &index) const
{
    if (index.column() == 5)
        return QSize(5 * star.width(), star.height()) + QSize(1, 1);
    // Since we draw the grid ourselves:
    return QSqlRelationalDelegate::sizeHint(option, index) + QSize(1, 1);
}

bool BookDelegate::editorEvent(QEvent *event, QAbstractItemModel *model,
                               const QStyleOptionViewItem &option,
                               const QModelIndex &index)
{
    if (index.column() != 5)
        return QSqlRelationalDelegate::editorEvent(event, model, option, index);

    if (event->type() == QEvent::MouseButtonPress) {
        QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);
        int stars = qBound(0, int(0.7 + qreal(mouseEvent->pos().x()
            - option.rect.x()) / star.width()), 5);
        model->setData(index, QVariant(stars));
        // So that the selection can change:
        return false;
    }

    return true;
}

QWidget *BookDelegate::createEditor(QWidget *parent,
                                    const QStyleOptionViewItem &option,
                                    const QModelIndex &index) const
{
    if (index.column() != 4)
        return QSqlRelationalDelegate::createEditor(parent, option, index);

    // For editing the year, return a spinbox with a range from -1000 to 2100.
    QSpinBox *sb = new QSpinBox(parent);
    sb->setFrame(false);
    sb->setMaximum(2100);
    sb->setMinimum(-1000);

    return sb;
}

"""


class BookDelegate(QSqlRelationalDelegate):
    """Books delegate to rate the books"""

    def __init__(self, parent=None):
        QSqlRelationalDelegate.__init__(self, parent)
        #print(os.path.dirname(__file__))
        star_png = os.path.dirname(__file__) + "/images/star.png"
        self.star = QPixmap(star_png)


    def paint(self, painter, option, index):
        """ Paint the items in the table.

            If the item referred to by <index> is a StarRating, we
            handle the painting ourselves. For the other items, we
            let the base class handle the painting as usual.

            In a polished application, we'd use a better check than
            the column number to find out if we needed to paint the
            stars, but it works for the purposes of this example.
        """
        if index.column() != 4:
            # Since we draw the grid ourselves:
            opt = copy.copy(option)
            opt.rect = option.rect.adjusted(0, 0, -1, -1)
            QSqlRelationalDelegate.paint(self, painter, opt, index)
        else:
            model = index.model()
            if option.state & QStyle.State_Enabled:
                if option.state & QStyle.State_Active:
                    color_group = QPalette.Normal
                else:
                    color_group = QPalette.Inactive
            else:
                color_group = QPalette.Disabled

            if option.state & QStyle.State_Selected:
                painter.fillRect(option.rect,
                                 option.palette.color(color_group, QPalette.Highlight))

            rating = model.data(index, Qt.DisplayRole)
            width = self.star.width()
            height = self.star.height()
            x = option.rect.x()
            y = option.rect.y() + (option.rect.height() / 2) - (height / 2)
            for i in range(rating):
                painter.drawPixmap(x, y, self.star)
                x += width

            # Since we draw the grid ourselves:
            self.drawFocus(painter, option, option.rect.adjusted(0, 0, -1, -1))

        pen = painter.pen()
        painter.setPen(option.palette.color(QPalette.Mid))
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
        painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
        painter.setPen(pen)

    def sizeHint(self, option, index):
        """ Returns the size needed to display the item in a QSize object. """
        if index.column() == 5:
            size_hint = QSize(5 * self.star.width(), self.star.height()) + QSize(1, 1)
            return size_hint
        # Since we draw the grid ourselves:
        return QSqlRelationalDelegate.sizeHint(self, option, index) + QSize(1, 1)

    def editorEvent(self, event, model, option, index):
        if index.column() != 4:
            return False

        if event.type() == QEvent.MouseButtonPress:
            mouse_pos = event.pos()
            new_stars = int(0.7 + (mouse_pos.x() - option.rect.x()) / self.star.width())
            stars = max(0, min(new_stars, 5))
            model.setData(index, stars)
            # So that the selection can change
            return False

        return True

    def createEditor(self, parent, option, index):
        print(index.column())
        if index.column() != 4:
            return QSqlRelationalDelegate.createEditor(self, parent, option, index)

        # For editing the year, return a spinbox with a range from -1000 to 2100.
        spinbox = QSpinBox(parent)
        spinbox.setFrame(False)
        spinbox.setMaximum(2100)
        spinbox.setMinimum(-1000)
        return spinbox

