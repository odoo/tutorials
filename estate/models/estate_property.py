from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare
from odoo import api, fields, models, exceptions


class Property(models.Model):
    _name = "estate.property"
    _description = "a real estate property"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )

    date_availability = fields.Date(string="Available From", default=fields.Date.today() + relativedelta(months=3), copy=False)

    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_offer = fields.Float(compute="_compute_best_offer")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)

    postcode = fields.Char()
    bedrooms = fields.Integer(default=2)
    garage = fields.Boolean()
    facades = fields.Integer()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")])
    living_area = fields.Integer(string="Living Area (sqm)")
    total_area = fields.Float(compute="_compute_total_area")

    _sql_constraints = [
        (
            "positive_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price should be stricly positive.",
        ),
        (
            "positive_selling_price",
            "CHECK(selling_price > 0)",
            "The selling price should be strictly positive.",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price")) if record.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for property in self:
            if property.state == "sold":
                if float_compare(property.selling_price, property.expected_price * 0.9, precision_digits=2) > 0:
                    raise exceptions.ValidationError("We can't sell at a price lower than 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_property_with_offers(self):
        if any(property.state != "cancelled" and property.state != "new" for property in self):
            raise exceptions.UserError("Can't delete a property that have offers, or that isn't cancelled.")

    def action_sold(self):
        for property in self:
            if property.state == "cancelled":
                raise exceptions.UserError("Cancelled properties cannot be sold.")
            else:
                property.state = "sold"

    def action_cancel(self):
        for property in self:
            if property.state == "sold":
                raise exceptions.UserError("Sold properties cannot be cancelled.")
            else:
                property.state = "cancelled"
