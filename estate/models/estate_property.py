from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'An individual estate property listing'

    name = fields.Char('Title', required=True, default='Unknown')
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        'Available From',
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', copy=False, readonly=True)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        'Garden Orientation',
    )
    last_seen = fields.Datetime('Last Seen', default=fields.Datetime.now)
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        'Status',
        default='new',
        copy=False,
        required=True,
    )
    property_type_id = fields.Many2one('estate.property.type', 'Property Type')
    salesperson_id = fields.Many2one(
        'res.users', 'Salesperson', default=lambda self: self.env.uid
    )
    buyer_id = fields.Many2one('res.partner', 'Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    best_price = fields.Float(
        'Best Price', copy=False, readonly=True, compute='_compute_best_price'
    )
    total_area = fields.Integer(
        compute='_compute_total_area', readonly=True, string='Total Area (sqm)'
    )

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = (
                max(record.offer_ids.mapped('price')) if record.offer_ids else 0
            )

    @api.onchange('garden')
    def _onchange_garden(self):
        """Set default garden area and orientation when garden is checked."""
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('You cannot cancel a sold property.')

            record.state = 'cancelled'

        return True

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('You cannot mark a cancelled property as sold.')

            record.state = 'sold'

        return True
