"""Extension of the users model."""

from odoo import fields, models


class Users(models.Model):
    """Users extension with inheritance to linked offers on salespersons."""

    _inherit = 'res.users'

    offer_ids = fields.One2many('estate.property', 'user_id', string='Real Estate Properties')
