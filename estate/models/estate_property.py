from odoo import api, exceptions, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstatePropertytModel(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property Model'
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new',
    )
    type_id = fields.Many2one(
        'estate.property.type',
        string='Tag',
    )
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False,
    )
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Tags',
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers'
    )
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError('Cancelled properties cannot be sold.')
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Sold properties can't be cancelled.")
            record.state = 'cancelled'

    @api.constrains('selling_price', 'expected_price')
    def _check_expected_to_selling_price_ratio(self):
        for record in self:
            limit = record.expected_price * 0.9
            if float_compare(record.selling_price, limit, precision_digits=2) == -1:
                raise ValidationError('The selling price cannot be lower than 90% of the expected price!')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The Expected price of a property should be > 0',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)',
        'The selling price of a property should be > 0',
    )
    _check_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The prop name must be unique!',
    )

    @api.ondelete(at_uninstall=False)
    def _check_property_state_on_delete(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError("You cannot delete a property that is not 'New' or 'Cancelled'!")
