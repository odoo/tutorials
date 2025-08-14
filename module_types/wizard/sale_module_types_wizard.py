from odoo import Command, api, fields, models


class SaleModuleTypeWizard(models.TransientModel):
    _name = "sale.module.type.wizard"
    _description = "Wizard to set Module Types for Sales Order Line"

    wizard_lines = fields.One2many(
        comodel_name='sale.module.type.wizard.line',
        inverse_name='wizard_id',
        string='Modular Wizard Lines'
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sales_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        if sales_order_line.product_template_id:
            res.update({
                'wizard_lines': [
                    Command.create({
                        'module_type_id': modular_type.id,
                        'value': modular_type.value
                    })
                    for modular_type in sales_order_line.product_template_id.module_types
                ],
            })
        return res

    def action_confirm(self):
        for lines in self.wizard_lines:
            lines.module_type_id.write({
                'value': lines.value
            })
        

class SaleModuleTypeWizardLine(models.TransientModel):
    _name = "sale.module.type.wizard.line"
    _description = "Wizard Lines for Module Types"

    wizard_id = fields.Many2one('sale.module.type.wizard')
    module_type_id = fields.Many2one('module.types', string="Module Type")
    value = fields.Integer()
