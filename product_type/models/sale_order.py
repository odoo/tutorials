from odoo import fields, models


class sale_order(models.Model):
    _inherit = "sale.order"

    is_print = fields.Boolean(default=False, string="is_print")
