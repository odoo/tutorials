from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class AddWarranty(models.TransientModel):
    _name = "warranty.add"
    product_ids = fields.One2many('warranty.add.line', 'warranty_id')

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields) or {}
        active_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(active_id)

        products_to_add = []
        for product in sale_order.order_line:

            if product.product_template_id.warranty_available:
                product_values = {
                    'product': product.product_template_id.id,
                }

                products_to_add.append((0, 0, product_values))

        res['product_ids'] = products_to_add
        return res

    def add_warranty_wizard_action(self):
        print("clicked ADD")

        active_id = self.env.context.get('active_id')
        sale_order = self.env['sale.order'].browse(active_id)
        # Product tempolate id iterate
        for record in self.product_ids:
            # print(record)
            # print(record.product.name)
            if record.year:
                sale_order_line = sale_order.order_line.filtered(
                    lambda line: line.product_template_id == record.product)
                # print("t-> ", sale_order_line.name)
                
                price = sale_order_line.price_subtotal * (record.year.percentage/100)
                # print("p->", price)
                sale_order.order_line.create({
                    "name": f"{record.year.product_id.name}/ {record.end_date}",
                    "order_id": sale_order.id,
                    "price_unit": price,
                    "product_id": record.year.product_id.id,
                    "product_uom": self.env.ref("uom.product_uom_unit").id,
                    "tax_id": None,
                    "warranty_product_id": sale_order_line.product_template_id.id
                })


class ProductList(models.TransientModel):
    _name = "warranty.add.line"

    warranty_id = fields.Many2one("warranty.add")
    product = fields.Many2one("product.template", string="Product")
    year = fields.Many2one("warranty.config")
    end_date = fields.Date(compute="_compute_end_date", readonly=True)

    @api.depends('year')
    def _compute_end_date(self):
        print("end date computed")
        for record in self:
            if record.year != None:
                record.end_date = fields.Date.today() + relativedelta(years=record.year.period)
