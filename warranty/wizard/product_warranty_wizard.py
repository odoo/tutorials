from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, Command


class ProductWarrantyWizard(models.TransientModel):
    _name = "product.warranty.wizard"
    _description = "Product Warranty Wizard"

    product_ids = fields.One2many(
        "product.warranty.list", "warranty_line", string="Warranty Lines"
    )

    # @api.model
    # def default_get(self, fields):
    #     res = super(ProductWarrantyWizard, self).default_get(fields)
    #     order_id = self.env['sale.order'].browse(self._context.get('active_id'))
    #     order_lines_with_warranty = order_id.order_line.filtered(
    #         lambda line: line.product_id.warranty and not line.warranty_line_ids
    #     )

    #     res['product_ids'] = [
    #         Command.create({"product_id": line.product_id.id, "main_order_line": line.id})
    #         for line in order_lines_with_warranty
    #     ]
    #     return res

    def add_warranty(self):
        for record in self.product_ids:
            if record.year:
                self.env["sale.order.line"].create(
                    {
                        "sequence": record.main_order_line.sequence + 1,
                        "product_id": record.year.product_id.id,
                        "product_uom_qty": record.main_order_line.product_uom_qty,
                        "order_id": self._context.get("active_id"),
                        "price_unit": record.product_id.list_price
                        * record.year.percentage
                        / 100,
                        "warranty_line_id": record.main_order_line.id,
                        "name": record.year.product_id.name
                        + "\nFor "
                        + record.main_order_line.name
                        + ", End Date: "
                        + str(record.end_date),
                    }
                )


class ProductWarrantyList(models.TransientModel):
    _name = "product.warranty.list"
    _description = "Product Warranty List"

    product_id = fields.Many2one("product.product", string="Product", readonly=True)
    year = fields.Many2one("product.warranty", string="Year")
    end_date = fields.Date(string="End Date", compute="_compute_end_date")
    warranty_line = fields.Many2one("product.warranty.wizard", string="Warranty Line")
    main_order_line = fields.Many2one("sale.order.line", string="Order Line")

    @api.depends("year")
    def _compute_end_date(self):
        for record in self:
            record.end_date = datetime.now() + relativedelta(years=record.year.duration)
