from odoo import Command, api, fields, models


class ProductKit(models.TransientModel):
    _name = 'product.kit'
    _description = "Kit Wizard"

    sale_order_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string="Sale Order Line",
        required=True,
        help="Reference to the sale order line",
    )
    kit_product_id = fields.Many2one(related='sale_order_line_id.product_id')
    kit_subproducts_ids = fields.One2many(
        comodel_name='product.kit.line',
        inverse_name='product_kit_id',
        string="Sub Products",
        compute="_compute_kit_subproducts",
        store=True,
        readonly=False,
    )

    @api.depends('sale_order_line_id')
    def _compute_kit_subproducts(self):
        for product in self:
            if product.sale_order_line_id:
                product.kit_subproducts_ids = [
                    Command.create({
                        'product_id': component.kit_component_id.id,
                        'kit_component_id': component.id,
                        'quantity': component.kit_qty,
                        'price': component.price,
                    })
                    for component in product.sale_order_line_id.kit_component_ids
                ]

    def action_confirm(self):
        """
        Confirms the changes made in the wizard and updates the sale order line accordingly.
        - Updates existing kit components with the new quantities and prices.
        - If a sub-product does not exist in the order, it creates a new sale order line for it.
        - Adjusts the sequence of sub-products in the sale order.
        - Updates the total price of the main kit product based on its components.
        """
        if self.sale_order_line_id.is_kit:
            sale_order_line = self.sale_order_line_id
            order = sale_order_line.order_id
            main_product_sequence = sale_order_line.sequence
            total_subproduct_price = 0.0

            for index, line in enumerate(self.kit_subproducts_ids, start=1):
                component = sale_order_line.kit_component_ids.filtered(
                    lambda c: c.kit_component_id.id == line.product_id.id
                )
                if component:
                    component.write({
                        'kit_qty': line.quantity,
                        'price': line.price
                    })
                existing_line = order.order_line.filtered(
                    lambda ol: ol.product_id == line.product_id and
                    ol.is_kit_component
                )
                if existing_line:
                    existing_line.write({
                        'product_uom_qty': line.quantity,
                        'price_unit': 0.0,
                        'sequence': main_product_sequence + index
                    })
                else:
                    self.env['sale.order.line'].create({
                        'order_id': order.id,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.quantity,
                        'price_unit': 0.0,
                        'is_kit_component': True,
                        'kit_parent_line_id': sale_order_line.id,
                        'sequence': main_product_sequence + index
                    })
                total_subproduct_price += line.total_price
                sale_order_line.write({
                    'price_unit': sale_order_line.price_unit + total_subproduct_price
                })


class ProductKitLine(models.TransientModel):
    _name = 'product.kit.line'
    _description = "Wizard Line for Sub Products"

    product_kit_id = fields.Many2one(
        'product.kit', string="Product Kit",
        help="Reference to the product kit wizard"
    )
    product_id = fields.Many2one(
        'product.product', string="Product",
        help="Main product of the kit"
    )
    kit_component_id = fields.Many2one(
        'product.kit.component', string="Kit Component",
        help="Sub-product of the kit"
    )
    quantity = fields.Integer(string="Quantity", required=True, default=1)
    price = fields.Float(string="Price", required=True, default=0.0)
    total_price = fields.Float(string="Total Price", compute="_compute_total_price", store=True)

    @api.depends('quantity', 'price')
    def _compute_total_price(self):
        """
        Computes the total price of the kit component in the wizard.
        - Formula: total_price = quantity * price
        - Ensures total price is calculated only if both quantity and price are set.
        """
        for line in self:
            line.total_price = line.quantity * line.price
