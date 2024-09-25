from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class SaleOrderWarrantyWizard(models.TransientModel):
    _name = "sale.order.warranty.wizard"

    product_ids = fields.One2many('warranty.wizard.add.line', 'warranty_id')

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(active_id)

        warranty_lines = self.env['warranty.wizard.add.line'].create([
            {
                'product': product.product_template_id.id,
            }
            for product in sale_order.order_line
            if product.product_template_id.warranty_available
        ])

        res['product_ids'] = [(6, 0, warranty_lines.ids)]
        return res

    def add_warranty_wizard_action(self):
        active_id = self.env.context.get('active_id')
        sale_order = self.env['sale.order'].browse(active_id)
        for record in self.product_ids:
            sale_order_line = sale_order.order_line.filtered(
                lambda line: line.product_template_id == record.product)
            price = sale_order_line.price_subtotal * (record.year.percentage / 100)
            vals_to_create = {
                "name": "Exteded Warranty End Date: " + str(record.end_date),
                "order_id": sale_order.id,
                "price_unit": price,
                "product_id": record.year.product_id.id,
                "tax_id": None,
                "warranty_product_id": sale_order_line.product_template_id.id
            }
            # self.env["sale.order.line"].create(vals_to_create)
            sale_order.order_line.create(vals_to_create)


class WarrantyWizardAddLine(models.TransientModel):
    _name = "warranty.wizard.add.line"

    warranty_id = fields.Many2one("sale.order.warranty.wizard")
    product = fields.Many2one("product.template", string="Product")
    year = fields.Many2one("product.warranty")
    end_date = fields.Date(compute="_compute_end_date", store=True)

    @api.depends('year')
    def _compute_end_date(self):
        for record in self.year:
            if record.year:
                self.end_date = fields.date.today() + relativedelta(years=record.year)
