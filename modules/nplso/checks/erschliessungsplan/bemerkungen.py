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
    names['de'] = u'Bemerkungen'
    #names['fr'] = 'Parcelles'

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
                                          _translate("VeriSO_NPLSO_Erschliessungsplan",
                                                     "project_id not set",
                                                     None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_NPLSO_Erschliessungsplan", "Bemerkungen - Erschliessungsplan", None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Bemerkungen - Plan",
                                    None),
                "featuretype": "t_maengel_plan",
                "geom": "", "key": "t_id", "sql": "plan_txt='Erschliessungsplan'",
                "readonly": True, "group": group
            }
            lyr_plan = self.layer_loader.load(layer, True, True, False)

            layer = {
                "type": "postgres", "title": _translate("VeriSO_NPLSO_Erschliessungsplan",
                                                        "Bemerkungen - kommunaler Typ",
                                                        None),
                "featuretype": "t_maengel_komm_typ",
                "geom": "", "key": "t_id",
                "sql": "", "readonly": True, #gruppe = 'Bahn'
                "group": group
            }
            lyr_komm_typ = self.layer_loader.load(layer, True, True, False)

            layer = {
                "type": "postgres", "title": _translate("VeriSO_NPLSO_Erschliessungsplan",
                                                        "Bemerkungen (Punkte)",
                                                        None),
                "featuretype": "t_maengel_punkt",
                "geom": "the_geom", "key": "t_id",
                "sql": "plan='Erschliessungsplan'", "readonly": False,  # plan='Erschliessungsplan'
                "group": group, "style": "bemerkungen/bemerkungen_punkt.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)
            
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
                "type": "postgres", "title": _translate("VeriSO_NPLSO_Erschliessungsplan",
                                                        "Bemerkungen (Linien)",
                                                        None),
                "featuretype": "t_maengel_linie",
                "geom": "the_geom", "key": "t_id",
                "sql": "plan='Erschliessungsplan'", "readonly": False,
                "group": group, "style": "bemerkungen/bemerkungen_linie.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)
            
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

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Kontrolllayer",
                                    None),
                "featuretype": "t_grundnutzung_kontrolliert",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": False, "group": group,
                "style": "checks/t_grundnutzung_kontrolliert.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True, False)

            if vlayer <> False:
                self.iface.legendInterface().setLayerVisible(vlayer, True) 
                vlayer.setLayerName(u"Kontroll-Layer")
                #vlayer.saveDefaultStyle()            

                provider = vlayer.dataProvider()
                provider.attributeIndexes()
                t_id_idx = provider.fieldNameIndex("t_id")
                kontrolliert_idx = provider.fieldNameIndex("kontrolliert")

      
                vlayer.setEditorWidgetV2(0,"Hidden")
                vlayer.setEditorWidgetV2(1, "CheckBox")       
                 
                vlayer.setEditorWidgetV2Config(1, {'fieldEditable':"1", 'UncheckedState':'f','CheckedState':'t'})



        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()
