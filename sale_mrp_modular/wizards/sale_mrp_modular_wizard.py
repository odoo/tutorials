from odoo import api, fields, models


class SaleMrpModularWizard(models.Model):
    _name = 'sale.mrp.modular.wizard'
    _description = 'Wizard for modular values'

    modular_wizard_line_ids = fields.One2many(comodel_name='sale.mrp.modular.wizard.line', inverse_name='modular_wizard_id', string='Modular Wizard Lines')
    source_sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', string='Source Order Line')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        sale_order_line_id = self.env['sale.order.line'].browse(self.env.context['active_id'])
        res['source_sale_order_line_id'] = sale_order_line_id

        if len(sale_order_line_id.product_id.modular_type_ids):
            if not sale_order_line_id.modular_value_ids:
                modular_lines_data = [
                    (
                        0,0, {
                            "modular_type_id": modular_type_id.id,
                            "value": 1
                        }
                    ) for modular_type_id in sale_order_line_id.product_id.modular_type_ids
                ]
            else:
                modular_lines_data = sale_order_line_id.modular_value_ids

            res['modular_wizard_line_ids'] = modular_lines_data

        return res

    def action_add_modular_values(self):
        self.source_sale_order_line_id.modular_value_ids = self.modular_wizard_line_ids
