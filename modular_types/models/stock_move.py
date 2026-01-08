from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    modular_type_id = fields.Many2one('modular.type', compute="_compute_modular_type", store=True)
    sale_order_line_modular_value_id = fields.Many2one('sale.order.line.modular.value')
    base_bom_qty = fields.Float()

    @api.depends('production_id.bom_id.bom_line_ids')
    def _compute_modular_type(self):
        for move in self:
            move.modular_type_id = move.raw_material_production_id.bom_id.bom_line_ids.filtered(
                lambda line: line.product_id == move.product_id).modular_type_id

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            mo = move.raw_material_production_id
            so_line = mo.sale_line_id
            bom = mo.bom_id
            bom_line = bom.bom_line_ids.filtered(
                lambda l: l.product_id == move.product_id
            )[:1]
            base_qty = bom_line.product_qty * mo.product_qty
            move.base_bom_qty = base_qty
            modular_map = {
                mv.modular_type_id.id: mv.value
                for mv in so_line.modular_value_ids
            }
            if move.modular_type_id and move.modular_type_id.id in modular_map:
                move.product_uom_qty = (
                    base_qty * modular_map[move.modular_type_id.id]
                )
        return moves
