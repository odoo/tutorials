from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_add_warranty_button = fields.Boolean(
        string="Show Add Warranty Button", compute="_compute_show_add_warranty_button"
    )
    warranty_year_id = fields.Many2one("warranty.config", string="Warranty")
    warranty_end_date = fields.Date(string="Warranty End Date")

    @api.depends("order_line.product_id")
    def _compute_show_add_warranty_button(self):
        for order in self:
            # Check if any product in the order lines has the warranty_available flag set to True
            order.show_add_warranty_button = any(
                line.product_id.warranty_available for line in order.order_line
            )

    @api.model
    def unlink(self):
        for line in self:
            # Check if the line has a warranty before unlinking
            if line.warranty_year_id:
                line.write({"warranty_year_id": False, "warranty_end_date": False})
        return super().unlink()
