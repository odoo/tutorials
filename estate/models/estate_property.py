from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char('Property Name', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    postcode = fields.Char('Post Code', required=True)
    date_availability = fields.Date(
        'Availability Date',
        required=True,
        copy=False,
        default=fields.Date.today() + relativedelta(months=3),
    )
    type_id = fields.Many2one("estate.property.type", string="Type", required=True)
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    expected_price = fields.Float('Expected Price')
    selling_price = fields.Float(
        'Selling Price',
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(
        '# Bedrooms',
        default=2,
    )
    facades = fields.Integer('# Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    living_area = fields.Integer('Living Area mt²')
    garden_area = fields.Integer('Garden mt²')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default="new",
        copy=False,
        required=True,
        readonly=True,
        # group_expand=True
    )
    total_area = fields.Integer(
        "Total Area m²",
        compute="_compute_total_area",
    )
    best_price = fields.Float(
        "Best Price",
        compute="_compute_best_price",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            # Nasty magic string. I should turn the option into a variable and then reference it
            self.garden_orientation = "north"
            return

        self.garden_area = 0
        self.garden_orientation = None

    def action_sold(self):
        for property in self:
            if not property.selling_price:
                raise UserError("You can not sell a property without accepted offers")

            if property.state == "cancelled":
                raise UserError("You can not sell a cancelled property")

            property.state = "sold"

        return True

    def action_cancel(self):
        for property in self:
            if property.state == "sold":
                raise UserError("You can not cancel a sold property")

            property.state = "cancelled"

        return True

    _exp_price_positive = models.Constraint(
        'CHECK(expected_price > 0)',
        'The property expected price must be strictly positive',
    )

    _sell_price_positive = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The property selling price must be positive',
    )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for property in self:
            if float_is_zero(property.selling_price, precision_digits=2):
                continue

            limit = 0.9 * property.expected_price
            if float_compare(property.selling_price, limit, precision_digits=2) == -1:
                raise ValidationError("The property selling price must be at least 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_not_new_or_cancelled(self):
        for property in self:
            if property.state not in ('new', 'cancelled'):
                raise UserError("You can not delete a property that is not either 'new' or 'cancelled'")
