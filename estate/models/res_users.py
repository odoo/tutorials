from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_id = fields.One2many(comodel_name='estate.properties', inverse_name='salesperson_id', domain=[('state', 'not in', ['cancelled', 'sold'])])
