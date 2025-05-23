from odoo import fields, models, api


class users(models.Model):
    _inherit = "res.users"
    property_ids = fields.One2many('estate_property', 'seller', domain=[('state', 'not in', ['offer_accepted','sold', 'cancelled'])])
