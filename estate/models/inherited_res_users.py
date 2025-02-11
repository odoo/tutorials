from odoo import api, fields, models


class InheritedResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many("estate.property", inverse_name="salesman", domain=[("state", "in", ["new", "offer received"])])
