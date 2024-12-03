from odoo import models, fields, api, Command


class AddWarrantyWizard(models.TransientModel):
    _name = "add.warranty.wizard"
    _description = "Wizard to Add Warranty"

    order_id = fields.Many2one("sale.order", string="Sale Order")
    product_ids = fields.Many2many("product.product")
    warranty_lines_ids = fields.One2many(
        comodel_name="add.warranty.line.wizard",
        inverse_name="wizard_id",
        store=True,
        string="Warranty Lines",
    )

    def action_add_warranty(self):
        print("-*- " * 100)

        new_order_line_list = []
        # Iterate through the warranty lines in the wizard
        for record in self:
            print(record.order_id)
            warranty_product_ids = record.warranty_lines_ids.mapped("product_id.id")
            print("Warranty product IDs:", warranty_product_ids)

            # # Iterate over order lines to find matching products
            # for ol in record.order_id.order_line:
            #     new_order_line_list.append(ol)
            #     print(
            #         f"Checking Order Line Product: {ol.product_id.id} in Warranty Lines"
            #     )

            #     if ol.product_id.id in warranty_product_ids:
            #         print(f"Match found: {ol}")

        print(new_order_line_list)
        print("hello from warranty !")
        print("-*- " * 100)

        return new_order_line_list

    @api.model
    def default_get(self, fields):
        res = super(AddWarrantyWizard, self).default_get(fields)
        order_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(order_id)

        warranty_products = sale_order.order_line.mapped("product_id").filtered(
            lambda p: p.warranty
        )

        warranty_line_vals = []
        for product in warranty_products:
            warranty_line_vals.append(Command.create({"product_id": product.id}))
        print(warranty_products)
        res["product_ids"] = [Command.set(warranty_products)]

        return res
