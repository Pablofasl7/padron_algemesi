from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from zeep import Client
from zeep.transports import Transport 
from requests import Session
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from datetime import datetime

class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    level_studies = fields.Char(help="Nivel de estudios.", readonly=True)
    variation_date = fields.Date(help="Fecha en la que se modifica algún valor necesario para avisar al INE.", readonly=True)
    create_date = fields.Date(help="Fecha de creacion del contacto.", readonly=True)
    provice_birth = fields.Char(help="Provincia de nacimiento.", readonly=True)
    destination_province = fields.Char(readonly=True)
    municipality_birth = fields.Char(help="Municipio de nacimiento.", readonly=True)
    destination_municipality = fields.Char(readonly=True)
    country_nationality = fields.Char(help="Pais de nacionalidad.", readonly=True)
    variation_code = fields.Char(readonly=True)

    nia = fields.Char(string="NIA", help="Prueba", readonly=True)
    
    def get_people(self):
        
        ENDPOINT = "http://192.168.15.123:5580/karat/services/POBLACION/sh_poblacionws.sh_poblacionwsHttpSoap11Endpoint/"
        username = "srvpoblacion"
        password = "KS9bRhQ7"

        session = Session()
        session.verify = False
        session.auth = HTTPBasicAuth(username,password)
        client = Client("http://192.168.15.123:5580/karat/services/POBLACION/sh_poblacionws?wsdl", transport=Transport(session=session))

        service = client.create_service("{http://client.ws.unit4.com}sh_poblacionwsSoap11Binding", ENDPOINT)
        
        # Create XML parameters
        parametros = ET.Element("parametros")
        param1 = ET.SubElement(parametros, "parametro", id="CODIGOPROVINCIA")
        param2 = ET.SubElement(parametros, "parametro", id="CODIGOMUNICIPIO")
        param3 = ET.SubElement(parametros, "parametro", id="NIF")
        param4 = ET.SubElement(parametros, "parametro", id="TIPODOCUMENTO")
        param5 = ET.SubElement(parametros, "parametro", id="TIPOVOLANTE")
        param6 = ET.SubElement(parametros, "parametro", id="IDIOMA")
        param7 = ET.SubElement(parametros, "parametro", id="GENERARDOCUMENTO")

        # Set parameter values
        param1.text = "46"
        param2.text = "29"
        param3.text = "20863603G"
        param4.text = "1"
        param5.text = "0"
        param6.text = "0"  # Assuming this parameter is optional and can be left empty
        param7.text = "2"

        # Convert XML tree to string
        xml_str = ET.tostring(parametros, encoding="unicode", method="xml")

        # Now you can send the XML string to the service
        resp = service.existeHabitante(smlEntrada=xml_str)

        print(resp)
        self.procesar_xml(resp)

    def procesar_xml(self, xml_data):
        xml_tree = ET.fromstring(xml_data)

        datos_persona = xml_tree.find('DatosPersona')
        if datos_persona is not None:
            nivel_estudios = datos_persona.find('ESTUDIOS').text
            fecha_modificacion = datetime.strptime(datos_persona.find('FECHAVARIACION').text, '%d/%m/%Y').date()
            provincia_nacimiento = datos_persona.find('DESCRIPCION_PROVINCIANACIMIENTO').text
            municipio_nacimiento = datos_persona.find('DESCRIPCION_MUNICIPIONACIMIENTO').text
            pais_nacionalidad = datos_persona.find('DESCRIPCION_NACIONALIDAD').text
            codigo_variacion = datos_persona.find('CODIGOVARIACION').text
            # nia = datos_persona.find('NIA').text  

            self.write({
                'level_studies': nivel_estudios,
                'variation_date': fecha_modificacion,
                'provice_birth': provincia_nacimiento,
                'municipality_birth': municipio_nacimiento,
                'country_nationality': pais_nacionalidad,
                'variation_code': codigo_variacion,
                #'nia': nia,
            })    