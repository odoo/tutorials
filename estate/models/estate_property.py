from odoo import fields, models, api, exceptions, tools


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Properties'

    name = fields.Char('Estate Property', required=True, translate=True)
    description = fields.Char('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available from', default=lambda self: fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Façades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Oriented is used to show which cardinal direction the garden is oriented to",
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        default='new',
        copy=False,
        help="Shows the state of the property",
    )
    property_type_id = fields.Many2one('estate.property.type', string='Type')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(compute='_compute_total_area')
    best_offer = fields.Float(compute='_compute_best_price')

    _expected_price_must_be_positive = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be greater than 0",
    )

    _selling_price_must_be_positive = models.Constraint(
        "CHECK(selling_price > 0)",
        "The selling price must be greater than 0",
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        self.total_area = self.living_area + self.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        self.best_offer = max(self.offer_ids.mapped('price')) if self.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if (
                not tools.float_is_zero(record.selling_price, 2)
                and tools.float_compare(record.selling_price, record.expected_price * 0.9, 2) == -1
            ):
                raise exceptions.ValidationError("The selling price cannot be below the 90% of the expected price.")


    def action_set_sold(self):
        if self.state != 'cancelled':
            self.state = 'sold'
            return True
        else:
            raise exceptions.UserError("The property is marked as cancelled. Cancelled properties cannot be sold.")

    def action_set_cancelled(self):
        if self.state != 'sold':
            self.state = 'cancelled'
            self.selling_price = 0
            self.buyer_id = None
            return True
        else:
            raise exceptions.UserError("The property is marked as sold. Sold properties cannot be cancelled.")
