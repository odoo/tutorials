from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    offer_ids = fields.One2many('estate.property', 'user_id', string='Real Estate Properties')
