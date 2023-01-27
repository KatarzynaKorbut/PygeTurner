import logging

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView


class SheetViewer(QGraphicsView):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sheet_scene = QGraphicsScene(self)
        self.sheet_pixmap_item = QGraphicsPixmapItem()
        self.sheet_scene.addItem(self.sheet_pixmap_item)
        self.setScene(self.sheet_scene)
        self.setFrameShape(QFrame.Shape.NoFrame)

    def load(self, pixmap: QPixmap):
        self.setStyleSheet("")
        self.sheet_pixmap_item.setPixmap(pixmap)
        rect = pixmap.rect()
        logging.debug("Sheet image size: %s", rect)
        self.setSceneRect(rect)

        viewrect = self.viewport().rect()
        scenerect = self.transform().mapRect(rect)
        factor = 0.9 * viewrect.width() / scenerect.width()
        self.scale(factor, factor)
