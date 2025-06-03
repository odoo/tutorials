from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price of a property must be positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "The selling price of a property must be positive.",
        ),
    ]
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Date.today() + relativedelta(months=3), copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman = fields.Many2one("res.users", default=lambda self: self.env.user)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    buyer = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="This is Garden orientation described in directions",
    )
    total_area = fields.Integer(compute="_compute_total_area")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for prp in self:
            prp.total_area = prp.garden_area + prp.living_area

    best_price = fields.Float(string="Best offer", compute="_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prp in self:
            pricelist = prp.mapped("offer_ids.price")
            if len(pricelist) > 0:
                prp.best_price = max(pricelist)
            else:
                prp.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def set_sold_state(self):
        if self.state != "cancelled":
            if self.state == "offer_accepted":
                self.state = "sold"
            else:
                raise UserError("Only Accepeted offers property can be sold")
        else:
            raise UserError("Cancelled property can not be sold.")
        return True

    def set_cancelled_state(self):
        if self.state != "sold":
            self.state = "cancelled"
        else:
            raise UserError("Sold property can not be cancelled.")
        return True

    @api.constrains("selling_price, expected_price")
    def _check_selling_price(self):
        for record in self:
            if (
                record.selling_price
                and record.expected_price
                and record.selling_price < record.expected_price * 0.9
            ):
                raise ValidationError(
                    "The selling_price cannot be lower than 90% of the expected price"
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for rcd in self:
            if rcd.state not in ("new", "cancelled"):
                raise UserError("Only New and Cancelled property can be deleted.")
