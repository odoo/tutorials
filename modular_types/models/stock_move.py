from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    modular_type_id = fields.Many2one('modular.type', compute="_compute_modular_type")

    @api.depends('production_id.bom_id.bom_line_ids')
    def _compute_modular_type(self):
        for move in self:
            move.modular_type_id = move.raw_material_production_id.bom_id.bom_line_ids.filtered(lambda line: line.product_id == move.product_id).modular_type_id
