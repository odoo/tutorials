from odoo import api, fields, models


class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many("estate.property", inverse_name="salesman", domain="['|', ('state', '=', 'new'), ('state', '=', 'offer received')]")
