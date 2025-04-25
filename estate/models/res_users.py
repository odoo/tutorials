from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"
    property_ids = fields.One2many('estate.property', 'sales_person', domain = [('state', 'in', ['new', 'received'])], store = True)