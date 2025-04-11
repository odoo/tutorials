from odoo import api, fields, models
from odoo.exceptions import UserError


class ModularTypeWizard(models.TransientModel):
    _name = "modular.type.wizard"
    _description = "Modular Type Wizard"

    product_id = fields.Many2one('product.template', string='product Id')
    wizard_lines = fields.One2many('modular.type.wizard.line', 'wizard_id')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        product_template = self.env['sale.order.line'].browse(self.env.context.get('active_id')).product_template_id

        if product_template:
            modular_types = product_template.modular_types
            modular_types_data = [
                (
                0, 0, {
                        'modular_type_id': type.id,
                        'value': 0,
                    },
                )
                for type in modular_types
            ]
        else:
            raise UserError("Product Template Id not found.....!!!")
        res.update({
            'product_id': product_template.id,
            'wizard_lines': modular_types_data,
        })

        return res

    def action_add(self):
        active_order_line_id = self.env.context.get('active_order_line_id')
        for record in self:
            if not record.product_id:
                raise UserError("Product Template Id not found.....!!!")
            for wizard_line in record.wizard_lines:
                if not wizard_line.modular_type_id:
                    raise UserError("Please select a Modular Type for all lines before submitting.")
                existing = self.env['sale.order.line.modular.value'].search([
                    ('order_line_id', '=', active_order_line_id),
                    ('modular_type_id', '=', wizard_line.modular_type_id.id)
                ], limit=1)

                if existing:
                    existing.value = wizard_line.value
                else:
                    self.env['sale.order.line.modular.value'].create({
                        'order_line_id': active_order_line_id,
                        'modular_type_id': wizard_line.modular_type_id.id,
                        'value': wizard_line.value,
                    })
        return


# contain remaining line's indivudual data
class ModularTypeWizardLine(models.TransientModel):
    _name = "modular.type.wizard.line"
    _description = "Modular Type Wizard Line"

    wizard_id = fields.Many2one('modular.type.wizard')
    modular_type_id = fields.Many2one('modular.type')
    value = fields.Integer(string='Value')
