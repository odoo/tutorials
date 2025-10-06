from odoo import api, Command, fields, models


class ModularTypesWizard(models.Model):
    _name = 'modular.types.wizard'
    _description = 'Wizard for modular values'

    modular_wizard_line_ids = fields.One2many(
        comodel_name='modular.types.wizard.line',
        inverse_name='modular_wizard_id',
        string='Modular Wizard Lines'
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        if sale_order_line.product_id:
            res.update({
                'modular_wizard_line_ids': [
                    Command.create({
                        'modular_type_id': modular_type.id,
                        'current_value': modular_type.multiplier
                    })
                    for modular_type in sale_order_line.product_id.modular_type_ids
                ],
            })
        return res

    def action_add_modular_values(self):
        for wizard_lines in self.modular_wizard_line_ids:
            wizard_lines.modular_type_id.write({
                'multiplier': wizard_lines.current_value
            })
        self.env['sale.order.line'].browse(self.env.context.get('active_id')).write({
                'is_modular_type_set': True
            })

class ModularTypesWizardLine(models.Model):
    _name = 'modular.types.wizard.line'
    _description = 'Wizard Line for modular values'

    modular_wizard_id = fields.Many2one('modular.types.wizard', string='Modular Wizard')
    modular_type_id = fields.Many2one('modular.types', string='Modular Type')
    current_value = fields.Integer()
