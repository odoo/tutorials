from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line.kit_line_ids', 'order_line.parent_kit_line_id')
    def _compute_kit_lines_count(self):
        for order in self:
            order.kit_lines_count = len(
                order.order_line.filtered(lambda l: l.kit_line_ids or l.parent_kit_line_id)
            )

    kit_lines_count = fields.Integer(
        string="Kit Lines",
        compute='_compute_kit_lines_count',
    )

    def action_open_kit_config_wizard(self):

        self.ensure_one()

        context = self.env.context.copy()
        active_line_id = context.get('active_id')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'kit.config.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id,
                'default_sale_line_id': active_line_id,
                'active_ids': self.ids,
            },
        }

    def action_confirm(self):

        res = super(SaleOrder, self).action_confirm()

        for order in self:
            lines_to_process = order.order_line.filtered(
                lambda l: l.product_id and not l.kit_line_ids
                          and l.product_id.product_tmpl_id.is_kit
                          and l.product_id.product_tmpl_id.kit_product_ids
            )
            for line in lines_to_process:
                kit_template = line.product_id.product_tmpl_id

                section_seq = line.sequence + 1
                self.env['sale.order.line'].create({
                    'order_id': order.id,
                    'display_type': 'line_section',
                    'name': _("Sub products of %s", line.name),
                    'sequence': section_seq,
                })

                for idx, kit_component in enumerate(kit_template.kit_product_ids):
                    vals = {
                        'order_id': order.id,
                        'product_id': kit_component.product_id.id,
                        'product_uom_qty': line.product_uom_qty * kit_component.quantity,
                        'price_unit': kit_component.product_id.lst_price,
                        'name': kit_component.product_id.display_name,
                        'parent_kit_line_id': line.id,
                        'sequence': section_seq + 1 + idx,
                    }
                    child_line = self.env['sale.order.line'].create(vals)
                    line.write({'kit_line_ids': [(4, child_line.id)]})

                vals = {'product_uom_qty': 0}
                if line.name and not line.name.startswith('[Kit] '):
                    vals['name'] = f"[Kit] {line.name}"
                line.write(vals)

        return res
