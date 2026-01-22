from odoo import api, exceptions, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    property_tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    date_availability = fields.Date(
        'Availability Date',
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)

    bedrooms = fields.Integer('# Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('# Facades')
    garage = fields.Boolean('Garage')

    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )

    total_area = fields.Float(string='Total Area', compute='_compute_total_area')

    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.uid)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    best_offer = fields.Float(string='Best Offer', compute='_compute_best_offer')

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        default='new',
        required=True
    )

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price of a property should be stricly positive'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price of a property should be positive'
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.onchange('offer_ids')
    def _onchange_offer_ids(self):
        for record in self:
            if record.state == 'new' and len(record.offer_ids) > 0:
                record.state = 'offer_received'

    def action_sell(self):
        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError('Canceled properties cannot be sold')

            record.state = 'sold'

        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError('Sold properties cannot be canceled')

            record.state = 'canceled'

        return True
