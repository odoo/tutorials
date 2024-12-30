from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class WarrantyLineWizard(models.TransientModel):
    _name = "warranty.line.wizard"

    product_id = fields.Many2one(
        comodel_name="product.product",
        required=True,
        domain=[("has_warranty", "=", True)],
    )
    warranty_id = fields.Many2one("warranty")
    end_date = fields.Date(compute="_compute_end_date")
    warranty_list_form_id = fields.Many2one(comodel_name="warranty.wizard")
    link_order_line_id = fields.Many2one(comodel_name="sale.order.line")

    @api.depends("warranty_id")
    def _compute_end_date(self):
        for record in self:
            record.end_date = date.today() + relativedelta(
                years=record.warranty_id.duration
            )


class WarrantyWizard(models.TransientModel):
    _name = "warranty.wizard"
    _description = "Add warranty in Quotation"

    warranty_line_ids = fields.One2many(
        comodel_name="warranty.line.wizard", inverse_name="warranty_list_form_id"
    )

    def action_add_warranty_in_order_line(self):
        active_sale_order = self.env["sale.order"].browse(
            self.env.context.get("active_id")
        )
        if not active_sale_order.exists():
            raise UserError("The active sale order does not exist.")

        for line in self.warranty_line_ids:
            # only those warranty added who have warranty set. baaki to skip kro
            if not line.warranty_id:
                continue

            # Find the main product's sale order line
            main_product_line = active_sale_order.order_line.filtered(
                lambda sale_order_line: sale_order_line.product_id == line.product_id
            )
            main_product_line.is_warranty_in_order_line = True

            # Create a new order line for the warranty product
            self.env["sale.order.line"].create(
                {
                    "order_id": active_sale_order.id,
                    "product_id": line.warranty_id.product_id.id,
                    "name": f"{line.warranty_id.product_id.name}\nExtended Warranty ({line.product_id.name})\nEnd Date: {line.end_date}",
                    "product_uom_qty": 1.0,
                    "product_uom": line.warranty_id.product_id.uom_id.id,
                    "price_unit": line.product_id.list_price
                    * (line.warranty_id.percentage / 100),
                    "related_warranty_line_id": main_product_line.id,
                }
            )
