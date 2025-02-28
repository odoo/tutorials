from odoo import fields, models


class SaleOrderLineDistributionWizardLine(models.TransientModel):
    _name = "sale.order.line.distribution.wizard.line"
    _description = "Sale Order Line Distribution Wizard Line"

    distribution_wizard_id = fields.Many2one(
        comodel_name='sale.order.line.distribution.wizard',
        string="Distribution Wizard",
        required=True,
    )
    sale_order_line = fields.Many2one(
        comodel_name='sale.order.line',
        string="Order Line",
        required=True,
    )
    distributed_amount = fields.Float(string="Distributed Amount")
