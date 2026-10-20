from odoo import fields, models, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string='Property name', required=True)
    description = fields.Text()

    type_id = fields.Many2one('estate.property.type', string='Property type', required=True)

    seller_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', index=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    best_price = fields.Float(string='Best price', compute='_compute_best_price')

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('new', 'New'),
         ('received', 'Offer Received'),
         ('accepted', 'Offer Accepted'),
         ('sold', 'Sold'),
         ('cancelled', 'Cancelled')],
        default='new'
    )
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string='Expected price', required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Float(compute='_compute_total_area')
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = None

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None
