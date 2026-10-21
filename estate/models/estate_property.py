from odoo import api, exceptions, fields, models, tools


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True, string='Title')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        string='Available From',
    )
    garden_area = fields.Integer(string='Garden Area (sqm)')
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_orientation = fields.Selection(
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
            ('offer', 'Offer Received'),
            ('accept', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancel', 'Cancelled'),
        ],
        default='new',
        required=True,
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(compute='_compute_area', string='Total Area (sqm)')
    best_price = fields.Float(compute='_compute_best_price', string='Best Offer')

    _exp_price_positive_constraint = models.Constraint(
        "CHECK (expected_price > 0)", "A property expected price must be strictly positive"
    )
    _sell_price_positive_constraint = models.Constraint(
        "CHECK (selling_price >= 0)", "A property selling price must be strictly positive"
    )

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if (
                    not tools.float_is_zero(record.selling_price, 2)
                    and tools.float_compare(record.selling_price, record.expected_price * 0.9, 2) == -1
            ):
                raise exceptions.ValidationError("The selling price cannot be lower than 90% of the expected price.")

    def action_set_sold(self):
        if self.state != 'cancel':
            self.state = 'sold' if self.state != 'sold' else 'new'
        else:
            raise exceptions.UserError("Cancelled properties cannot be sold")
        return True

    def action_set_cancelled(self):
        if self.state != 'sold':
            self.state = 'cancel' if self.state != 'cancel' else 'new'
        else:
            raise exceptions.UserError("Sold properties cannot be cancelled")
        return True
