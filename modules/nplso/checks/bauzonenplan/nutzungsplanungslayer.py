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
    names['de'] = u'Nutzungsplanungslayer'

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
            group = _translate("VeriSO_NPLSO_Bauzonenplan", "Nutzungsplanungslayer - Bauzonenplan", None)
            group += " (" + str(project_id) + ")"


            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Grundnutzung",
                                    None),
                "featuretype": "t_nutzungsplanung_grundnutzung",
                "geom": "geometrie", "key": "t_id", "sql": "typ_code_kommunal::numeric < 1919",
                "readonly": True, "group": group,
                "style": "nutzungsplanungslayer_bauzone/t_grundnutzung.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)


            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Grundnutzung kommunal",
                                    None),
                "featuretype": "t_nutzungsplanung_grundnutzung",
                "geom": "geometrie", "key": "t_id", "sql": "typ_code_kommunal::numeric < 1919",
                "readonly": True, "group": group,
                "style": "nutzungsplanungslayer_bauzone/t_grundnutzung_kommunal.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "überlagernde Fläche",
                                    None),
                "featuretype": "t_nutzungsplanung_ueberlagernd_flaeche",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "nutzungsplanungslayer_bauzone/t_ueberlagernd_flaeche.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)


            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "überlagernde Fläche kommunal",
                                    None),
                "featuretype": "t_nutzungsplanung_ueberlagernd_flaeche",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "nutzungsplanungslayer_bauzone/t_ueberlagernd_flaeche_kommunal.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "überlagernde Linie",
                                    None),
                "featuretype": "t_nutzungsplanung_ueberlagernd_linie",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "nutzungsplanungslayer_bauzone/t_ueberlagernd_linie.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)


            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "überlagernde Linie kommunal",
                                    None),
                "featuretype": "t_nutzungsplanung_ueberlagernd_linie",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "nutzungsplanungslayer_bauzone/t_ueberlagernd_linie_kommunal.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "überlagernder Punkt",
                                    None),
                "featuretype": "t_nutzungsplanung_ueberlagernd_punkt",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "nutzungsplanungslayer_bauzone/t_ueberlagernd_punkt.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)


            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "überlagernder Punkt kommunal",
                                    None),
                "featuretype": "t_nutzungsplanung_ueberlagernd_punkt",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "nutzungsplanungslayer_bauzone/t_ueberlagernd_punkt_kommunal.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Nutzungsplanung Beschriftung",
                                    None),
                "featuretype": "t_nutzungsplanung_beschriftung",
                "geom": "pos", "key": "t_ili_tid", "sql": "",
                "readonly": True, "group": group,
                "style": "nutzungsplanungslayer_bauzone/t_grundnutzung_beschriftung.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "ausserhalb Bauzone",
                                    None),
                "featuretype": "t_ausserhalb_bauzone",
                "geom": "geometrie_ausserhalb_bauzone", "key": "bfs_gemeindenummer", "sql": "",
                "readonly": True, "group": group,
                "style": "nutzungsplanungslayer_bauzone/t_ausserhalb_bauzone.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Bauzonen Perimeter",
                                    None),
                "featuretype": "t_nutzungsplanung_grundnutzung_vereinigt",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "nutzungsplanungslayer_bauzone/t_nutzungsplanung_grundnutzung_vereinigt.qml"
            }
            bauzone = self.layer_loader.load(layer, True, True, False)


            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Dokument",
                                    None),
                "featuretype": "rechtsvorschrften_dokument",
                "geom": "", "key": "t_id", "sql": "",
                "readonly": True, "group": group
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            

      
            if bauzone:
                rect = bauzone.extent()
                self.iface.mapCanvas().setExtent(rect)
                self.iface.mapCanvas().refresh()

        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()

