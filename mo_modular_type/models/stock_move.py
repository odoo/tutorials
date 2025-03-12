from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    modular_type_id = fields.Many2one(
        "module.types",
        string="Module Types",
        compute="_compute_modular_type",
        store=True,
    )

    @api.depends("raw_material_production_id")
    def _compute_modular_type(self):
        for move in self:
            # If move is linked to a Manufacturing Order (MO)
            if move.raw_material_production_id:
                bom_line = self.env["mrp.bom.line"].search(
                    [
                        ("product_id", "=", move.product_id.id),
                        ("bom_id", "=", move.raw_material_production_id.bom_id.id),
                    ],
                    limit=1,
                )
                if bom_line:
                    move.modular_type_id = bom_line.modular_type_id 
            else:
                move.modular_type_id = False  



    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)

        for move in moves:
            if move.bom_line_id and move.raw_material_production_id:
                # Get the Sale Order linked to the MO
                sale_order = self.env["sale.order"].search(
                    [("name", "=", move.raw_material_production_id.origin)], limit=1
                )

                if sale_order:
                    # Find the matching modular type value
                    matching_value = sale_order.order_line.mapped("modular_type_values").filtered(
                        lambda val: val.modular_type_id == move.bom_line_id.modular_type_id
                    )
                    
                    if matching_value:
                        move.product_uom_qty = move.bom_line_id.product_qty * matching_value[0].value
                       
        return moves

