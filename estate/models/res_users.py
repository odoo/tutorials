from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'seller_id', domain=[('state', 'not in', ['sold', 'cancelled'])])
