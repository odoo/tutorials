from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Name", required=True, default="Unknown")
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    description = fields.Text(string="Description")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    postcode = fields.Char(string="Postcode", required=True)
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden_area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("west", "West"),
            ("south", "South"),
        ],
    )
    status = fields.Selection(
        string="Status",
        selection=[("saved", "Save"), ("cancelled", "Cancel")],
        readonly=True,
    )

    # If it is false then newly created record won't be appear. but record is created when active is set true record will appear.
    active = fields.Boolean("Active", default=True)
    # State can get selected and as copy is set False in duplicate it cannot get copied
    state = fields.Selection(
        string="state",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("accepted", "Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    buyer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Buyer",
        copy=False,
        default=lambda self: self.env.user.partner_id,
    )
    sales_person = fields.Many2one(
        comodel_name="res.users",
        string="Sales person",
        index=True,
        default=lambda self: self.env.user,
    )
    property_tag = fields.Many2many(
        comodel_name="estate.property.tag", string="Property Tags"
    )
    offer_id = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Property offer",
    )

    total_area = fields.Integer(
        string="total_area", name="Total area", compute="_compute_total"
    )
    best_price = fields.Integer(
        string="best_price", name="Best Price", compute="_compute_best_price"
    )

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_id.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.mapped("offer_id.price")
            record.best_price = max(prices) if prices else 0

    # to add when garden is clicked then its area and orientation is set to default values. works on decorators concepts
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel_offer(self):
        for record in self:
            if record.status == "saved":
                raise UserError("Saved properties can't be cancelled")
            else:
                record.status = "cancelled"

    def action_save_offer(self):
        for record in self:
            if record.status == "cancelled":
                raise UserError("Cancelled properties can't be saved")
            else:
                record.status = "saved"

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)", "Expected price must be positive"
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price > 0)", "Selling Price must be positive"
    )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_expected_price(self):
        for record in self:
            base = record.expected_price * 0.9
            if record.selling_price < base:
                raise ValidationError(
                    "Selling Price must be greater than 90 percent of expected price"
                )
