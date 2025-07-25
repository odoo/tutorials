from odoo import fields, models


class SaleMrpModularWizardLine(models.Model):
    _name = 'sale.mrp.modular.wizard.line'
    _description = 'Wizard Line for modular values'

    modular_type_id = fields.Many2one(comodel_name='sale.mrp.modular', string='Modular Type')
    value = fields.Integer(string='Values')
    source_sale_order_line_id = fields.Many2one('sale.order.line')

    modular_wizard_id = fields.Many2one(comodel_name='sale.mrp.modular.wizard', string='Modular Wizard')
