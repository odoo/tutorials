from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True, size=50)
    description = fields.Text()
    postcode = fields.Char(size=25)
    date_availability = fields.Date(
        copy=False, default=fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="Property State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    sales_man = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag = fields.Many2many("estate.property.tag", string="Tags")
    offer = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for records in self:
            records.total_area = records.living_area + records.garden_area

    @api.depends("offer.price")
    def _compute_best_price(self):
        for records in self:
            prices = records.mapped("offer.price")
            records.best_price = max(prices) if prices else 0

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "A property expected price must be strictly positive",
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "A property selling price must be positive",
    )

    @api.constrains("state")
    def on_state_change(self):
        for record in self:
            if record.state == "offer_accepted" or record.state == "sold":
                if float_compare(record.selling_price, record.expected_price * 0.9, 3) < 0:
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

    @api.onchange("garden")
    def _on_change_garden(self):
        for records in self:
            if records.garden:
                records.garden_area = 10
                records.garden_orientation = "north"
            else:
                records.garden_area = False
                records.garden_orientation = False

    def sold_button(self):
        for records in self:
            # breakpoint()
            if records.state == "cancelled":
                raise UserError("Cancelled property cannot be sold.")
            records.state = "sold"
            records.selling_price = records.selling_price
        return True

    def cancel_button(self):
        for records in self:
            if records.state == "sold":
                raise UserError("Sold property cannoy be cancelled.")
            records.state = "cancelled"
            records.state = False
        return True
