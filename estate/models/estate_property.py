from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property details"
    _order = "id desc"

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description", required=True)
    postcode = fields.Char(string="Postcode")
    expected_price = fields.Float("Expected Price")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(
        string="Selling Price", default=0.0, readonly=True, copy=False
    )
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(default=True)
    status = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),  
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="new"
    )
    total_area = fields.Float(string="Total Aream(sqm)", compute="_compute_total_area")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type" ,ondelete="cascade")
    sequence = fields.Integer("Sequence", default=1)
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        ondelete="restrict",
        default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", ondelete="restrict", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    image = fields.Image("Image")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_id"
    )
    best_prices = fields.Float(string="Best Offer", compute="_compute_best_offer")

    _sql_constraints = [
        (
            "expected_price_positive",
            "CHECK(expected_price > 0)",
            "Expected Price must be strictly positive!",
        ),
        (
            "selling_price_positive",
            "CHECK(selling_price >= 0)",
            "Selling Price must be strictly positive!",
        ),
    ]

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_canceled(self):
        for record in self:
            if (
                record.status == "offer_received"
                or record.status == "offer_accepted"
                or record.status == "sold"
            ):
                raise UserError("Only new and canceled properties can be deleted")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if not record.offer_ids:
                record.best_prices = 0
                continue
            record.best_prices = max(record.offer_ids.mapped("price"))

    @api.onchange("garden")
    def onchange_check_garden_status(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if not record.offer_ids:
                raise UserError("A property cannot be sold without receiving at least one offer.")
            if record.status in ["new", "offer_accepted", "offer_received"]:
                record.status = "sold"
            elif record.status == "cancelled":
                raise UserError("Cancelled property can't be sold.")
            else:
                raise UserError("Property already sold.")

    def action_cancel(self):
        for record in self:
            if record.status == "sold":
                raise UserError("Sold property can't be canceled")
            if record.status == "cancelled":
                raise UserError("Property already canceled")
            record.status = "cancelled"
            