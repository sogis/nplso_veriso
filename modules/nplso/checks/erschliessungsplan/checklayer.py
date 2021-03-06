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
                    "Error", _translate("VeriSO_NPLSO_Erschliessungsplan", "project_id not "
                                                         "set", None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_NPLSO_Erschliessungsplan", "Checklayer - Erschliessungsplan",
                               None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "private Strasse nicht plausibel",
                                    None),
                "featuretype": "t_private_strasse_nicht_plausibel",
                "geom": "geometrie", "key": "id", "sql": "",
                "readonly": True, "group": group,
                "style": "checks/ES_private_stasse_nicht_plausibel.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Baulinie geht durch Gebäude",
                                    None),
                "featuretype": "t_baulinie_durch_gebaeude",
                "geom": "geometrie", "key": "id", "sql": "",
                "readonly": True, "group": group,
                "style": "checks/ES_Baulinie_geht_durch_gebaeude.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Baulinie Strasse nicht plausibel",
                                    None),
                "featuretype": "t_baulinie_strasse_nicht_plausibel",
                "geom": "geometrie", "key": "id", "sql": "",
                "readonly": True, "group": group,
                "style": "checks/ES_Baulinie_strasse_nicht_plausibel.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Gewässerbaulinie nicht plausibel",
                                    None),
                "featuretype": "t_gewaesserbaulinie_nicht_plausibel",
                "geom": "geometrie", "key": "id", "sql": "",
                "readonly": True, "group": group,
                "style": "checks/ES_gewaesserbaulinie_nicht_plausibel.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)


            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Dokument ohne Verknüpfung",
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
