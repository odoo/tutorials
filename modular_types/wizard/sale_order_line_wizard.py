from collections import defaultdict

from odoo import Command, api, fields, models


class SaleOrderLineWizard(models.TransientModel):
    _name = 'sale.order.line.wizard'
    _description = 'Sale Order Line Wizard to assign values to modular types'

    sale_order_line_id = fields.Many2one(
        comodel_name='sale.order.line', string='Sale Order Line', required=True
    )
    wizard_line_ids = fields.One2many(
        comodel_name='sale.order.line.wizard.line',
        inverse_name='wizard_id',
        string='Modular Type Values',
        required=True,
    )

    @api.model
    def default_get(self, field_ids):
        """
        Override default_get to set default values for the wizard.
        Populates the wizard with existing values if available.
        If no existing values are found, it initializes the wizard with 0
        """
        result = super().default_get(field_ids)
        if self.env.context.get(
            'active_model'
        ) == 'sale.order.line' and self.env.context.get('active_id'):
            line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
            possible_modular_types = (
                line.product_id.bom_ids.sorted('sequence')[0].applied_modular_types
                if line.product_id and line.product_id.bom_ids
                else self.env['product.modular.type']
            )

            # Populate existing modular type values if any
            existing_kvs = self.env['modular.type.value'].search([
                ('sale_order_line_id', '=', line.id),
                ('modular_type_id', 'in', possible_modular_types.ids),
            ])

            kv_dict = defaultdict(lambda: 0.0)
            for kv in existing_kvs:
                kv_dict[kv.modular_type_id.id] = kv.value

            wizard_lines = self.env['sale.order.line.wizard.line'].create([
                {'modular_type_id': kv.id, 'value': kv_dict[kv.id]}
                for kv in possible_modular_types
            ])

            result.update({
                'sale_order_line_id': line.id,
                'wizard_line_ids': [Command.set(wizard_lines.ids)],
            })
        return result

    def save_configuration(self):
        self.ensure_one()
        # Clear existing key-values
        self.sale_order_line_id.modular_type_value_ids.unlink()

        # Create new key-values
        for line in self.wizard_line_ids:
            self.env['modular.type.value'].create({
                'sale_order_line_id': self.sale_order_line_id.id,
                'modular_type_id': line.modular_type_id.id,
                'value': line.value,
            })

        return {'type': 'ir.actions.act_window_close'}
