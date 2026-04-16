from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class Estate(models.Model):
    _name = "estate_property"
    _description = "real estate management"
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_available = fields.Date(
        string="Date available",
        copy=False,
        default=fields.Datetime.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
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
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "NEW"),
            ("offerRecieved", "OFFER RECIEVED"),
            ("offerAccepted", "OFFER ACCEPTED"),
            ("sold", "SOLD"),
            ("cancelled", "CANCELLED"),
        ],
        default="new",
        copy=False,
        required=True,
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property_type", string="Property Type"
    )
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    salesman_id = fields.Many2one(
        comodel_name="res.users", string="Salesman", default=lambda self: self.env.user
    )
    property_tag_ids = fields.Many2many(
        comodel_name="estate.property_tag", string="Property Tags"
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property_offer",
        inverse_name="property_id",
        string="Offers",
    )
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "A property selling price must be positive"
    )
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "A property expected price must be strictly positive",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_90(self):
        for record in self:
            if (
                record.selling_price
                and float_compare(
                    record.expected_price * 0.9,
                    record.selling_price,
                    precision_rounding=0.01,
                )
                == 1
            ):
                raise ValidationError(
                    "selling price must be least 90 percent of expected price"
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = False

    def mark_property_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("cancelled property can't be sold")
            record.state = "sold"
            return True

    def mark_property_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("sold property can't be canceled")
            record.state = "cancelled"
            return True
