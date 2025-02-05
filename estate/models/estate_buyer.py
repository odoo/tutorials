from odoo import models,fields

class EstateBuyer(models.Model):
    _name='estate.property.buyer'
    _description='Buyes'

    name=fields.Char(string="Buyer",required=True)
    
