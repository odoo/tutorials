from odoo import api, exceptions, fields, models, tools


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real estate management'
    _order = 'id desc'
    _sql_constraints = [
        ('expected_price_strictly_positive', 'CHECK(expected_price > 0)',
            'The expected price should be stricly positive.'),
        ('selling_price_positive', 'CHECK(selling_price >= 0)',
            'The selling price should be positive.')
    ]

    active = fields.Boolean('Is Active?', default=True)
    name = fields.Char('Title', required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')

    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False,
        default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    best_price = fields.Float('Best Offer', compute='_compute_best_price', default=0)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)

    bedrooms_count = fields.Integer('Bedrooms', default=2)
    description = fields.Text('Description')
    facades_count = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('east', 'East'),
        ('south', 'South'),
        ('west', 'West')], string='Garden Orientation')
    living_area = fields.Integer('Living Area (sqm)')
    total_area = fields.Integer('Total Area (sqm)', compute='_compute_total_area')

    buyer_id = fields.Many2one('res.partner', string='Buyer', readonly=True, copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string='Status', copy=False, required=True, readonly=True, default='new')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for property in self:
            best_price = self.env['estate.property.offer']._read_group(
                [('id', 'in', property.offer_ids.ids)], aggregates=['price:max'])[0][0]
            property.best_price = best_price if property.offer_ids else 0

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for property in self:
            property._check_selling_price()

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for property in self:
            if property.state not in ['new', 'offer_received']:
                is_selling_price_too_low = tools.float_compare(property.selling_price, property.expected_price * 0.9, precision_digits=1) < 0
                if is_selling_price_too_low:
                    raise exceptions.ValidationError(
                        'The selling price cannot be less than 90% of the expected price.')

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else False

    def write(self, vals):
        for property in self:
            origin = property._origin.state
            current = vals.get('state')
            if origin == 'canceled' and current == 'sold':
                raise exceptions.UserError('You cannot mark a canceled property as sold.')
            elif origin == 'sold' and current == 'canceled':
                raise exceptions.UserError('You cannot mark a sold property as canceled.')
        return super().write(vals)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_not_new_or_canceled(self):
        for property in self:
            if property.state not in ['new', 'canceled']:
                raise exceptions.UserError(
                    'You cannot delete a property that is not new or canceled.'
                )

    def action_mark_canceled(self):
        for property in self:
            property.state = 'canceled'

    def action_mark_sold(self):
        for property in self:
            if not any([offer.status == 'accepted' for offer in property.offer_ids]):
                raise exceptions.UserError('You cannot mark as sold a property with no accepted offer.')
            property.state = 'sold'
