from odoo import api, fields, models
from odoo.exceptions import UserError


class WizardProductKit(models.TransientModel):
    _name = 'wizard.product.kit'
    _description = "Wizard to add product kit"

    # sale_order_id = fields.Many2one(comodel_name="sale.order")
    product_ids = fields.One2many(
        comodel_name="wizard.product.kit.add",
        inverse_name="kit_id",
        string="Product"
    )

    def add_product_kits(self):
        sale_order_id = self.env.context.get("default_sale_order_id")
        main_order_line_id = self.env.context.get("active_id")

        existing_line = self.env['sale.order.line'].search([
            ('linked_line_id', '=', main_order_line_id),
            ('order_id', '=', sale_order_id)
        ])
        existing_product_ids = existing_line.mapped('product_id.id')

        kits_price = 0
        for product in self.product_ids:
            # if product already in sale order line only update quantity and price
            if product.product_id.id in existing_product_ids:
                for line in existing_line:
                    if line.product_id.id == product.product_id.id:
                        line.write({
                            "product_uom_qty": product.quantity,
                            "price_unit": 0
                        })
            # If not found create new line
            else:
                new_sale_order_line = self.env['sale.order.line'].create({
                    "product_id": product.product_id.id,
                    "order_id": sale_order_id,
                    "product_uom_qty": product.quantity,
                    "linked_line_id": main_order_line_id,
                    "price_unit": 0,
                    "is_kit": True,
                })
                if not new_sale_order_line:
                    raise UserError("something went wrong!!!")

            kits_price += product.price

        # Updating main order line price
        order_line = self.env['sale.order.line'].browse(main_order_line_id)
        order_line.write({
            "price_subtotal": (order_line.product_uom_qty * order_line.product_id.list_price) + kits_price
        })

        return {"type": "ir.actions.act_window_close"}


class WizardProductKitAdd(models.TransientModel):
    _name = 'wizard.product.kit.add'
    _description = 'Wizard to add product kit list'

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Name",
    )
    quantity = fields.Float(string='Quantity', default=1.0)
    price = fields.Float(string='Price', compute="_compute_price")
    kit_id = fields.Many2one(
        comodel_name="wizard.product.kit",
        string="Kit Name"
    )

    @api.depends("quantity")
    def _compute_price(self):
        for record in self:
            record.price = record.quantity * record.product_id.list_price
