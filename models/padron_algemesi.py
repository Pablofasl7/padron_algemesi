from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

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