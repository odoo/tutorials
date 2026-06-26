from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    kit_line_ids = fields.One2many(
        'sale.order.line',
        'parent_kit_line_id',
        string="Kit Lines",
        help="Sale order lines generated from exploding this kit.",
    )
    parent_kit_line_id = fields.Many2one(
        'sale.order.line',
        string="Parent Kit Line",
        help="Parent kit sale order line that generated this line.",
        ondelete='cascade',
    )

    is_kit = fields.Boolean(
        string="Is Kit",
        compute='_compute_is_kit',
        help="Whether the product on this line is a kit.",
    )

    @api.depends('product_id')
    def _compute_is_kit(self):
        for line in self:
            line.is_kit = bool(
                line.product_id
                and line.product_id.product_tmpl_id.is_kit
                and line.product_id.product_tmpl_id.kit_product_ids
            )

    def action_open_kit_config_wizard(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'kit.config.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_order_id': self.order_id.id,
                'default_sale_line_id': self.id,
                'active_ids': self.order_id.ids,
            },
        }

    def unlink(self):

        kit_child_lines = self.env['sale.order.line']
        kit_section_lines = self.env['sale.order.line']
        for line in self:
            if line.kit_line_ids:
                kit_child_lines |= line.kit_line_ids
                # Find and remove the section header that sits between the kit line and its components
                section_line = self.search([
                    ('order_id', '=', line.order_id.id),
                    ('display_type', '=', 'line_section'),
                    ('sequence', '=', line.sequence + 1),
                ], limit=1)
                if section_line:
                    kit_section_lines |= section_line
        if kit_child_lines:
            kit_child_lines.unlink()
        if kit_section_lines:
            kit_section_lines.unlink()
        return super(SaleOrderLine, self).unlink()

    def _get_kit_component_lines(self):

        self.ensure_one()
        return self.kit_line_ids

    def _is_kit_line(self):

        self.ensure_one()
        return bool(self.kit_line_ids)

    def _is_kit_component(self):

        self.ensure_one()
        return bool(self.parent_kit_line_id)
