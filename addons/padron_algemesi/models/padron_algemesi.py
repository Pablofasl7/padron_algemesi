from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from zeep import Client
from zeep.transports import Transport 
from requests import Session
from requests.auth import HTTPBasicAuth

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

    nia = fields.Char(readonly=True)
    
    def get_people(self):
        
        ENDPOINT = "https://192.168.15.123/karat/services/POBLACION/sh_poblacionws.sh_poblacionwsHttpsSoap11Endpoint/"
        VERIFY = False
        username = "srvpoblacion"
        password = "KS9bRhQ7"
        session = Session()
        session.verify = VERIFY
        session.auth = HTTPBasicAuth(username, password)
        client = Client("http://192.168.15.123:5580/karat/services/POBLACION/sh_poblacionws?wsdl")
        service = client.create_service("{http://192.168.15.123:5580/karat/services/POBLACION/sh_poblacionws}sh_poblacionwsSoap11Binding",ENDPOINT)
        
        response = service.certificadoHabitante(certificadoHabitanteRequest={
            "ramon":"ramon"
        })
        print(response)
        print(response)
        print(response)
        
        
        
        
        
        