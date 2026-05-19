from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import _, api, exceptions, fields, models
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Model"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda x: date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])

    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type"
    )
    salesman_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)

    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], required=True, default='new')
    sequence = fields.Integer(default=1)
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be stricly positive.'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be stricly positive.'
    )

    @api.constrains('selling_price')
    def _check_selling_price_py(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2)\
                    and float_compare(record.selling_price,
                                      record.expected_price * .9,
                                      precision_digits=2) < 0:
                raise exceptions.ValidationError(
                    "The selling price can't be lower than 90%% of the expected price.")  # noqa: E501

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped(
                'price')) if record.offer_ids else None

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = None
        self.garden_orientation = None
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

    def action_set_sold(self):
        error = None
        for record in self:
            if record.state == 'cancelled':
                error = _('Cancelled properties cannot be sold')
                continue
            record.state = 'sold'
        if error:
            raise exceptions.UserError(error)

    def action_set_cancelled(self):
        error = None
        for record in self:
            if record.state == 'sold':
                error = _('Sold properties cannot be cancelled')
                continue
            record.state = 'cancelled'
        if error:
            raise exceptions.UserError(error)

    @api.ondelete(at_uninstall=False)
    def _unlink_only_new_or_cancelled(self):
        if self.state not in ['new', 'cancelled']:
            raise exceptions.UserError(
                _('Can only delete New or Cancelled properties.')
            )
