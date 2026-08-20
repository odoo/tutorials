from odoo import models, fields, api


class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = ["res.users"]

    property_ids = fields.One2many('estate.property', 'salesperson_id', string="Real Estate Properties", domain=[('status', 'in', ['new','offer_received'])])
