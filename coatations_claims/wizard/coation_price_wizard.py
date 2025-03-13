from odoo import api, fields, models


class CoatationPriceWizard(models.TransientModel):
    _name = "coatation.price.wizard"
    _description = "Select negotiated price on the sales order form"

    # =====================================
    # Field Definitions
    # =====================================
    coation_id = fields.Many2one("coatations.claims", string="Coatations Claims")
    coation_lines_ids = fields.One2many(
        "coatations.lines",
        related="coation_id.coation_lines_ids",
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
        string="Custom Domain",
        help="dynamic domain used for mapped customers",
        compute="_compute_coation_ids_domain",
    )
    recommended_selling_price = fields.Float(
        string="Recommended Selling Price", compute="_compute_recommended_selling_price"
    )  # this extra field is for gui aesthetic purpose it displays only one line instead of multiple tables
    last_sales_order_unit_price = fields.Float(
        string="Last Sales Order Unit Price",
        compute="_compute_last_sales_order_unit_price",
    )
    type_of_price = fields.Selection(
        selection=[
            ("regular", "Regular price"),
            ("coatation", "Coatation price"),
            ("last", "Last selling price"),
        ],
        default="regular",
        required=True,
    )

    # =====================================
    # Activity Handling Methods
    # =====================================
    def _create_activity_for_expired_quotation(self, coatation_line):
        """
        Creates an activity to remind the user about the expired quotation.
        This activity will be linked to the related partner (customer) of the quotation.
        """
        created_reminder = self.env["mail.activity"].search(
            [("note", "=", coatation_line.coation_id.name)]
        )

        if not created_reminder:
            self.order_line_id.order_id.activity_schedule(
                "mail.mail_activity_data_todo",
                user_id=self.env.user.id,
                date_deadline=coatation_line.coation_id.date_to,
                summary="Finalize quotation",
                note=coatation_line.coation_id.name,
            )

    # =====================================
    # Initialization Methods
    # =====================================
    @api.model_create_multi
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get("active_id")
        if active_id:
            res.update({"order_line_id": active_id})
        return res

    # =====================================
    # Price Computation Methods
    # =====================================
    @api.depends("coation_id", "coation_lines_ids.status")
    def _compute_coation_ids_domain(self):
        for wizard in self:
            wizard.domain_ids = [
                (
                    "coation_lines_ids.product_id",
                    "=",
                    wizard.order_line_id.product_id.id,
                ),
                ("client_id", "=", wizard.order_line_id.order_id.partner_id.id),
                ("coation_lines_ids.status", "=", "active"),
            ]

    @api.depends("coation_id")
    def _compute_recommended_selling_price(self):
        for wizard in self:
            if wizard.coation_id:
                line = wizard.coation_id.coation_lines_ids
                try:
                    index = line.product_id.ids.index(
                        wizard.order_line_id.product_id.id
                    )
                    wizard.recommended_selling_price = line[index].recommended_sp
                except ValueError:
                    wizard.recommended_selling_price = 0
            else:
                wizard.recommended_selling_price = 0

    @api.depends("order_line_id.price_unit")
    def _compute_last_sales_order_unit_price(self):
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

    # =====================================
    # Price Selection Action
    # =====================================
    def action_select_price(self):
        """
        Method to process the selected price and update the sales order line or take further actions.
        This method will apply either the coation price (recommended selling price),
        the last sales order price (if it exists), or the regular price of the product.
        """
        selected_price = None
        selected_coation_id = None
        Reminder_created = False

        # Select price type
        if self.type_of_price == "regular":
            # Regular price selected
            product = self.order_line_id.product_id
            selected_price = product.list_price

        elif self.type_of_price == "last":
            # Last sales order price selected
            selected_price = self.last_sales_order_unit_price

        elif self.type_of_price == "coatation":
            # Coatation price selected
            for line in self.coation_lines_ids:
                if line.product_id == self.order_line_id.product_id:
                    selected_price = line.recommended_sp
                    selected_coation_id = line.coation_id.id
                    if not Reminder_created:
                        self._create_activity_for_expired_quotation(line)
                        Reminder_created = True
                    break

        # If no valid price was found, do nothing
        if selected_price is None:
            return False

        # Update the sales order line with the selected price
        self.order_line_id.price_unit = selected_price
        self.order_line_id.type_of_price = self.type_of_price

        # If coatation price is selected, set the coation_id
        if self.type_of_price == "coatation" and selected_coation_id:
            self.order_line_id.coation_ids = selected_coation_id
        else:
            # If not coatation, clear the coation_ids
            self.order_line_id.coation_ids = None

        return True
