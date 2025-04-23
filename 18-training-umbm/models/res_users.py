from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(comodel_name='estate_property', inverse_name='salesman_id', string="Properties")
    #domain="[('usage', '=', 'internal')]"
