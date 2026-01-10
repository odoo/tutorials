from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    modular_type_id = fields.Many2one(
        comodel_name="modular.type",
        compute="_compute_modular_type_id",
        store=True,
        string="Modular Type",
    )

    @api.depends("raw_material_production_id.bom_id.bom_line_ids")
    def _compute_modular_type_id(self):
        for move in self:
            bom_line = move.raw_material_production_id.bom_id.bom_line_ids.filtered(
                lambda bl: bl.product_id == move.product_id
            )
            move.modular_type_id = bom_line.modular_type_id if bom_line else False
