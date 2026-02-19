# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'seller_id', string='Properties for Sale', domain="['|',('state', '=', 'new'),('state', '=', 'offer_received')]")
