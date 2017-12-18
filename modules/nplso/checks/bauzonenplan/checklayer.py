# coding=utf-8
import sys
import traceback
from builtins import str
from qgis.PyQt.QtCore import QObject, QSettings, Qt
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsProject
from qgis.gui import QgsMessageBar

from veriso.base.utils.loadlayer import LoadLayer

try:
    _encoding = QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

from veriso.modules.complexcheck_base import ComplexCheckBase


class ComplexCheck(ComplexCheckBase):
    name = 'Checklayer'

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
            self.message_bar.pushCritical(
                    "Error", _translate("VeriSO_NPLSO_Bauzonenplan", "project_id not "
                                                         "set", None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_NPLSO_Bauzonenplan", "Checklayer - Bauzonenplan",
                               None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Stützpunkte nicht identisch zur Liegenschaft",
                                    None),
                "featuretype": "t_stuetzpunkte_nicht_identisch_zur_liegenschaft",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "checks/checklayer_punkt.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Beschriftung nicht io",
                                    None),
                "featuretype": "t_beschriftung_nicht_io",
                "geom": "pos", "key": "t_ili_tid", "sql": "",
                "readonly": True, "group": group,
                "style": "checks/checklayer_punkt.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Rechtsstatus nicht 'in Kraft'",
                                    None),
                "featuretype": "t_rechtsstatus_nicht_inkraft",
                "geom": "geometrie", "key": "t_ili_tid", "sql": "",
                "readonly": True, "group": group,
                "style": "checks/checklayer_punkt.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Perimeter ohne Dokument",
                                    None),
                "featuretype": "t_perimeter_ohne_plandokument",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "checks/checklayer_punkt.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)


            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Perimeter mit Dokument",
                                    None),
                "featuretype": "t_perimeter_mit_plandokument",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "checks/checklayer_punkt.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)


            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Dokument ohne Verknüpfung",
                                    None),
                "featuretype": "t_dokument_ohne_verknuepfung",
                "geom": "", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "checks/checklayer_punkt.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)



        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()
