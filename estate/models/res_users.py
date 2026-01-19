from odoo import fields, models


class EstatePropertyUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'seller_id')
    name = fields.Char()
