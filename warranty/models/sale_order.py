from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    warranty_year_id = fields.Many2one("warranty.config", string="Warranty")
    warranty_end_date = fields.Date(string="Warranty End Date")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_product_id = fields.Many2one(
        "sale.order.line",
        string="Warranty Product",
    )

    # ------------------------------------------ CRUD Method -------------------------------------
    def unlink(self):
        for line in self:
            warranty_product_ids = self.env["sale.order.line"].search(
                [("warranty_product_id", "=", line.id)]
            )
            if warranty_product_ids:
                warranty_product_ids.unlink()

            return super().unlink()
