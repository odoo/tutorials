from odoo.tools.float_utils import float_compare, float_is_zero

from odoo import api, exceptions, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate properties"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)", default=30)
    facades = fields.Integer("Facades", default=1)
    garage = fields.Boolean("Has Garage")
    garden = fields.Boolean("Has Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, readonly=True)
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id", string="Offers")
    total_area = fields.Integer(string="Total Area (sqm)", copy=False, readonly=True, compute="_compute_total_area")
    best_price = fields.Float(string="Best Price", copy=False, readonly=True, compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "Property expected price must be strictly positive.",
    )

    _check_bedrooms = models.Constraint(
        "CHECK(bedrooms > 0)",
        "Property must have at least 1 bedroom.",
    )

    _check_garden_area = models.Constraint(
        "CHECK(garden_area >= 0)",
        "Property garden area must be positive",
    )

    _check_living_area = models.Constraint(
        "CHECK(living_area >= 0)",
        "Property living area must be positive.",
    )

    _check_facades = models.Constraint(
        "CHECK(facades > 0 AND facades <= 4)",
        "Property facades must be between 1 and 4",
    )

    @api.depends("living_area", "garden", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + (property.garden_area if property.garden else 0)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped("price")) if property.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        for property in self:
            has_garden = property.garden
            property.garden_area = 10 if has_garden else 0
            property.garden_orientation = "north" if has_garden else None

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
                raise exceptions.ValidationError(
                    "selling price cannot be lower than 90% of the expected price"
                )

    def action_property_sold(self):
        self.ensure_one()
        if self.state == "sold":
            raise exceptions.ValidationError("Already sold property")
        if self.state == "cancelled":
            raise exceptions.ValidationError("Can't sold a cancelled property")
        self.state = "sold"
        return True

    def action_property_refused(self):
        self.ensure_one()
        if self.state == "cancelled":
            raise exceptions.ValidationError("Already cancelled property")
        if self.state == "sold":
            raise exceptions.ValidationError("Can't cancel an already sold property")
        self.state = "cancelled"
        return True
