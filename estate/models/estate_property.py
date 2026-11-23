from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _explanation = "Real Estate Property"

    title = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    # The One2many needs the inverse field name.
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(compute="_compute_total")
    best_price = fields.Float(compute="_highest_price", string="Best Offer")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "A property expected price must be strictly positive.",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "A property selling price must be positive.",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids")
    def _highest_price(self):
        for offers in self:
            if not offers.offer_ids:
                offers.best_price = 0.0
            else:
                offers.best_price = max(offers.offer_ids.mapped("price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for property in self:
            if property.state == "cancelled":
                raise UserError(
                    self.env._("Cancelled properties cannot be sold.")
                )  # env._ to translate on the right language
            property.state = "sold"
            return True

    def action_cancelled(self):
        for property in self:
            if property.state == "sold":
                raise UserError(self.env._("Sold properties cannot be cancelled."))
            property.state = "cancelled"
            return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for property in self:
            if property.state in {"new", "offer_received"}:
                return True
            if (
                fields.Float.compare(
                    property.selling_price * 0.9, property.expected_price, precision_digits=2
                )
                < 0
            ):
                raise ValidationError(
                    self.env._("The selling price cannot be lower than 90% of the expected price.")
                )
