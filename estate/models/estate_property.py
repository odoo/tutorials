from odoo import api, fields, models

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate properties'

    name = fields.Char('Name', required=True)
    description = fields.Char('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Date('Available From', copy=False, default=lambda x:fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation', 
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default='new')
    property_type_id = fields.Many2one('estate.property.type', string='Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer('Total Area', compute='_compute_total_area')
    best_price = fields.Float('Best Offer', compute='_compute_best_price')

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            record.garden_area = (10 if record.garden else 0)
            record.garden_orientation = ('north' if record.garden else None)