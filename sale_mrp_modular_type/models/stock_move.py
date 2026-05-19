from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    modular_type_id = fields.Many2one(
        'modular.type', compute="_compute_modular_type", store=True
    )
    sale_order_line_modular_value_id = fields.Many2one('sale.order.line.modular.value')
    base_bom_qty = fields.Float()

    @api.depends('production_id.bom_id.bom_line_ids')
    def _compute_modular_type(self):
        for move in self:
            mo = move.raw_material_production_id
            move.modular_type_id = mo.bom_id.bom_line_ids.filtered(
                lambda line: line.product_id == move.product_id).modular_type_id

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            mo = move.raw_material_production_id
            so_line = mo.sale_line_id
            if so_line:
                so_line._set_default_modular_values()
            bom_line = mo.bom_id.bom_line_ids.filtered(
                lambda line: line.product_id == move.product_id
            )[:1]
            move.base_bom_qty = bom_line.product_qty * mo.product_qty
            modular_value = so_line.modular_value_ids.filtered(
                lambda mv: mv.modular_type_id == bom_line.modular_type_id
            )
            if bom_line.modular_type_id and modular_value:
                move.product_uom_qty = move.base_bom_qty * modular_value.value
        return moves
