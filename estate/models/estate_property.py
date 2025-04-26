from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)",
         "The expected price must be strictly positive"),
        ("check_sell_price", "CHECK(selling_price > 0)",
         "The selling price of a property must be positive")
    ]
    _order = "id desc"

    name = fields.Char('name', required=True)
    description = fields.Text('description')
    postcode = fields.Char('postcode')
    availability_date = fields.Date('availabilty date', copy=False,
                                    default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float('expected price', required=True)
    selling_price = fields.Float('selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('bedrooms', default=2)
    living_area = fields.Integer('living area')
    facades = fields.Integer('facades')
    garage = fields.Boolean('garage')
    garden = fields.Boolean('garden')
    garden_area = fields.Integer('garden area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
    )
    active = fields.Boolean('active', default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Acccepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="property type")
    user_id = fields.Many2one("res.users", string="Salesperson",
                              default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute='_compute_total_area')
    best_offer = fields.Float(compute="_compute_best_offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sell(self):
        if "cancelled" in self.mapped('state'):
            raise UserError("You can't sell a cancelled property")
        self.state = "sold"
        return True

    def action_cancel(self):
        if "sold" in self.mapped('state'):
            raise UserError("You can't cancel a sold property")
        self.state = "cancelled"

        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2) and \
                float_compare(record.selling_price, 0.9 * record.expected_price, 2) < 0:
                raise ValidationError("The selling price has to be at least 90% of the expected price")
