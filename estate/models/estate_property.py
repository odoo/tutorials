from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _order = "id desc"

    name = fields.Text('Title', required=True, default='Unknown', translate=True)
    description = fields.Text('Description')
    post_code = fields.Char('Postcode')
    date_availability = fields.Date(
        'Available From',
        copy=False,
        default=lambda self: date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string='Garden Orientation',
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer', 'Offer'),
            ('received', 'Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string='State',
        default='new',
        required=True,
        copy=False,
    )
    active = fields.Boolean('Active', default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one(
        'res.users', string='Salesman', default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
        readonly=True,
        domain=[('is_company', '=', False)],
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(
        "Best Offer", compute="_compute_best_price", readonly=True
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = (rec.living_area or 0) + (rec.garden_area or 0)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            prices = rec.offer_ids.mapped('price')
            rec.best_price = max(prices, default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        if any([prop.state == "cancelled" for prop in self]):
            raise UserError("Canceled property cannot be sold !")
        self.state = 'sold'
        return True

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold property cannot be canceled !")
        return self.write({"state": "cancelled"})

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_constraint(self):
        for rec in self:
            if float_is_zero(rec.selling_price or 0.0, precision_digits=2):
                continue
            if not rec.expected_price:
                raise ValidationError(
                    "Expected price must be set to validate selling price."
                )
            threshold = 0.9 * rec.expected_price
            if float_compare(rec.selling_price, threshold, precision_digits=2) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)', 'The selling price must be positive or zero.'
    )

    @api.ondelete(at_uninstall=False)
    def _ondelete_check_state(self):
        for prop in self:
            if prop.state not in ('new', 'cancelled'):
                raise UserError(
                    'Only properties in New or Cancelled state can be deleted.'
                )
