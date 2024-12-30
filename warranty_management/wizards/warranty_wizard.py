from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class WarrantyWizard(models.TransientModel):
    _name = "warranty.wizard"
    _description = "Warranty Wizard"

    product_id = fields.Many2one("product.product", string="Product", required=True)
    warranty_id = fields.Many2one("warranty.configuration")
    end_date = fields.Date(string="End Date", compute="_compute_end_date")
    warranty_list_form_id = fields.Many2one(comodel_name="add.warranty")
    order_line_id = fields.Integer()
    @api.depends("warranty_id")
    def _compute_end_date(self):
            for record in self:
                    record.end_date = date.today() + relativedelta(
                        years=record.warranty_id.extended_years
                    )

class AddWarranty(models.TransientModel):
    _name = "add.warranty"
    _description = "Add warranty"

    warranty_lines_ids = fields.One2many(
        comodel_name="warranty.wizard", inverse_name="warranty_list_form_id"
    )

    def action_add_warranty_in_order_line(self):
        active_sale_order = self.env["sale.order"].browse(
            self.env.context.get("active_id")
        )
        for line in self.warranty_lines_ids:
            if line.warranty_id:
                self.env["sale.order.line"].create(
                    {
                        "order_id": active_sale_order.id,
                        "product_id": line.warranty_id.product_id.id,
                        "name": f"{line.warranty_id.product_id.name} \nEnd Date: {line.end_date}",
                        "product_uom_qty": 1.0,
                        "product_uom": line.warranty_id.product_id.uom_id.id,\
                        "price_unit": line.product_id.list_price * (line.warranty_id.percentage / 100),
                        "warranty_linked": line.order_line_id,
                    }
                )
