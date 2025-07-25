from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Module"
    _order = "id desc"

    name = fields.Char(required=True)
    create_uid = fields.Integer()
    create_date = fields.Date()
    write_uid = fields.Integer()
    write_date = fields.Date()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("northeast", "North-East"),
            ("east", "East"),
            ("southeast", "South-East"),
            ("west", "West"),
            ("southwest", "South-West"),
            ("south", "South"),
            ("northwest", "North-West"),
        ],
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    type_id = fields.Many2one("estate.property.type", string="Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "Expected price should be bigger than 0"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "Selling price should be 0 or bigger"),
    ]

    @api.constrains("selling_price")
    def _check_sell_price(self):
        for record in self:
            if float_compare(record.selling_price, 0.0, 2) == 0:
                continue
            if float_compare(record.selling_price, record.expected_price * 0.9, 2) == -1:
                raise ValidationError("Sell Price needs to be at least 90perc of Expected Price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped("price"))
            else:
                record.best_offer = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def sell_property(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled property cannot be sold")
            record.state = "sold"

    def cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be cancelled")
            record.state = "cancelled"
