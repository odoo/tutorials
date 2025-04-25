from odoo import fields, models


class SaleOrderLineWizardLine(models.TransientModel):
    _name = 'sale.order.line.wizard.line'
    _description = 'Key-Value Line for Sale Order Line Config Wizard'

    wizard_id = fields.Many2one('sale.order.line.wizard', string='Wizard')
    modular_type_id = fields.Many2one('product.modular.type', required=True)
    value = fields.Float('Value', required=True)
