from odoo import fields, models


class EstateCustomer(models.Model):
    _inherit = "res.partner"

    estate_ids = fields.Many2many("estate.estate")
