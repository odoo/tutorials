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
        for line in sale_order.order_line:

            if line.product_template_id.warranty_available:

                product_values = {
                    'product_id': line.id,
                    'name': line.name,
                }

                products_to_add.append((0, 0, product_values))

        res['product_ids'] = products_to_add
        return res

    def add_warranty_wizard_action(self):

        active_id = self.env.context.get('active_id')
        sale_order = self.env['sale.order'].browse(active_id)

        for record in self.product_ids:

            if record.year:

                sale_order_line = sale_order.order_line.filtered(lambda line: line == record.product_id)

                price = sale_order_line.price_subtotal * (record.year.percentage / 100)

                sale_order.order_line.create({
                    "name": f"{record.year.product_id.name}/ {record.end_date}",
                    "order_id": sale_order.id,
                    "price_unit": price,
                    "product_id": record.year.product_id.id,
                    "product_uom": self.env.ref("uom.product_uom_unit").id,
                    "tax_id": None,
                    "warranty_product_id": sale_order_line.id
                })
