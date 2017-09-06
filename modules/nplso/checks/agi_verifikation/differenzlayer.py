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

from collections import OrderedDict
from veriso.modules.complexcheck_base import ComplexCheckBase


class ComplexCheck(ComplexCheckBase):
    names = OrderedDict()
    names['de'] = u'Differenzlayer'

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
                    "Error", _translate("VeriSO_PNF_AGI_Verifikation", "project_id not "
                                                         "set", None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_PNF_AGI_Verifikation", "Differenzlayer",
                               None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_AGI_Verifikation", "BB vorher NICHT in nachher",
                                    None),
                "featuretype": "t_bb_before_except_after",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "bb/bb_before_except_after.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_AGI_Verifikation", "BB nachher NICHT in vorher",
                                    None),
                "featuretype": "t_bb_after_except_before",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "bb/bb_after_except_before.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_AGI_Verifikation", "EO.Flaeche vorher NICHT in nachher",
                                    None),
                "featuretype": "t_eo_fl_before_except_after",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_fl_before_except_after.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_AGI_Verifikation", "EO.Flaeche nachher NICHT in vorher",
                                    None),
                "featuretype": "t_eo_fl_after_except_before",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_fl_after_except_before.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_AGI_Verifikation", "EO.Linie vorher NICHT in nachher",
                                    None),
                "featuretype": "t_eo_li_before_except_after",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_li_before_except_after.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_AGI_Verifikation", "EO.Linie nachher NICHT in vorher",
                                    None),
                "featuretype": "t_eo_li_after_except_before",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_li_after_except_before.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_AGI_Verifikation", "EO.Punkt vorher NICHT in nachher",
                                    None),
                "featuretype": "t_eo_pt_before_except_after",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_pt_before_except_after.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_AGI_Verifikation", "EO.Punkt nachher NICHT in vorher",
                                    None),
                "featuretype": "t_eo_pt_after_except_before",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_pt_after_except_before.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
                   
                       
            

        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()

