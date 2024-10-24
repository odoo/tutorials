from odoo import models, fields


class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'salesperson_id', string='Properties',
                                   domain="[('date_availability', '&lt;=', context_today().strftime('%Y-%m-%d'))]")
