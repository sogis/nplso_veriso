# coding=utf-8
import sys
import traceback
from builtins import str
from qgis.PyQt.QtCore import QObject, QSettings
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsProject, QgsVectorLayer
from qgis.gui import QgsMessageBar

from veriso.base.utils.loadlayer import LoadLayer
from veriso.base.utils.utils import tr


class LoadDefects(QObject):
    def __init__(self, iface, module, tr_tag):

        # TODO remove debugging trace
        # import pydevd
        # pydevd.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)

        QObject.__init__(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.canvas = self.iface.mapCanvas()

        self.root = QgsProject.instance().layerTreeRoot()
        self.layer_loader = LoadLayer(self.iface)
        self.settings = QSettings("CatAIS", "VeriSO")
        self.project_id = None
        self.epsg = None

        self.tr_tag = tr_tag  # "VeriSO_V+D_Defects" or "VeriSO_EE_Defects"

    def run(self):
        try:
            self.project_id = self.settings.value("project/id")
            self.epsg = self.settings.value("project/epsg")

            group = tr(u"Bemerkungen", self.tr_tag, None)
            group += " (" + str(self.project_id) + ")"

            layer = {
                "type": "postgres",
                "title": tr("VeriSO_NPLSO_Bauzonenplan", "Bemerkungen - Plan",
                                    None),
                "featuretype": "t_maengel_plan",
                "geom": "", "key": "t_id", "sql": "",
                "readonly": True, "group": group
            }
            lyr_plan = self.layer_loader.load(layer, True, True, False)

            layer = {
                "type": "postgres", "title": tr("VeriSO_NPLSO_Bauzonenplan",
                                                        "Bemerkungen - kommunaler Typ",
                                                        None),
                "featuretype": "t_maengel_komm_typ",
                "geom": "", "key": "t_id",
                "sql": "", "readonly": True, 
                "group": group
            }
            lyr_komm_typ = self.layer_loader.load(layer, True, True, False)

            layer = {
                "type": "postgres",
                "title": tr(u"Bemerkungen (Punkte)", self.tr_tag, None),
                "featuretype": "t_maengel_punkt", "geom": "the_geom",
                "key": "t_id", "readonly": False, "sql": "",
                "group": group, "style": "bemerkungen/bemerkungen_punkt.qml"
            }

            vlayer = self.layer_loader.load(layer)

            if vlayer <> False:
                self.iface.legendInterface().setLayerVisible(vlayer, True) 
                vlayer.setLayerName(u"Bemerkungen (Punkte)")
                #vlayer.saveDefaultStyle()            

                provider = vlayer.dataProvider()
                provider.attributeIndexes()
                ogc_fid_idx = provider.fieldNameIndex("t_id")
                plan_idx = provider.fieldNameIndex("plan")
                kommunaler_typ_idx = provider.fieldNameIndex("kommunaler_typ")
                bemerkung_idx = provider.fieldNameIndex("bemerkung")
                datum_idx = provider.fieldNameIndex("datum")  

                vlayer.addAttributeAlias(plan_idx, "Plan:")
                vlayer.addAttributeAlias(kommunaler_typ_idx, "kommunaler Typ:")
                vlayer.addAttributeAlias(bemerkung_idx, "Bemerkung:")
      
                vlayer.setEditorWidgetV2(0,"Hidden")
                vlayer.setEditorWidgetV2(1, "ValueRelation")
                vlayer.setEditorWidgetV2(2, "ValueRelation")
                vlayer.setEditorWidgetV2(3, "TextEdit")            
                vlayer.setEditorWidgetV2(4, "Hidden")        
                 
                vlayer.setEditorWidgetV2Config(1, {'Layer':lyr_plan.id(), 'Key':'plan_txt', 'Value':'plan_txt', 'OrderByValue':"1", 'AllowNull':"0", 'AllowMulti':'0'})
                vlayer.setEditorWidgetV2Config(2, {'Layer':lyr_komm_typ.id(), 'Key':'kommunaler_typ', 'Value':'kommunaler_typ', 'OrderByValue':"1", 'AllowNull':"0", 'AllowMulti':'0' })
                vlayer.setEditorWidgetV2Config(3, {'IsMultiline':"1", 'fieldEditable':"1", 'UseHtml':"0", 'labelOnTop':"0"})

            layer = {
                "type": "postgres",
                "title": tr(u"Bemerkungen (Linien)", self.tr_tag, None),
                "featuretype": "t_maengel_linie", "geom": "the_geom",
                "key": "t_id", "readonly": False, "sql": "",
                "group": group, "style": "global_qml/maengel/maengel_linie.qml"
            }

            vlayer = self.layer_loader.load(layer)

            if vlayer <> False:
                self.iface.legendInterface().setLayerVisible(vlayer, True) 
                vlayer.setLayerName(u"Bemerkungen (Linie)")
                #vlayer.saveDefaultStyle()            

                provider = vlayer.dataProvider()
                provider.attributeIndexes()
                ogc_fid_idx = provider.fieldNameIndex("t_id")
                plan_idx = provider.fieldNameIndex("plan")
                kommunaler_typ_idx = provider.fieldNameIndex("kommunaler_typ")
                bemerkung_idx = provider.fieldNameIndex("bemerkung")
                datum_idx = provider.fieldNameIndex("datum")  

                vlayer.addAttributeAlias(plan_idx, "Plan:")
                vlayer.addAttributeAlias(kommunaler_typ_idx, "kommunaler Typ:")
                vlayer.addAttributeAlias(bemerkung_idx, "Bemerkung:")
      
                vlayer.setEditorWidgetV2(0,"Hidden")
                vlayer.setEditorWidgetV2(1, "ValueRelation")
                vlayer.setEditorWidgetV2(2, "ValueRelation")
                vlayer.setEditorWidgetV2(3, "TextEdit")            
                vlayer.setEditorWidgetV2(4, "Hidden")        
                 
                vlayer.setEditorWidgetV2Config(1, {'Layer':lyr_plan.id(), 'Key':'plan_txt', 'Value':'plan_txt', 'OrderByValue':"1", 'AllowNull':"0", 'AllowMulti':'0'})
                vlayer.setEditorWidgetV2Config(2, {'Layer':lyr_komm_typ.id(), 'Key':'kommunaler_typ', 'Value':'kommunaler_typ', 'OrderByValue':"1", 'AllowNull':"0", 'AllowMulti':'0' })
                vlayer.setEditorWidgetV2Config(3, {'IsMultiline':"1", 'fieldEditable':"1", 'UseHtml':"0", 'labelOnTop':"0"})


        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()
