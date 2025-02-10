from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id"

    name = fields.Char(required=True)
    tag_ids = fields.Many2many("estate.property.tag", string="tags")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Datetime.today() + relativedelta(days=90),
    )
    salesperson_id = fields.Many2one(
        "res.partner",
        string="Salesperson",
        default=lambda self: self.env.user.partner_id,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute="_compute_best_price")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    property_type_id = fields.Many2one("estate.property.type")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()

    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("west", "West"),
            ("south", "South"),
        ],
        help="Type is used to separate Leads and Opportunities",
    )
    total_area = fields.Integer(compute="_compute_total_area")
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "cancelled"),
        ],
        help="Type is used to separate Leads and Opportunities",
        required=True,
        default="new",
        copy=False,
    )
    active = True
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    _sql_constraints = [
        (
            "positive_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price cannot be negative.",
        ),
        (
            "positive_selling_price",
            "CHECK(selling_price > 0)",
            "Selling_price cannot be negative.",
        ),
        ("unique_property_name", "UNIQUE(name)", "Property name should be unique"),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            offer_prices = record.offer_ids.mapped("price")
            record.best_price = max(offer_prices) if offer_prices else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if self.garden:
                self.garden_area = 10
                self.garden_orientation = "north"
            else:
                self.garden_orientation = ""
                self.garden_area = 0

    def sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled property cannot be sold.")
            record.state = "sold"

    def cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be cancelled.")
            record.state = "cancelled"

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < record.expected_price * 0.9:
                raise ValidationError(
                    "Price cannot be less than 90 percent of the expected price"
                )
            else:
                record.state = "sold"

    def unlink(self):
        for record in self:
            if record.state not in ['new','cancelled']:
                raise ValidationError("Cant Delete a property that is not New or Cancelled")
        return super(EstateProperty, self).unlink()
