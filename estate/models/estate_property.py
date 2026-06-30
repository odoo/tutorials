from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True, default="Unknown")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3),
    )
    expected_price = fields.Float(
        string="Expected Price", required=True, digits=(16, 4)
    )
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        copy=False,
        default="new",
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(
        string="Total Area (sqm)", compute="_compute_total_area"
    )
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "A property expected price must be strictly positive.",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "A property selling price must be positive."
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = (
                max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("You can not sold a cancelled property.")
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("You can not cancel a sold property.")
            record.state = "cancelled"
        return True
