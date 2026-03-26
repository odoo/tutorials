from odoo import fields, models


class resUsers(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'salesman_id', domain=['|', ('state', '=', 'new'), ('state', '=', 'offer_received')])
