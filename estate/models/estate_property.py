from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    # Attributes
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    # Fields
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
        index=True,
    )
    active = fields.Boolean(default=True)

    # Relational Fields
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Computed Fields
    total_area = fields.Integer(
        string="Total Area (sqm)", compute="_compute_total_area"
    )
    best_price = fields.Float(
        string="Best Offer", compute="_compute_best_price", store=True
    )

    # SQL Constraints
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive.",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price must be positive.",
    )

    # Compute / Inverse Methods
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = record.offer_ids[0].price if record.offer_ids else 0.0

    # Onchange Methods
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # Constrains Methods
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_ratio(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01) < 0:
                    raise UserError(self.env._("The selling price cannot be lower than 90% of the expected price!"))

    # Helper Methods
    def _check_new_offer_price(self, price):
        self.ensure_one()
        if self.offer_ids and price <= self.offer_ids[0].price:
            raise UserError(self.env._("The offer amount must be strictly higher than existing offers."))

    def _accept_offer(self, buyer, price):
        self.ensure_one()
        if self.buyer_id:
            raise UserError(self.env._("An offer has already been accepted for this property."))
        self.write({
            "buyer_id": buyer.id,
            "selling_price": price,
            "state": "offer_accepted",
        })

    # CRUD Methods
    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_or_cancelled(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError(self.env._("Only new and cancelled properties can be deleted."))

    # Action Methods
    def action_cancel(self):
        if self.filtered(lambda record: record.state == "sold"):
            raise UserError(self.env._("A sold property cannot be cancelled."))
        self.write({"state": "cancelled"})
        return True

    def action_sold(self):
        if self.filtered(lambda record: record.state == "cancelled"):
            raise UserError(self.env._("A cancelled property cannot be sold."))
        if self.filtered(lambda prop: prop.state != "offer_accepted"):
            raise UserError(self.env._("A property can only be sold if an offer has been accepted."))
        self.write({"state": "sold"})
        return True
