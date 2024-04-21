from odoo import fields, models

class ResUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate_property', 'user_id', domain=[('state', 'in', ['New', 'Offer Received'])])
