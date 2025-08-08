from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.depends("product_id", "location_id")
    def _compute_product_stock_quant_ids(self):

        # Fetch stock quants using _read_group (aggregated results)
        result = dict(self.env["stock.quant"]._read_group(
            domain=[
                ("product_id", "in", self.product_id.ids),
                ("location_id", "child_of", self.picking_id.location_id.ids),
                ("location_id.usage", "=", "internal"),
                ("quantity", ">", 0),
                ("company_id", "in", self.env.companies.ids),
            ],
            groupby=["product_id"],
            aggregates=["id:recordset"],
        ))
        
        # Assign computed stock quant IDs
        for line in self:
            line.product_stock_quant_ids = result.get(line.product_id, self.env["stock.quant"])
