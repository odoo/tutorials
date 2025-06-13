from odoo import api, fields, models


class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many("estate.property", 'salesperson_id', string="Property", domain=[('state', 'in', ['new', 'offer_received'])])
