from odoo import models, fields


class InheritedSalesOrder(models.Model):
    _inherit = "sale.order"

    print_in_report = fields.Boolean()
