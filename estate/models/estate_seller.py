from odoo import models,fields

class EstateSeller(models.Model):
    _name = 'estate.property.seller' 
    _description = 'Seller'

    name = fields.Char(string="Salesmen", required=True)


