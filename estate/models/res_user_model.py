from odoo import models, fields


class ResUserModel(models.Model):
    _inherit = 'res.users'
    property_ids = fields.One2many('estate.property', 'salesman_id', string='Properties', domain="['|', ('state', '=', 'new'),('state', '=', 'offer_recived')]")
