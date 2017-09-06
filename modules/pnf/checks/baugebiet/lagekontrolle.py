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
    names['de'] = u'Lagekontrolle'
    #names['fr'] = "Vue d'ensemble"

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
                                          _translate("VeriSO_PNF_Baugebiet",
                                                     "project_id not set",
                                                     None)
                                          )
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_PNF_Baugebiet", "Lagekontrolle - Bebautes Gebiet", None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "wms",
                "title": _translate("VeriSO_PNF_Baugebiet", "Orthofoto CIR",
                                    None),
                "url": "http://geoweb.so.ch/wms/sogis_orthofoto.wms",
                "layers": "Ortho_CIR_SO",
                "format": "image/png", "crs": "EPSG:" + str(epsg),
                "group": group
            }

            vlayer = self.layer_loader.load(layer, False, True)            
            
            layer = {
                "type": "wms",
                "title": _translate("VeriSO_PNF_Baugebiet", "Orthofoto RGB",
                                    None),
                "url": "http://geoweb.so.ch/wms/sogis_orthofoto.wms",
                "layers": "Ortho_SO",
                "format": "image/png", "crs": "EPSG:" + str(epsg),
                "group": group
            }

            vlayer = self.layer_loader.load(layer, True, True)
            
            layer = {
                "type": "wms",
                "title": _translate("VeriSO_PNF_Baugebiet", "GEWISSO",
                                    None),
                "url": "http://geoweb.so.ch/wms/sogis_gewaesser.wms",
                "layers": "gewaesser",
                "format": "image/png", 
                "crs": "EPSG:" + str(epsg),
                "group": group
            }
            vlayer = self.layer_loader.load(layer, True, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Baugebiet", "Gemeindegrenze",
                                    None),
                "featuretype": "gemeindegrenzen_gemeindegrenze",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "gemeindegrenze/gemgre_strichliert.qml"
            }
            gemgrelayer = self.layer_loader.load(layer, True, False)

            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Baugebiet", "BB.BoFlaeche",
                                    None),
                "featuretype": "bodenbedeckung_boflaeche",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "bb/bb_baugebiet_ortho.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Baugebiet", "EO.Einzelobjekt",
                                    None),
                "featuretype": "einzelobjekte_einzelobjekt",
                "geom": "", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                #"style": "bodenbedeckung/projboflaeche_color.qml"
            }
            eoeolayer = self.layer_loader.load(layer, False, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Baugebiet", "EO.Flaechenelement",
                                    None),
                "featuretype": "einzelobjekte_flaechenelement",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_fl_baugebiet_ortho.qml"
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
                "title": _translate("VeriSO_PNF_Baugebiet", "EO.Linienelement",
                                    None),
                "featuretype": "einzelobjekte_linienelement",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_li_baugebiet_ortho.qml"
            }
            eolilayer = self.layer_loader.load(layer, True, False)
            
            if eolilayer <> False:
                self.iface.legendInterface().setLayerVisible(eolilayer, True)    

            if eoeolayer <> False and eolilayer <> False:
                joinLayerId = eoeolayer.id()
                joinProvider = eoeolayer.dataProvider()
                joinProvider.attributeIndexes()
                joinIdx = joinProvider.fieldNameIndex("tid")
            
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
                "title": _translate("VeriSO_PNF_Baugebiet", "EO.Punktelement",
                                    None),
                "featuretype": "einzelobjekte_punktelement",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_pk_andere.qml"
            }
            eopklayer = self.layer_loader.load(layer, True, False)
            
            if eopklayer <> False:
                self.iface.legendInterface().setLayerVisible(eopklayer, True)    

            if eoeolayer <> False and eopklayer <> False:
                joinLayerId = eoeolayer.id()
                joinProvider = eoeolayer.dataProvider()
                joinProvider.attributeIndexes()
                joinIdx = joinProvider.fieldNameIndex("ogc_fid")
            
                targetProvider = eopklayer.dataProvider()
                targetProvider.attributeIndexes()
                targetIdx = targetProvider.fieldNameIndex("punktelement_von")

                joinInfo = QgsVectorJoinInfo()
                joinInfo.joinFieldIndex = joinIdx
                joinInfo.joinFieldName = "ogc_fid"
                joinInfo.joinLayerId = joinLayerId
                joinInfo.targetFieldIndex = targetIdx
                joinInfo.targetFieldName = "punktelement_von"
                joinInfo.memoryCache = True
            
                eopklayer.addJoin(joinInfo)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Baugebiet", "LI.Liegenschaft",
                                    None),
                "featuretype": "liegenschaften_liegenschaft",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "li/liegenschaft_ortho.qml"
            }
            vlayer = self.layer_loader.load(layer, False, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Baugebiet", "BB.Objektname",
                                    None),
                "featuretype": "v_bb_objektnamen",
                "geom": "pos", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "bb/bb_objektnamen.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Baugebiet", "EO.Objektname",
                                    None),
                "featuretype": "v_eo_objektnamen",
                "geom": "pos", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_objektnamen.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Baugebiet", "Reservoir (AfU)",
                                    None),
                "params": {"dbhost": "localhost", "dbport": 5432, "dbname": "grundlagen", "dbschema": "sogis"},
                "featuretype": "reservoir_afu",
                "geom": "wkb_geometry", "key": "gid", "sql": "",
                "readonly": True, "group": group,
                "style": "sogis/reservoir_afu.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Baugebiet", "Kontrollraster (Planeinteilung)",
                                    None),
                "featuretype": "t_kontrollraster_plan_bebaut",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": False, "group": group,
                "style": "kontrollraster/kontrollraster.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            if vlayer <> False:            
                self.iface.legendInterface().setLayerVisible(vlayer, False)        
                provider = vlayer.dataProvider()
                provider.attributeIndexes()
                ogc_fid_idx = provider.fieldNameIndex("ogc_fid")
                vlayer.setEditorWidgetV2(0,"Hidden")
            
                plannummer_idx = provider.fieldNameIndex("plannummer")
                vlayer.setEditorWidgetV2(2,"Hidden")            
            
                kontrolliert_idx = provider.fieldNameIndex("kontrolliert")
                vlayer.setEditorWidgetV2(1,"CheckBox")
                vlayer.setEditorWidgetV2Config(1, {'fieldEditable':"1", 'UncheckedState':'f','CheckedState':'t'})
                
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Baugebiet", "Kontrollraster",
                                    None),
                "featuretype": "t_kontrollraster_strasse_500",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": False, "group": group,
                "style": "kontrollraster/kontrollraster.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            if vlayer <> False:            
                self.iface.legendInterface().setLayerVisible(vlayer, True)        
                provider = vlayer.dataProvider()
                provider.attributeIndexes()
                ogc_fid_idx = provider.fieldNameIndex("ogc_fid")
                vlayer.setEditorWidgetV2(0,"Hidden")
            
                kontrolliert_idx = provider.fieldNameIndex("kontrolliert")
                vlayer.setEditorWidgetV2(1,"CheckBox")
                vlayer.setEditorWidgetV2Config(1, {'fieldEditable':"1", 'UncheckedState':'f','CheckedState':'t'})

 
            if gemgrelayer:
                rect = gemgrelayer.extent()
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
