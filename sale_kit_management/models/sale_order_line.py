from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    _KIT_SUBPRODUCT_SEQ_BASE = 9990

    is_kit = fields.Boolean(related='product_id.product_tmpl_id.is_kit')
    is_kit_subproduct = fields.Boolean(string="Is Kit Subproduct", default=False)
    kit_unit_qty = fields.Float(string="Kit Unit Qty")
    kit_parent_line_id = fields.Many2one('sale.order.line', string="Kit Parent Line", ondelete='cascade', index=True)
    has_kit_subproducts = fields.Boolean(compute='_compute_has_kit_subproducts')
    kit_config_line_ids = fields.One2many('sale.order.kit.config.line', 'sale_order_line_id', string="Kit Configuration")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_kit_subproduct') or vals.get('kit_parent_line_id'):
                continue
            seq = vals.get('sequence', 0)
            if seq >= self._KIT_SUBPRODUCT_SEQ_BASE:
                vals['sequence'] = self._KIT_SUBPRODUCT_SEQ_BASE - 1
        return super().create(vals_list)

    @api.depends('order_id.order_line.kit_parent_line_id')
    def _compute_has_kit_subproducts(self):
        for line in self:
            if line.is_kit and line.id:
                line.has_kit_subproducts = any(
                    l.kit_parent_line_id.id == line.id
                    for l in line.order_id.order_line
                    if l.is_kit_subproduct
                )
            else:
                line.has_kit_subproducts = False

    def _compute_kit_price(self):
        for line in self:
            if line.is_kit and line.kit_config_line_ids:
                line.price_unit = sum(
                    cl.price_unit * cl.product_uom_qty
                    for cl in line.kit_config_line_ids
                )

    def write(self, vals):
        result = super().write(vals)
        if 'product_uom_qty' in vals:
            for line in self.filtered(lambda l: l.is_kit and l.id):
                child_lines = self.env['sale.order.line'].search([
                    ('kit_parent_line_id', '=', line.id),
                    ('is_kit_subproduct', '=', True),
                ])
                for child in child_lines:
                    if child.kit_unit_qty:
                        child.product_uom_qty = line.product_uom_qty * child.kit_unit_qty
                        child.price_unit = 0
        return result

    @api.ondelete(at_uninstall=False)
    def _ondelete_handle_kit(self):
        for line in self.filtered(lambda l: l.is_kit_subproduct):
            if line.kit_parent_line_id in self:
                continue
            section_in_batch = any(
                l.display_type == 'line_section'
                and l.kit_parent_line_id.id == line.kit_parent_line_id.id
                for l in self
            )
            if section_in_batch:
                continue
            raise UserError(_(
                "You cannot delete subproduct lines directly. "
                "Delete the parent kit product or delete the entire subproducts section."
            ))

        child_lines = self.env['sale.order.line'].search([
            ('kit_parent_line_id', 'in', self.ids),
            ('id', 'not in', self.ids),
        ])
        if child_lines:
            child_lines.unlink()

    def action_open_kit_configurator(self):
        self.ensure_one()
        return {
            'name': _("Kit"),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.kit',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_order_line_id': self.id},
        }
