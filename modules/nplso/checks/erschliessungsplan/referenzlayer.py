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
                                          _translate("VeriSO_NPLSO_Erschliessungsplan",
                                                     "project_id not set",
                                                     None)
                                          )
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_NPLSO_Erschliessungsplan", "Referenzlayer - Erschliessungsplan", None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Bewirtschaftungseinheiten mit Direktzahlungsgrösse",
                                    None),
                "params": {"dbhost": "geodb.verw.rootso.org", "dbport": 5432, "dbname": "sogis", "dbschema": "gelan"},
                "featuretype": "gelanx_so_bewe",
                "geom": "wkb_geometry", "key": "ogc_fid", "sql": "typ_name = 'Anerkannt nach LBV' OR typ_name = 'Betriebsgemeinschaft' OR typ_name='LBV ohne DZ'",
                "readonly": True, "group": group,
                "style": "referenzlayer_erschliessung/gelan_bewirtschaftungseinheiten.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Gelan-Standorte",
                                    None),
                "params": {"dbhost": "geodb.verw.rootso.org", "dbport": 5432, "dbname": "sogis", "dbschema": "gelan"},
                "featuretype": "gelanx_so_stao_point",
                "geom": "wkb_geometry", "key": "ogc_fid", "sql": "betriebtyp = 'Anerkannt nach LBV' OR betriebtyp = 'Betriebsgemeinschaft' OR betriebtyp='LBV ohne DZ'",
                "readonly": True, "group": group,
                "style": "referenzlayer_erschliessung/gelan_standorte.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)


            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Grundwasserschutzzonen und -areale",
                                    None),
                "params": {"dbhost": "geodb.verw.rootso.org", "dbport": 5432, "dbname": "sogis", "dbschema": "public"},
                "featuretype": "aww_gszoar",
                "geom": "wkb_geometry", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "referenzlayer_erschliessung/grundwasserschutz.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Archäologische Fundstellen - Punktfundstellen",
                                    None),
                "params": {"dbhost": "geodb.verw.rootso.org", "dbport": 5432, "dbname": "sogis", "dbschema": "ada_adagis_a"},
                "featuretype": "punktfundstellen",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "referenzlayer_erschliessung/archaeologische_fundstellen_punktfundstellen.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Archäologische Fundstellen - Flächenfundstellen",
                                    None),
                "params": {"dbhost": "geodb.verw.rootso.org", "dbport": 5432, "dbname": "sogis", "dbschema": "ada_adagis_a"},
                "featuretype": "flaechenfundstellen",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "referenzlayer_erschliessung/archaeologische_fundstellen_flaechenfundstellen.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "historische Verkehrswege",
                                    None),
                "params": {"dbhost": "geodb.verw.rootso.org", "dbport": 5432, "dbname": "sogis", "dbschema": "public"},
                "featuretype": "arp_ivsso_line",
                "geom": "wkb_geometry", "key": "ogc_fid", "sql": "archive=0",
                "readonly": True, "group": group,
                "style": "referenzlayer_erschliessung/historische_verkehrswege.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Grundnutzung Linie",
                                    None),
                "featuretype": "t_nutzungsplanung_grundnutzung",
                "geom": "geometrie", "key": "t_id", "sql": "typ_code_kommunal::numeric > 1919",
                "readonly": True, "group": group,
                "style": "referenzlayer_erschliessung/t_grundnutzung_linie.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Erschliessung Flaechenobjekt",
                                    None),
                "featuretype": "t_erschliessung_flaechenobjekt",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "referenzlayer_erschliessung/t_erschliessung_flaechenobjekt.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Erschliessung Linienobjekt",
                                    None),
                "featuretype": "t_erschliessung_linienobjekt",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "referenzlayer_erschliessung/t_erschliessung_linienobjekt.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Erschliessung Punktobjekt",
                                    None),
                "featuretype": "t_erschliessung_punktobjekt",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "referenzlayer_erschliessung/t_erschliessung_punktobjekt.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "90000 Grundstücke aggregiert",
                                    None),
                "featuretype": "t_grundstuecke_90000_aggregiert",
                "geom": "geometrie", "key": "id", "sql": "",
                "readonly": True, "group": group,
                "style": "referenzlayer_erschliessung/t_grundstuecke_90000_aggregiert.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "AV Gewaesser gepuffert 4m",
                                    None),
                "featuretype": "t_av_gewaesser_gepuffert",
                "geom": "geometrie", "key": "id", "sql": "",
                "readonly": True, "group": group,
                "style": "referenzlayer_erschliessung/t_av_gewaesser_gepuffert.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_NPLSO_Erschliessungsplan", "Verkehrszone gepuffert 4m, 5m, 6m",
                                    None),
                "featuretype": "t_verkehrszone_gepuffert",
                "geom": "geometrie", "key": "t_id", "sql": "",
                "readonly": True, "group": group,
                "style": "referenzlayer_erschliessung/t_verkehrszone_gepuffert.qml"
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

