from odoo import api, exceptions, fields, models


class ModularTypeWizard(models.TransientModel):
    _name = 'modular.type.wizard'
    _description = 'Modular Type Wizard'

    product_id = fields.Many2one('product.template', readonly=True)
    wizard_line_ids = fields.One2many('modular.type.wizard.line', 'wizard_id')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        order_line = self.env['sale.order.line'].browse(
            self.env.context.get('active_order_line_id')
        )
        product = order_line.product_template_id
        res.update({
            'product_id': product.id,
            'wizard_line_ids': [
                (0, 0, {'modular_type_id': mt.id, 'value': 0})
                for mt in product.modular_types
            ]
        })
        return res

    def add_modular_value(self):
        active_order_line_id = self.env.context.get('active_order_line_id')
        if not self.product_id:
            raise exceptions.UserError("Sales order line not found.")
        for line in self.wizard_line_ids:
            existing = self.env['sale.order.line.modular.value'].search([
                ('order_line_id', '=', active_order_line_id),
                ('modular_type_id', '=', line.modular_type_id.id),
            ], limit=1)
            if existing:
                existing.value = line.value
            else:
                self.env['sale.order.line.modular.value'].create({
                    'order_line_id': active_order_line_id,
                    'modular_type_id': line.modular_type_id.id,
                    'value': line.value,
                })
        return


class ModularTypeWizardLine(models.TransientModel):
    _name = 'modular.type.wizard.line'
    _description = 'Modular Type Wizard Line'

    wizard_id = fields.Many2one('modular.type.wizard')
    modular_type_id = fields.Many2one('modular.type')
    value = fields.Float()
