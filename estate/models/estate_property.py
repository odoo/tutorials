# imports of python lib
from dateutil.relativedelta import relativedelta

# imports of odoo
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Test'
    _order = 'id desc'

    # SQL Constraints
    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price > 0)', 'Selling price must be strictly positive.'),
    ]

    name = fields.Char(string='Name', required=True)
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(string='Available From', copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string='Garden Orientation'
    )
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string='Status',
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(string='Total Area', compute='_compute_total_area')
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')

    # -----------------------
    # Compute methods
    # -----------------------
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area) + (record.garden_area)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    # ----------------------------------
    # Constraints and onchange methods
    # ----------------------------------
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for property in self:
            if not float_is_zero(property.selling_price, precision_digits=2):
                min_allowed = 0.9 * property.expected_price
                if float_compare(property.selling_price, min_allowed, precision_digits=2) < 0:
                    raise ValidationError('Selling price cannot be lower than 90% of the expected price.')

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.write({
                'garden_area': 10,
                'garden_orientation': 'north'
            })
        else:
            self.write({
                'garden_area': 0,
                'garden_orientation': False
            })

    # ----------------------
    # CRUD methods
    # -----------------------
    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError('You can only delete properties that are in New or Cancelled state.')

    # ----------------------
    # Action methods
    # ----------------------
    def action_mark_sold(self):
        for record in self:
            if not record.offer_ids:
                raise UserError("You can mark this property as sold because there are no offers.")
            if record.state == 'cancelled':
                raise UserError('Cancelled properties cannot be marked as sold.')

            accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            if not accepted_offer:
                raise UserError("You must accept an offer before marking the property as sold.")

            record.state = 'sold'
        return True

    def action_mark_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properties cannot be marked as cancelled.')
            record.state = 'cancelled'
        return True
