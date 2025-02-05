from odoo import api,fields,models 

class EstateResUsers(models.Model):
    _inherit="res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesman",
         string="Propereties"
    ) 