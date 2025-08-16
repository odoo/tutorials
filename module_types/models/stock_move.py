from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    module_type_id = fields.Many2one(
        comodel_name='module.types',
        compute="_compute_modular_type_id",
        string='Modular Type')

    @api.depends('production_id.bom_id.bom_line_ids')
    def _compute_modular_type_id(self):
        for line in self:
            line.module_type_id = line.raw_material_production_id.bom_id.bom_line_ids.filtered(lambda bom_line: bom_line.product_id == line.product_id).module_types_id
