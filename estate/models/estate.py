from odoo import models, fields, api, exceptions


class EstateModel(models.Model):
    _name = 'estate.property'
    _description = "Real estate model"
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    property_type_id = fields.Many2one('estate.type', string="Property Type")
    property_tags_ids = fields.Many2many('estate.tag', string="Property Tags")
    buyer_id = fields.Many2one('res.partner', string="Property Owner")
    salesperson_id = fields.Many2one('res.users', string="Property Salesperson", default=lambda self: self.env.user)
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), month=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False, default=0)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="garden orientation")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer received'), ('offer_accepted', 'Offer accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="State",
        default='new',
        copy=False,
        required=True
    )
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offer")
    total_area = fields.Float(compute="_compute_total_area", readonly=True)
    best_price = fields.Float(compute="_compute_best_offer", readonly=True, default=0)

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price >= 0)',
         'Expected Price should be a positive value'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)',
         'Selling Price should be a positive value'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if len(record.offer_ids) else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if (self.garden):
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            expected_minimum_price = record.expected_price * 0.9
            if record.selling_price < expected_minimum_price:
                raise exceptions.ValidationError("This selling price is too low")

    def cancel(self):
        if self.state == 'sold':
            raise exceptions.UserError("Cannot cancel a sold property")
        self.state = 'canceled'
        return True

    def sold(self):
        if self.state == 'canceled':
            raise exceptions.UserError("Cannot sell a canceled property")
        self.state = 'sold'
        return True
