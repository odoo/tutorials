from odoo import api, models, fields
from odoo.exceptions import UserError
import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    notes = fields.Html()
    date_availability = fields.Date(copy=False, default=lambda self: datetime.date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")])
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("cancelled", "Cancelled")],
        copy=False, required=True, default="new")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    _positive_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price of a property must be strictly positive'
    )
    _positive_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price of a property must be positive'
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            if len(prices) > 0:
                record.best_price = max(prices)
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def sell_property(self):
        self.ensure_one()
        for record in self:
            if record.state == "cancelled":
                raise UserError("Error - You cannot sell a cancelled property !")
            record.state = "sold"
        return True

    def cancel_property(self):
        self.ensure_one()
        for record in self:
            if record.state == "sold":
                raise UserError("Error - You cannot cancel a sold property !")
            record.state = "cancelled"
        return True

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=3):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=3) < 0:
                    raise UserError(r"The selling price must be at least 90% of the expected price !")

    @api.ondelete(at_uninstall=False)
    def _unlike_if_stats_new_or_cancelled(self):
        for record in self:
            if record.state in ('new', 'cancelled'):
                raise UserError("You cannot delete a new or cancelled property !")
