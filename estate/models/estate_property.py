from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _oder = "id desc"

    name = fields.Char(required=True)

    property_tag_ids = fields.Many2many("estate.property.tag")

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        required=True,
    )
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )

    expected_price = fields.Float(required=True)
    best_price = fields.Float(
        string="Best Price",
        compute="_compute_best_price",
    )
    selling_price = fields.Float(readonly=True, copy=False)

    description = fields.Text()
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
        ],
        help="Select the orientation of the property.",
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
    )

    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, readonly=True)
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )

    offer_ids = fields.One2many(
        "estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )

    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
    active = fields.Boolean(default=True)

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "Property expected price must be strictly positive.",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price > 0)",
        "Property selling price must be strictly positive.",
    )

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for property in self:
            if (
                not float_is_zero(property.selling_price, precision_digits=2)
                and float_compare(
                    property.selling_price,
                    property.expected_price * 0.9,
                    precision_digits=2,
                )
                == -1
            ):
                raise ValidationError(
                    self.env._(
                        "Selling price need to be higher than 90% of the expected price",
                    ),
                )

    @api.depends("living_area", "garden", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + (
                property.garden_area if property.garden else 0
            )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        has_garden = self.garden
        self.garden_area = 10 if has_garden else 0
        self.garden_orientation = "north" if has_garden else False

    def action_property_sold(self):
        self.ensure_one()
        if self.state == "sold":
            raise ValidationError(self.env._("Already sold property"))
        if self.state == "cancelled":
            raise ValidationError(self.env._("Can't sold a cancelled property"))

        self.state = "sold"
        return True

    def action_property_refused(self):
        self.ensure_one()
        if self.state == "sold":
            raise ValidationError(self.env._("Can't cancel an already sold property"))
        if self.state == "cancelled":
            raise ValidationError(self.env._("Already cancelled property"))

        self.state = "cancelled"
        return True
