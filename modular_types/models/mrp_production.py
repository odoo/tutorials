from odoo import models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def _get_moves_raw_values(self):
        res = super()._get_moves_raw_values()
        for production in self:
            if (
                not production.sale_line_id
                or not production.sale_line_id.modular_value_ids
            ):
                continue

            factors = {
                val.modular_type_id.id: val.value
                for val in production.sale_line_id.modular_value_ids
            }

            for move_vals in res:
                if move_vals.get("raw_material_production_id") == production.id:
                    bom_line_id = move_vals.get("bom_line_id")
                    if bom_line_id:
                        bom_line = self.env["mrp.bom.line"].browse(bom_line_id)
                        if (
                            bom_line.modular_type_id
                            and bom_line.modular_type_id.id in factors
                        ):
                            factor = factors[bom_line.modular_type_id.id]
                            move_vals["product_uom_qty"] *= factor
        return res

    def _get_move_raw_values(
        self, product, product_uom_qty, product_uom, operation_id=False, bom_line=False
    ):
        res = super()._get_move_raw_values(
            product, product_uom_qty, product_uom, operation_id, bom_line
        )
        if bom_line and bom_line.modular_type_id:
            res["modular_type_id"] = bom_line.modular_type_id.id
        return res
