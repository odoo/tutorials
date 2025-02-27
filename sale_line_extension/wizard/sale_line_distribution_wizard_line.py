from odoo import fields, models


class SaleLineDistributionWizard(models.TransientModel):
    _name = "sale.line.distribution.wizard.line"
    _description = "Sale Line Distribution Wizard Line"

    wizard_id = fields.Many2one(comodel_name='sale.line.distribution.wizard', string="Wizard", required=True)
    sale_order_line = fields.Many2one(comodel_name='sale.order.line', string="Order Line", required=True)
    distributed_cost = fields.Float(string="Distributed Cost")
