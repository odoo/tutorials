from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CoatationPriceWizard(models.TransientModel):
    _name = "coatation.price.wizard"
    _description = "Select negotiated price on the sales order form"
    coation_ids = fields.Many2one("coatations.claims", string="Coatations Claims")
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
        string="Custom Domain",
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
        ],
        default="regular",
        required=True,
    )

    def _create_activity_for_expired_quotation(self,coatation_line):
        """
        Creates an activity to remind the user about the expired quotation.
        This activity will be linked to the related partner (customer) of the quotation.
        """
        print("CREATING ACTIVITY!!!!!!!!!!")
        # Create an activity (e.g., a todo task) for the expired quotation
        activity_type = self.env["mail.activity.type"].search(
            [("id", "=", "4")], limit=1
        )

        if not activity_type:
            raise ValidationError("No 'To Do' activity type found.")

        # Create the activity linked to the partner (customer)
        created_reminder = self.env["mail.activity"].search([("note",'=',coatation_line.coation_id.name)])
        print(created_reminder)
        if not created_reminder:
            self.env["mail.activity"].create(
                {
                    "summary": " Finalize quotation",
                    "activity_type_id": activity_type.id,
                    "res_model_id": self.env["ir.model"]._get_id("sale.order"),
                    "res_id": self.order_line_id.order_id.id,  
                    "date_deadline": coatation_line.coation_id.date_to,  
                    "user_id": self.env.user.id, 
                    "res_name":self.order_line_id.order_id.name,
                    "note":coatation_line.coation_id.name
                }
            )
            print(
                "Activity created for quotation."
            )
        else:
            print("reminder has already been created!!!")

    @api.model_create_multi
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get("active_id")
        if active_id:
            res.update({"order_line_id": active_id})
        return res

    def _fetch_coatation_records(self):
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
        return coatation_lines, coatation_ids

    @api.depends("coation_ids", "coation_lines_ids.status")
    def _compute_coation_ids_domain(self):
        for coationID in self:
            coatation_lines, coatation_ids = self._fetch_coatation_records()
            print(coatation_lines)
            coationID.domain_ids = [("id", "in", coatation_ids)]

    @api.depends("coation_ids")
    def _compute_recommended_selling_price(self):
        for wizard in self:
            # Fetch coation lines and coation ids that match the product and client
            coatation_lines, coatation_ids = self._fetch_coatation_records()
            print("Coatation Lines:", coatation_lines)
            print("Coatation IDs:", coatation_ids)

            # Initialize recommended_selling_price
            wizard.recommended_selling_price = 0.0

            # Check if the wizard's coation_id matches the coation_id list
            if wizard.coation_ids.id in coatation_ids:
                # Filter the coatation lines that correspond to the wizard's selected coation_id
                matching_lines = [
                    line
                    for line in coatation_lines
                    if line.coation_id.id == wizard.coation_ids.id
                ]

                # Now, if matching lines exist, get the recommended selling price for the product
                if matching_lines:
                    for line in matching_lines:
                        # Match the product in the coatation line and get its recommended price
                        if line.product_id == wizard.order_line_id.product_id:
                            wizard.recommended_selling_price = line.recommended_sp
                            break  # Exit the loop once a match is found

                print("Recommended Selling Price:", wizard.recommended_selling_price)
            else:
                print("No matching coatation_id found.")

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
        selected_price = None
        # Start by checking if the price type is 'regular'
        if self.type_of_price == "regular":
            # When the user selects 'regular' price, fetch the price from the product.
            product = (
                self.order_line_id.product_id
            )  # Get the product from the sales order line
            selected_price = (
                product.list_price
            )  # This is the regular price from the product

        elif self.type_of_price == "last":
            # If 'last' price is selected, use the last sales order price
            last_sales_order_price = self.last_sales_order_unit_price
            print("printing last order price!!!")
            print(last_sales_order_price)
            if last_sales_order_price:
                # If a last sale order line exists, use its price unit
                selected_price = last_sales_order_price

        elif self.type_of_price == "coatation":
            # If 'coatation' price is selected, use the recommended selling price
            # Match the product in the sales order line with the correct coatation line
            selected_price = None
            selected_coation_id = None  # Initialize the selected coation ID to None
            Reminder_created = False
            for line in self.coation_lines_ids:
                if line.product_id == self.order_line_id.product_id:
                    # If the product in the coatation line matches the order line's product
                    selected_price = line.recommended_sp
                    selected_coation_id = (
                        line.coation_id.id
                    )  # Get the corresponding coatation_id
                    if not Reminder_created:
                        self._create_activity_for_expired_quotation(line)
                        Reminder_created = True
                    break  # Exit once the matching product is found
            # If no matching coatation line is found, fall back to a default price or raise an error
            if not selected_price:
                return False  # Could also handle this with a fallback price or raise an error

        else:
            # If no price type is selected, do nothing (or raise an error)
            return False

        # Update the order line's price_unit based on the selected price
        if selected_price is not None:
            self.order_line_id.price_unit = selected_price
            self.order_line_id.type_of_price = self.type_of_price

            # If coatation price is selected, set the coation_id
            if self.type_of_price == "coatation" and selected_coation_id:
                print("Setting the coation_id for the sales order line:")
                print(
                    self.coation_ids.name
                )  # Print the selected coation ID name (for debugging)
                self.order_line_id.coation_ids = (
                    selected_coation_id  # Set the selected coation ID
                )
                # self._create_activity_for_expired_quotation()
            else:
                # If regular or last price is selected, clear the coation ID
                self.order_line_id.coation_ids = None

        else:
            # In case no price is found (should not happen), fallback to a default value
            print("fall back else is selected")
            product = (
                self.order_line_id.product_id
            )  # Get the product from the sales order line
            self.order_line_id.price_unit = product.list_price  # Use the regular price
            self.order_line_id.type_of_price = "regular"
            self.order_line_id.coation_ids = None

        return True
