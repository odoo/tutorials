from odoo import api, models


class ReportMODeliveryNote(models.AbstractModel):
    _name = "report.stock_custom_picking_report.mo_delivery_note_report"
    _description = "MO Delivery Note Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["stock.picking"].browse(docids)
        filtered_moves_by_picking = {}

        for picking in docs:
            linked_mos = picking.move_ids.move_orig_ids.production_id

            if linked_mos:
                components = self.env["stock.move"].search(
                    [
                        ("raw_material_production_id", "in", linked_mos.ids),
                        "|",
                        ("bom_line_id", "=", False),
                        ("bom_line_id.bom_id.type", "!=", "phantom"),
                    ]
                )
                filtered_moves_by_picking[picking.id] = components
            else:
                filtered_moves_by_picking[picking.id] = picking.move_ids

        return {
            "docs": docs,
            "filtered_moves": filtered_moves_by_picking,
        }
