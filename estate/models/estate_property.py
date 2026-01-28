from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, exceptions
from odoo.tools.float_utils import float_compare


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property app like immoweb"
    _order = "id desc"

    # computed fields
    total_area = fields.Float(string="Total Area", compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    # constraints
    _positive_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected price should be (strictly) positive'
    )
    _positive_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price should be positive'
    )

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    offer_ids = fields.One2many("estate.property.offer", string="Offers", inverse_name="property_id")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    salesman = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.uid)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    date_availability = fields.Date(string="Available From", default=fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer('Color Index', compute="_compute_color")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ]
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        readonly=True,
        default="new"
    )

    @api.depends("state")
    def _compute_color(self):
        for record in self:
            if record.state == "sold":
                record.color = 10  # Green
            elif record.state == "cancelled":
                record.color = 1   # Red
            elif record.state == "offer_received":
                record.color = 4   # Blue
            elif record.state == "offer_accepted":
                record.color = 3   # Light Green/Yellowish
            else:
                record.color = 0

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = None
        else:
            self.garden_area = 10
            self.garden_orientation = "north"

    def sell_property(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError("You cannot sell a cancelled property")
            else:
                record.state = "sold"
        return True

    def cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("You cannot cancel a sold property")
            else:
                record.state = "cancelled"
        return True

    @api.constrains("state", "offer_ids")
    def _check_selling_price(self):
        for record in self:
            for offer in record.offer_ids:
                if offer.status == "accepted" and float_compare(offer.price, 0.9 * record.expected_price, 2) == -1:
                    raise exceptions.UserError("Selling price should be at least 90 percent of the expected price")

    @api.ondelete(at_uninstall=False)
    def unlink_property(self):
        for property in self:
            if property.state in ("sold", "cancelled"):
                raise exceptions.UserError("You cannot delete a property that has existing offers")
