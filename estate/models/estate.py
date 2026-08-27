from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, exceptions
from odoo.tools.float_utils import float_compare, float_is_zero


class Estate(models.Model):
    _name = "estate"
    _description = "Real Estate Module"

    # fields
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
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
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ]
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean(default=True)
    estate_type_id = fields.Many2one("estate.type", string="Estate Type")
    seller_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.tag", string="Tags")
    offer_ids = fields.One2many("estate.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", store=True)
    best_offer = fields.Float(compute="_compute_best_offer")

    _check_expected_price_positive = models.Constraint(
        "CHECK(expected_price > 0)",
        "A property expected price must be strictly positive.",
    )
    _check_selling_price_positive = models.Constraint(
        "CHECK(selling_price >= 0)",
        "A property selling price must be positive.",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):

        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0)

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
                raise exceptions.UserError("Cannot sell a cancelled property")
            record.state = "sold"

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("Cannot cancel a sold property")
            record.state = "cancelled"

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                raise exceptions.ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )
