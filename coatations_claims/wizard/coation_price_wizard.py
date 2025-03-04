from odoo import api, fields, models


class CoatationPriceWizard(models.TransientModel):
    _name = "coatation.price.wizard"
    _description = "Select negotiated price on the sales order form"
    coation_ids = fields.Many2one("coatations.claims", string="Coatations Claims",required=True)
    coation_lines_ids = fields.One2many(
        "coatations.lines",
        related="coation_ids.coation_lines_ids",
        string="Coatation Lines",
    )
    order_line_id = fields.Many2one(
        "sale.order.line", string="Order Line", readonly=True
    )  # Reference to the sale order line
    customer_id = fields.Many2one(
        "res.partner",
        related="order_line_id.order_id.partner_id",
        string="Customer",
        readonly=True,
    )  # Related to the sales order
    domain_ids = fields.Char(
        string="Custome Domain",
        help="dynamic domain used for mapped customers",
        compute="_compute_coation_ids_domain",
    )
    recommended_selling_price = fields.Float(
        string="Recommended Selling Price", compute="_compute_recommended_selling_price"
    )  # this extra field is for gui aesthic purpose it displays only one line instead of multiple tables
    last_sales_order_unit_price = fields.Float(
        string="Last Sales Order Unit Price",
        compute="_compute_last_sales_order_unit_price",
    )
    type_of_price = fields.Selection(
        selection=[
            ("regular", "Regular price"),
            ("coatation", "Coatation price"),
            ("last", "Last selling price"),
        ],default="regular",required=True
    )

    @api.model_create_multi
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get("active_id")
        if active_id:
            res.update({"order_line_id": active_id})
        return res

    @api.depends("coation_ids", "coation_lines_ids")
    def _compute_coation_ids_domain(self):
        for coationID in self:
            active_id = self.env.context.get("active_id")
            product_id = self.env["sale.order.line"].browse(active_id).product_id.id
            sale_order_id = self.env["sale.order.line"].browse(active_id).order_id
            client_id = sale_order_id.partner_id.id
            product = self.env["product.product"].browse(product_id)
            coatation_lines = self.env["coatations.lines"].search(
                [
                    ("product_id", "=", product.id),
                    ("coation_id.client_id", "=", client_id),
                    ("status", "=", "active"),
                ]
            )
            coatation_ids = coatation_lines.mapped("coation_id.id")
            coationID.domain_ids = [("id", "in", coatation_ids)]

    @api.depends("coation_ids")
    def _compute_recommended_selling_price(self):
        for wizard in self:
            # the recommended_sp values from the related `coatations.lines`
            wizard.recommended_selling_price = wizard.coation_lines_ids.recommended_sp
            print(wizard.recommended_selling_price)

    @api.depends("order_line_id.price_unit")
    def _compute_last_sales_order_unit_price(self):
        """
        Computes the last sales order unit price by retrieving the most recent sale order line
        associated with the same product and client.
        """
        active_id = self.env.context.get("active_id")
        sale_order_line = self.env["sale.order.line"].browse(active_id)
        product_id = sale_order_line.product_id.id
        sale_order_id = sale_order_line.order_id
        client_id = sale_order_id.partner_id.id

        # Query for sale order lines matching the product and customer (partner)
        sale_order_lines = self.env["sale.order.line"].search(
            [
                ("product_id", "=", product_id),
                ("order_id.partner_id", "=", client_id),
                (
                    "order_id.state",
                    "in",
                    ["sale", "done"],
                ),  # Only confirmed or done orders
            ]
        )

        # Sort order lines by the associated sale order creation date (not order line date)
        sorted_sale_order_lines = sorted(
            sale_order_lines, key=lambda line: line.order_id.create_date, reverse=True
        )

        last_unit_price = 0
        if sorted_sale_order_lines:
            # Take the most recent sale order line and get its price unit
            most_recent_line = sorted_sale_order_lines[0]
            last_unit_price = most_recent_line.price_unit

        for wizard in self:
            wizard.last_sales_order_unit_price = last_unit_price


    def action_select_price(self):
        """
        Method to process the selected price and update the sales order line or take further actions.
        This method will apply either the coation price (recommended selling price),
        the last sales order price (if it exists), or the regular price of the product.
        """
        if self.type_of_price == "regular":
            # When the user selects 'regular' price, fetch the price from the product.
            product = self.order_line_id.product_id  # Get the product from the sales order line
            selected_price = product.list_price  # This is the regular price from the product

        elif self.type_of_price == "last":
            # If 'last' price is selected, use the last sales order price
            last_sales_order_price = self.last_sales_order_unit_price
            if last_sales_order_price:
                # If a last sale order line exists, use its price unit
                selected_price = last_sales_order_price

        elif self.type_of_price == "coatation":
            # If 'coatation' price is selected, use the recommended selling price
            selected_line = self.coation_lines_ids[0]
            selected_price = selected_line.recommended_sp

        else:
            # If no price type is selected, do nothing (or raise an error)
            return False

        # Update the order line's price_unit based on the selected price
        if selected_price is not None:
            self.order_line_id.price_unit = selected_price
        else:
            # In case no price is found (should not happen), fallback to a default value
            self.order_line_id.price_unit = 0.0  # Or some default value

        return True

