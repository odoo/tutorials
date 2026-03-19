from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property model"
    _order = "id desc"

    name = fields.Char("Title", required=True, size=100)
    description = fields.Text(
        "Description", help="write the description of this property",
    )
    postcode = fields.Char("Postcode", size=10, help="address postal code")
    date_availability = fields.Date(
        "Available From",
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float("Expected Price", default=0.00, required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2, help="Number of Bedrooms")
    living_area = fields.Integer("Living Area(sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Garden", default=False)
    garden_area = fields.Integer("Garden Area(sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean("active", default=True)
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
        default="new",
        copy=False,
        readonly=True,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many(
        "estate.property.tag", "estate_propery_tags_relation", string="Tags",
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, readonly=True)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user,
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer("Total Area", compute="_compute_total", readonly=True)
    best_price = fields.Float(
        "Best Price", readonly=True, compute="_compute_best_price", store=True,
    )

    _check_selling_and_expected_price = models.Constraint(
        "CHECK(selling_price >= 0 and expected_price > 0)",
        "expected price must be higher than 0 and selling price must be positive",
    )
    _check_bedrooms_and_facades = models.Constraint(
        "CHECK(bedrooms >= 0 and facades >= 0)",
        "bedrooms & facades can't be less than 0",
    )
    _check_living_and_garden_area = models.Constraint(
        "CHECK(living_area >= 0 and garden_area >= 0)",
        "living_area & garden_area can't be less than 0",
    )

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for rec in self:
            rec.total_area = rec.garden_area + rec.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.offer_ids.mapped("price")) if rec.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_not_in(self):
        for rec in self:
            if rec.state not in ("new", "cancelled"):
                raise UserError(_("Only New and Cancelled property can be deleted"))

    def action_mark_as_sold(self):
        for rec in self:
            if rec.state == "cancelled":
                raise UserError(_("Cancelled Property can't be SOLD"))
            rec.state = "sold"
        return True

    def action_mark_as_cancelled(self):
        for rec in self:
            if rec.state == "sold":
                raise UserError(_("SOLD Property can't be CANCELLED"))
            rec.state = "cancelled"
        return True

    def action_mark_sold_multi(self):
        for rec in self:
            if rec.state == "cancelled":
                raise UserError(_("Cancelled Property can't be SOLD"))
            rec.state = "sold"
        return True


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", "salesperson_id", string="Estate Properties",
    )
