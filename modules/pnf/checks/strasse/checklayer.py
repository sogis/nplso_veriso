# coding=utf-8
import sys
import traceback
from builtins import str
from qgis.PyQt.QtCore import QObject, QSettings, Qt
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
                    "Error", _translate("VeriSO_PNF_Strasse", "project_id not "
                                                         "set", None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_PNF_Strasse", "Checklayer - Strasse",
                               None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Strasse", "BB.BoFlaeche",
                                    None),
                "featuretype": "bodenbedeckung_boflaeche",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "bb/bb_strasse_bbplan.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Strasse", "EO.Einzelobjekt",
                                    None),
                "featuretype": "einzelobjekte_einzelobjekt",
                "geom": "", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group
            }
            eoeolayer = self.layer_loader.load(layer, False, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Strasse", "EO.Flaechenelement",
                                    None),
                "featuretype": "einzelobjekte_flaechenelement",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_fl_strasse_ortho.qml"
            }
            eoflayer = self.layer_loader.load(layer, True, False)

            if eoflayer <> False:
                self.iface.legendInterface().setLayerVisible(eoflayer, True)    
            
            if eoeolayer <> False and eoflayer <> False:
                joinLayerId = eoeolayer.id()
                for feature in eoeolayer.getFeatures():
						joinIdx=feature.fieldNameIndex("ogc_fid")

                for t_feature in eoflayer.getFeatures():
						targetIdx=t_feature.fieldNameIndex("flaechenelement_von")
 
                joinInfo = QgsVectorJoinInfo()
                joinInfo.joinFieldIndex = joinIdx
                joinInfo.joinFieldName = "ogc_fid"
                joinInfo.joinLayerId = joinLayerId
                joinInfo.targetFieldIndex = targetIdx
                joinInfo.targetFieldName = "flaechenelement_von"
                joinInfo.memoryCache = True
            
                eoflayer.addJoin(joinInfo)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Strasse", "EO.Linienelement",
                                    None),
                "featuretype": "einzelobjekte_linienelement",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_li_strasse_ortho.qml"
            }
            eolilayer = self.layer_loader.load(layer, True, False)
            
            if eolilayer <> False:
                self.iface.legendInterface().setLayerVisible(eolilayer, True)    

            if eoeolayer <> False and eolilayer <> False:
                joinLayerId = eoeolayer.id()
                joinProvider = eoeolayer.dataProvider()
                joinProvider.attributeIndexes()
                joinIdx = joinProvider.fieldNameIndex("ogc_fid")
            
                targetProvider = eolilayer.dataProvider()
                targetProvider.attributeIndexes()
                targetIdx = targetProvider.fieldNameIndex("linienelement_von")

                joinInfo = QgsVectorJoinInfo()
                joinInfo.joinFieldIndex = joinIdx
                joinInfo.joinFieldName = "ogc_fid"
                joinInfo.joinLayerId = joinLayerId
                joinInfo.targetFieldIndex = targetIdx
                joinInfo.targetFieldName = "linienelement_von"
                joinInfo.memoryCache = True
            
                eolilayer.addJoin(joinInfo)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Strasse", "LI.Liegenschaft",
                                    None),
                "featuretype": "liegenschaften_liegenschaft",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "li/liegenschaft_ortho.qml"
            }
            vlayer = self.layer_loader.load(layer, False, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Strasse", "Pfeiler < 0.25 m2",
                                    None),
                "featuretype": "t_pfeiler_50cm",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": False, "group": group,
                "style": "checks/checklayer_punkt.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Strasse", "BB.Strasse_Weg > 10000 m2",
                                    None),
                "featuretype": "t_str_flaeche_10000",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": False, "group": group,
                "style": "checks/checklayer_punkt.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Strasse", "EO.schmaler_Weg in TS 2",
                                    None),
                "featuretype": "t_schmaler_weg_ts2",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": False, "group": group,
                "style": "checks/checklayer_punkt.qml"
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
