from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CoationsLines(models.Model):
    _name = "coatations.lines"
    _description = "List of all coatations"

    product_id = fields.Many2one("product.product")
    coatation_unit_price = fields.Float()
    max_qty = fields.Integer()
    min_qty = fields.Integer()
    qty_per_order = fields.Integer()
    recommended_sp = fields.Float(
        help="Keep 0 to apply last coatation selling price if not available set the price accordingly."
    )
    consumed = fields.Integer(compute="_compute_consumed", readonly=True)
    status = fields.Selection(
        string="state",
        selection=[("active", "Active"), ("expired", "Expired")],
        required=True,
        compute="_compute_state",
        default="active",
        readonly=True,
        store=True,
    )
    claim = fields.Boolean()
    coation_id = fields.Many2one("coatations.claims")
    internal_reference = fields.Char(compute="_compute_internal_reference", store=True)
    sale_order_ids = fields.Many2many("sale.order")
    last_applied_price = fields.Float(
        compute="_compute_last_applied_price", store=True
    )  # Computed field for last applied price
    name = fields.Char()

    _sql_constraints = [
        # Ensuring max_qty is positive
        (
            "positive_max_qty",
            "CHECK(max_qty > 0)",
            "Maximum quantity must be greater than zero!",
        ),
        # Ensuring min_qty is positive
        (
            "positive_min_qty",
            "CHECK(min_qty > 0)",
            "Minimum quantity must be greater than zero!",
        ),
        # Ensuring qty_per_order is positive
        (
            "positive_qty_per_order",
            "CHECK(qty_per_order > 0)",
            "Quantity per order must be greater than zero!",
        ),
        # Ensuring coatation_unit_price is positive
        (
            "positive_coatation_unit_price",
            "CHECK(coatation_unit_price > 0)",
            "Coatation unit price must be greater than zero!",
        ),
        # Ensuring max_qty is greater than min_qty
        (
            "max_more_than_min",
            "CHECK(max_qty > min_qty)",
            "Maximum quantity should be more than minimum quantity!",
        ),
        # Ensuring recommended_sp is positive
        (
            "positive_recommended_sp",
            "CHECK(recommended_sp > 0)",
            "Recommended selling price must be greater than zero!",
        ),
        # Ensuring max_qty is greater than or equal to consumed only if not expired
        (
            "max_qty_greater_than_consumed",
            "CHECK(status = 'expired' OR max_qty >= consumed)",
            "Maximum quantity must be greater than or equal to consumed quantity if status is not expired!",
        ),
        # Ensuring consumed quantity is greater than or equal to zero
        (
            "positive_consumed_qty",
            "CHECK(consumed >= 0)",
            "Consumed quantity must be greater than or equal to zero!",
        ),
    ]

    def _set_last_sales_order_price(self):
        """Set the last applied sales order price for the product."""
        if not self.product_id or not self.coation_id:
            return

        # Find the last sale order line with the same product and coation_id
        sale_order_lines = self.env["sale.order.line"].search(
            [
                ("product_id", "=", self.product_id.id),
                ("order_id.partner_id", "=", self.coation_id.client_id.id),
                ("order_id.state", "in", ["sale", "done"]),
            ]
        )

        sorted_sale_order_lines = sorted(
            sale_order_lines, key=lambda line: line.order_id.create_date, reverse=True
        )

        if sorted_sale_order_lines:
            last_sale_order_line = sorted_sale_order_lines[0]
            last_unit_price = last_sale_order_line.price_unit

            # Set the last applied price (regardless of recommended_sp)
            self.last_applied_price = last_unit_price

            # If recommended_sp is not set (i.e., it is 0), apply the last sales price
            if self.recommended_sp == 0 or not self.recommended_sp:
                self.recommended_sp = last_unit_price

    @api.model_create_multi
    def create(self, vals_list):
        """Create method override to handle initial setup of last applied price on creation."""
        for vals in vals_list:
            vals["name"] = "Recommended selling price:" + str(vals["recommended_sp"])
        return super(CoationsLines, self).create(vals_list)

    @api.constrains("product_id", "coation_id")
    def _check_unique_product_for_coation(self):
        """
        Ensure that each product in a given coatation is unique.
        If the same product is added more than once for the same coation_id,
        raise a ValidationError.
        """
        for record in self:
            # Search for existing coatation lines with the same coation_id and product_id
            existing_lines = self.env["coatations.lines"].search(
                [
                    ("coation_id", "=", record.coation_id.id),
                    ("product_id", "=", record.product_id.id),
                    (
                        "id",
                        "!=",
                        record.id,
                    ),  # Exclude the current record to avoid self-comparison
                ]
            )

            if existing_lines:
                raise ValidationError(
                    f"The product '{record.product_id.name}' has already been added to the quotation."
                    " Each product must be unique within a coatation."
                )

    @api.depends("product_id")
    def _compute_last_applied_price(self):
        """Computes the last applied price based on the product_id."""
        for record in self:
            record._set_last_sales_order_price()

    @api.depends("coation_id")
    def _compute_internal_reference(self):
        for reference in self.coation_id:
            if reference and reference.name != "New":
                self.internal_reference = reference.name
            else:
                self.internal_reference = ""

    @api.depends("sale_order_ids.order_line.product_uom_qty")
    def _compute_consumed(self):
        for record in self:
            if record.status == "expired":
                record.consumed = record.max_qty  # Skip processing for expired records
            else:
                total_consumed = 0
                sale_order_lines = self.env["sale.order.line"].search(
                    [
                        ("order_id.partner_id", "=", record.coation_id.client_id.id),
                        ("product_id", "=", record.product_id.id),
                        ("order_id.state", "in", ["sale", "done"]),
                        ("coation_ids", "=", record.coation_id.id),
                    ]
                )

                # Sum the quantities of the matching order lines
                for line in sale_order_lines:
                    total_consumed += line.product_uom_qty

                # Assign the computed consumed value
                record.consumed = total_consumed
                record.write({"consumed": total_consumed})
                # print(
                #     f"Consumed for {record.product_id.name} and client {record.coation_id.client_id.name}: {total_consumed}"
                # )

    @api.depends("consumed", "coation_id.state")
    def _compute_state(self):
        print("computing coatation line state!!")
        for record in self:
            if not isinstance(record.id, models.NewId):
                if record.coation_id.state != "expired":
                    print("Parent coatation id coation_line line:187")
                    print(record.coation_id.state)
                    if record.status == "expired":
                        record.status = "expired"
                        continue  # Skip processing for expired records
                    # Check if consumed is properly initialized
                    if record.consumed != 0 and record.max_qty != 0:
                        print(
                            "calculating consumed and max quantity coation_line line:194"
                        )
                        print(record.consumed)
                        print(record.max_qty)
                        if record.consumed >= record.max_qty:
                            print("setting status")
                            record.status = "expired"
                            record.write({"status": record.status})
                        else:
                            record.status = "active"
                            record.write({"status": record.status})
                    else:
                        record.status = "active"
                        record.write({"status": record.status})
                        # Explicitly write the changes to the database
                else:
                    print("setting line status to expired")
                    record.status = "expired"
                    record.write({"status": record.status})
            else:
                record.status = "active"
                record.write({"status": record.status})
