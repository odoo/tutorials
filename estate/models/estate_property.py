from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Model"
    _order = "id desc"

    name = fields.Char("Title", required=True, translate=True)
    description = fields.Text(string="Description", required=True, translate=True)
    postcode = fields.Char("Postcode", required=True)
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", required=True, default=2)
    living_area = fields.Integer("Living Area (sqm)", required=True)
    facades = fields.Integer("Facades", required=True)
    garage = fields.Boolean("Garage", required=True)
    garden = fields.Boolean("Garden", required=True)
    garden_area = fields.Integer("Garden Area")
    active = fields.Boolean(string="Active", required=True, default=True)

    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.today() + relativedelta(months=3),
    )

    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Mucho calor o poco calor",
    )

    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        copy=False,
        default="new",
    )

    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    property_offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )

    total_area = fields.Float(compute="_compute_total_area", string="Total Area (sqm)")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("property_offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            if len(property.property_offer_ids) > 0:
                property.best_price = max(
                    offer.price for offer in property.property_offer_ids
                )
            else:
                property.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def sell_property(self):
        for property in self:
            if property.state == "cancelled":
                raise UserError(self.env._("Cancelled properties cannot be sold"))
            if property.state in ["offer_accepted", "sold"]:
                raise UserError(self.env._("Property is already sold"))
            property.state = "sold"
        return True

    def cancel_property(self):
        for property in self:
            if property.state == "cancelled":
                raise UserError(self.env._("Property is already cancelled"))
            if property.state in ["offer_accepted", "sold"]:
                raise UserError(self.env._("Sold properties cannot be cancelled"))
            property.state = "cancelled"
        return True

    _check_expected_price = models.Constraint(
        "CHECK(expected_price >= 0)",
        "The expected price should be positive",
    )
    _check_bedrooms = models.Constraint(
        "CHECK(bedrooms >= 0)",
        "The amount of bedrooms should be at least 0",
    )
    _check_living_area = models.Constraint(
        "CHECK(living_area >= 0)",
        "The living area should be at least 0",
    )
    _check_facades = models.Constraint(
        "CHECK(facades >= 0)",
        "The amount of facades should be at least 0",
    )
    _check_garden_area = models.Constraint(
        "CHECK(garden_area >= 0)",
        "The garden area should be at least 0",
    )

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for property in self:
            if property.selling_price < 0.9 * property.expected_price:
                raise ValidationError(
                    self.env._(
                        "Selling price cannot be lower than ninety percent of expected price",
                    ),
                )

    @api.ondelete(at_uninstall=False)
    def _prevent_unlink_if_new_or_cancelled(self):
        if any(property.state not in ("new", "cancelled") for property in self):
            raise UserError(self.env._("Can only delete New or Cancelled properties"))
