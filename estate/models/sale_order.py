from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    property_id = fields.Many2one("estate.property")
