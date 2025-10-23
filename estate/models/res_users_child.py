from odoo import fields, models


class resUsersChild(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'salesperson_id', string="sales person", domain="[('state', 'in', ['New', 'Offer Received'])]")
