# coding=utf-8
import sys
import traceback
from builtins import str
from qgis.PyQt.QtCore import QObject, QSettings, Qt, QCoreApplication, QDir
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsProject, QgsVectorJoinInfo, QgsDataSourceURI
from qgis.gui import QgsMessageBar
from PyQt4.QtGui import QMessageBox


from PyQt4.QtSql import *


import os, time
import xlsxwriter as pycel
#from veriso.base.utils.qgeoapputils import QGeoAppUtils



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
                    "Error", _translate("VeriSO_PNF_Seltene_Objekte", "project_id not "
                                                         "set", None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_PNF_Seltene_Objekte", "Checklayer - Seltene Objekte",
                               None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Seltene_Objekte", "BB.BoFlaeche",
                                    None),
                "featuretype": "bodenbedeckung_boflaeche",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "bb/bb_bb_plan.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Seltene_Objekte", "EO.Einzelobjekt",
                                    None),
                "featuretype": "einzelobjekte_einzelobjekt",
                "geom": "", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group
            }
            eoeolayer = self.layer_loader.load(layer, False, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Seltene_Objekte", "EO.Flaechenelement",
                                    None),
                "featuretype": "einzelobjekte_flaechenelement",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_fl_bb_plan.qml"
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
                "title": _translate("VeriSO_PNF_Seltene_Objekte", "EO.Linienelement",
                                    None),
                "featuretype": "einzelobjekte_linienelement",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "eo/eo_li_bb_plan.qml"
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
                "title": _translate("VeriSO_PNF_Seltene_Objekte", "Li.Liegenschaft",
                                    None),
                "featuretype": "liegenschaften_liegenschaft",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "li/liegenschaft_ortho.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Seltene_Objekte", "BB.Boeschungsbauwerk",
                                    None),
                "featuretype": "t_boeschungbwerke",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "checks/checklayer_punkt.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_PNF_Seltene_Objekte", "EO.Brunnen",
                                    None),
                "featuretype": "t_brunnen",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "checks/checklayer_punkt.qml"
            }
            vlayer = self.layer_loader.load(layer, True, False)
            
            QApplication.restoreOverrideCursor() 
            
            # Export feature count in excel file.
            try:    
                        
                settings = QSettings("CatAIS", "VeriSO")
                module_name = settings.value("project/appmodule")
                provider = settings.value("project/provider")
                dbhost = settings.value("project/dbhost")
                db_port = settings.value("project/dbport")
                dbname = settings.value("project/dbname")
                dbschema = settings.value("project/dbschema")
                dbuser = settings.value("project/dbuser")
                dbpwd = settings.value("project/dbpwd")
                projectId = settings.value("project/id")
                project_dir = settings.value("project/projectdir")
                
                db = QSqlDatabase.addDatabase("QPSQL", "SelteneObjekte")
                db.setDatabaseName(dbname)
                db.setHostName(dbhost)
                db.setUserName(dbuser)
                db.setPassword(dbpwd)
                

                
                if  db.open() == False:
                    QMessageBox.critical(None,  "QGeoApp", QCoreApplication.translate("QGeoApp", "Could not open database:\n") + str(db.lastError().driverText()))            
                    return 

                
                filename = QDir.convertSeparators(QDir.cleanPath(os.path.join(project_dir, "seltene_objekte.xlsx")))
                
                # Create excel file.
                wb = pycel.Workbook(filename)
                #wb.country_code = 41
                
            
                style1 = wb.add_format({'bold':True});
                style2 = wb.add_format({'italic':True});
                
  
                # Bodenbedeckung            
                sql = "SELECT CASE WHEN anz IS NULL THEN 0 ELSE anz END, bb_art.itfcode as art, bb_art.ilicode as art_txt "
                sql += "FROM ("
                sql += "SELECT count(art) as anz, art_txt, art"
                sql += " FROM "+dbschema+".bodenbedeckung_boflaeche"
                sql += " WHERE art IN (7, 9, 19, 20, 21, 22, 30, 33, 35, 36, 37, 38, 39, 40)"
                sql += " GROUP BY art, art_txt"
                sql += ") bb"
                sql += " FULL JOIN "+dbschema+".bodenbedeckung_bbart bb_art ON bb_art.itfcode = bb.art"
                sql += " WHERE bb_art.itfcode IN (7, 9, 19, 20, 21, 22, 30, 33, 35, 36, 37, 38, 39, 40)"
                sql += " ORDER BY bb_art.itfcode;"
                
                
                

                query = db.exec_(sql)
                
            
                if query.isActive() == False:
                    QMessageBox.critical(None,  "QGeoApp", QCoreApplication.translate("QGeoApp", "Error occured while fetching data informations."))            
                    return 
                        
                ws = wb.add_worksheet(u'BB seltene Objekte')
                ws.paper_size_code = 8
                ws.print_centered_vert = False
                ws.print_centered_horz = False
                ws.top_margin = 1.0
                ws.left_margin = 1.0 
                ws.bottom_margin = 1.0
                ws.portrait = True
            
                
                ws.write(0, 0,  str("BB seltene Objekte: "), style1 )              
                ws.write(0, 1,  str(projectId))               
  
                ws.write(2, 0, str("Art"))
                ws.write(2, 1, str("Art-Text"))
                ws.write(2, 2, str("Anzahl"))

                i = 0
                
                record = query.record()
                anz_index=record.indexOf("anz") 
                art_index=record.indexOf("art")
                art_txt_index=record.indexOf("art_txt")

                while query.next():
                    anz = str(query.value(anz_index))
                    art = str(query.value(art_index))
                    art_txt = str(query.value(art_txt_index))
                    
                    ws.write(3+i, 0, art)
                    ws.write(3+i, 1, art_txt)
                    ws.write(3+i, 2, anz)
                    
                
                    i += 1

                
                # Einzelobjekte
                sql = "SELECT CASE WHEN anz IS NULL THEN 0 ELSE anz END, eo_art.itfcode as art, eo_art.ilicode as art_txt"
                sql += " FROM"
                sql += " ("
                sql += " SELECT count(art) as anz, art_txt, art"
                sql += " FROM "+dbschema+".einzelobjekte_einzelobjekt"
                sql += " WHERE art IN (9, 14, 15, 16, 17, 18, 23, 30, 31, 35, 36, 37, 38, 40, 42)"
                sql += " GROUP BY art, art_txt"
                sql += ") eo"
                sql += " FULL JOIN "+dbschema+".einzelobjekte_eoart eo_art ON eo_art.itfcode = eo.art"
                sql += " WHERE eo_art.itfcode IN (9, 14, 15, 16, 17, 18, 23, 30, 31, 35, 36, 37, 38, 40, 42)"
                sql += " ORDER BY eo_art.itfcode"


                query = db.exec_(sql)
                
            
                if query.isActive() == False:
                    QMessageBox.critical(None,  "QGeoApp", QCoreApplication.translate("QGeoApp", "Error occured while fetching data informations."))            
                    return 

                
                ws = wb.add_worksheet(u'EO seltene Objekte')
                ws.paper_size_code = 8
                ws.print_centered_vert = False
                ws.print_centered_horz = False
                ws.top_margin = 1.0
                ws.left_margin = 1.0 
                ws.bottom_margin = 1.0
                ws.portrait = True
                
            
                ws.write(0, 0,  str("EO seltene Objekte: "), style1)
                ws.write(0, 1,  projectId)        

                ws.write(2, 0, str("Art"))
                ws.write(2, 1, str("Art-Text"))
                ws.write(2, 2, str("Anzahl"))
                

                i = 0
                record = query.record()
                while query.next():
                    anz = str(query.value(record.indexOf("anz")))
                    art = str(query.value(record.indexOf("art")))
                    art_txt = str(query.value(record.indexOf("art_txt")))
                
                    ws.write(3+i, 0, art)
                    ws.write(3+i, 1, art_txt)
                    if int(anz) > 0:
                        ws.write(3+i, 2, anz, style1)
                    else:
                        ws.write(3+i, 2, anz)
                
                    i += 1
                    
                

                #file = QDir.convertSeparators(QDir.cleanPath(project_dir + os.sep + "seltene_objekte.xls"))
                try:
                    wb.close()
                    QMessageBox.information( None, "", QCoreApplication.translate("QGeoAppModule.PNF", "File written:\n") + filename)
                except IOError:
                    QMessageBox.warning( None, "", QCoreApplication.translate("QGeoAppModule.PNF", "File <b>not</b> written!<br>")+ filename)
                    return

                db.close()

                
    
            except:
                QMessageBox.critical(None,  "QGeoApp", QCoreApplication.translate("QGeoApp", "Error exporting data from database to excel."))   
                    

            
                       
            

        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()
