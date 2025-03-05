from odoo import api, fields, models


class CoationsLines(models.Model):
    _name = "coatations.lines"
    _description = "List of all coations"
    product_id = fields.Many2one("product.product")
    coatation_unit_price = fields.Float()
    max_qty = fields.Integer()
    min_qty = fields.Integer()
    qty_per_order = fields.Integer()
    recommended_sp = fields.Float()
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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["name"] = "Recommended selling price:" + str(vals["recommended_sp"])
        return super(CoationsLines, self).create(vals_list)

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
            print(record.status)
            if record.status == "expired":
                record.consumed = record.max_qty  # Skip processing for expired records
            else:
                total_consumed = 0
                sale_order_lines = self.env["sale.order.line"].search(
                    [
                        ("order_id.partner_id", "=", record.coation_id.client_id.id),
                        ("product_id", "=", record.product_id.id),
                        (
                            "order_id.state",
                            "in",
                            ["sale", "done"],
                        ),  # Only consider confirmed or done orders
                    ]
                )

                # Sum the quantities of the matching order lines
                for line in sale_order_lines:
                    total_consumed += line.product_uom_qty

                # Assign the computed consumed value
                record.consumed = total_consumed
                record.write(
                    {"consumed": total_consumed}
                )  # added this because it helps the active status line change to expired
                print(
                    f"Consumed for {record.product_id.name} and client {record.coation_id.client_id.name}: {total_consumed}"
                )

    @api.depends("consumed")
    def _compute_state(self):
        for record in self:
            if record.status == "expired":
                continue  # Skip processing for expired records
            # Check if consumed is properly initialized
            if record.consumed is not None and record.max_qty is not None:
                if record.consumed >= record.max_qty:
                    record.status = "expired"
                else:
                    record.status = "active"
            else:
                # Default status if consumed is not initialized properly
                record.status = "active"
