# coding=utf-8
import os
import sys
import traceback
from builtins import str
from qgis.PyQt.QtCore import QDir, QObject, QSettings, Qt
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsProject, QgsVectorJoinInfo
from qgis.gui import QgsMessageBar

from veriso.base.utils.loadlayer import LoadLayer

try:
    _encoding = QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

from collections import OrderedDict
from veriso.modules.complexcheck_base import ComplexCheckBase


class ComplexCheck(ComplexCheckBase):
    names = OrderedDict()
    names['de'] = u'Grundlagelayer'

    def __init__(self, iface):
        super(ComplexCheck, self).__init__(iface)
        self.project_dir = None
        self.project_id = None

    def run(self):
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        self.project_dir = self.settings.value("project/projectdir")
        self.project_id = self.settings.value("project/id")

        locale = QSettings().value('locale/userLocale')[
                 0:2]  # this is for multilingual legends

        if locale == "fr":
            pass
        elif locale == "it":
            pass
        else:
            locale = "de"

        if not project_id:
            self.message_bar.pushCritical("Error",
                                          _translate("VeriSO_NPLSO_Bauzonenplan",
                                                     "project_id not set",
                                                     None)
                                          )
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_NPLSO_Bauzonenplan", "Grundlagelayer - Bauzonenplan", None)
            group += " (" + str(project_id) + ")"


            layer = {
                "type": "wms",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Hintergrundkarte schwarz-weiss (WMS)",
                                    None),
                "url": "https://geo.so.ch/wms?",
                "layers": "ch.so.agi.hintergrundkarte_sw",
                "format": "image/png", "crs": "EPSG:" + str(epsg),
                "group": group
            }
            vlayer = self.layer_loader.load(layer, True, True, False)


            layer = {
                "type": "wms",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Orthofoto RGB",
                                    None),
                "url": "https://geo.so.ch/wms?",
                "layers": "ch.so.agi.orthofoto_rgb",
                "format": "image/jpeg", "crs": "EPSG:" + str(epsg),
                "group": group
            }
            vlayer = self.layer_loader.load(layer, False, True, False)


        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()

