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
    names['de'] = u'Referenzlayer'

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
            group = _translate("VeriSO_NPLSO_Bauzonenplan", "Referenzlayer - Bauzonenplan", None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Bewirtschaftungseinheiten mit Direktzahlungsgrösse",
                                    None),
                "params": {"dbhost": "geodb.verw.rootso.org", "dbport": 5432, "dbname": "sogis", "dbschema": "gelan"},
                "featuretype": "gelanx_so_bewe",
                "geom": "wkb_geometry", "key": "ogc_fid", "sql": "typ_name = 'Anerkannt nach LBV' OR typ_name = 'Betriebsgemeinschaft' OR typ_name='LBV ohne DZ'",
                "readonly": True, "group": group,
                "style": "referenzlayer_bauzone/gelan_bewirtschaftungseinheiten.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Gelan-Standorte",
                                    None),
                "params": {"dbhost": "geodb.verw.rootso.org", "dbport": 5432, "dbname": "sogis", "dbschema": "gelan"},
                "featuretype": "gelanx_so_stao_point",
                "geom": "wkb_geometry", "key": "ogc_fid", "sql": "betriebtyp = 'Anerkannt nach LBV' OR betriebtyp = 'Betriebsgemeinschaft' OR betriebtyp='LBV ohne DZ'",
                "readonly": True, "group": group,
                "style": "referenzlayer_bauzone/gelan_standorte.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)


            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Grundwasserschutzzonen und -areale",
                                    None),
                "params": {"dbhost": "geodb.verw.rootso.org", "dbport": 5432, "dbname": "sogis", "dbschema": "public"},
                "featuretype": "aww_gszoar",
                "geom": "wkb_geometry", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "referenzlayer_bauzone/grundwasserschutz.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Archäologische Fundstellen - Punktfundstellen",
                                    None),
                "params": {"dbhost": "geodb.verw.rootso.org", "dbport": 5432, "dbname": "sogis", "dbschema": "ada_adagis_a"},
                "featuretype": "punktfundstellen",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "referenzlayer_bauzone/archaeologische_fundstellen_punktfundstellen.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Archäologische Fundstellen - Flächenfundstellen",
                                    None),
                "params": {"dbhost": "geodb.verw.rootso.org", "dbport": 5432, "dbname": "sogis", "dbschema": "ada_adagis_a"},
                "featuretype": "flaechenfundstellen",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "referenzlayer_bauzone/archaeologische_fundstellen_flaechenfundstellen.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Grundnutzung Linie",
                                    None),
                "featuretype": "t_nutzungsplanung_grundnutzung",
                "geom": "geometrie", "key": "t_id", "sql": "typ_code_kommunal::numeric < 1919",
                "readonly": True, "group": group,
                "style": "referenzlayer_bauzone/t_grundnutzung.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Überlagernd Linie",
                                    None),
                "featuretype": "t_nutzungsplanung_ueberlagernd_linie",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "referenzlayer_bauzone/t_nutzungsplanung_ueberlagernd_linie.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Bauzonenplan", "Bauzone unbebaut (ARP)",
                                    None),
                "params": {"dbhost": "geodb.verw.rootso.org", "dbport": 5432, "dbname": "sogis", "dbschema": "digizone"},
                "featuretype": "bauzone_bebaut_unbebaut_v",
                "geom": "wkb_geometry", "key": "ogc_fid", "sql": "bebaut = 'f' and  flaeche >5",
                "readonly": True, "group": group,
                "style": "referenzlayer_bauzone/bauzone_unbebaut_arp.qml"
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

