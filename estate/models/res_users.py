from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(string='Properties', comodel_name='estate.property', inverse_name='salesperson_id', domain=[('state', '=', 'available')])
