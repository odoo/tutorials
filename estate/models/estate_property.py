from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'All properties'
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute='_compute_best_price')
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute='_compute_total_area')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        required=True,
        default='new',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        )
    property_type_id = fields.Many2one(
        'estate.property.type', string='Property Type',
    )
    buyer_id = fields.Many2one(
        'res.partner', string='Buyer', copy=False,
    )
    salesperson_id = fields.Many2one(
        'res.users', string='Salesperson',
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price of a property should be strictly positive.',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price of a property should be positive.',
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            living_area = record.living_area or 0
            garden_area = record.garden_area or 0
            record.total_area = living_area + garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if self.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, 2)
                and float_compare(record.selling_price, record.expected_price * 0.90, 2) < 0
            ):
                raise ValidationError("Selling price cannot be lower than 90% of expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(f"Can't delete property in {record.state} state")

    def action_mark_as_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('Property is already cancelled')

            record.state = 'sold'

    def action_mark_as_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Property is already sold')

            record.state = 'cancelled'
