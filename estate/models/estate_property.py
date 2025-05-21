from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "estate property description"
    name = fields.Char('Property Name', required=True)
    address = fields.Char('Property Address', required=True)
    postcode = fields.Char('Property Postcode', required=True)
    expected_price = fields.Float('Property Expected Price', digits=(16, 2), required=True)
    availability_date = fields.Date('Property Available', required=True, copy=False, default=lambda _: fields.Date.today() + relativedelta(months=3))
    furnished = fields.Boolean('Property Furnished', default=False)
    bedrooms = fields.Integer('Property Bedrooms', required=True, default=2)
    bathrooms = fields.Integer('Property Bathrooms', required=False, default=1)
    selling_price = fields.Float('Property Selling Price', digits=(16, 2), required=False, readonly=True, copy=False)
    living_area = fields.Integer('Property Living Area', required=False)
    garage = fields.Boolean('Property Has Garage', required=True)
    garden = fields.Boolean('Property Has Garden', required=True)
    garden_area = fields.Integer('Property Garden Area (sqm)', required=True)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="orientation of the garden")
    active = fields.Boolean('Property Active', default=True)
    state = fields.Selection(
        string='Property State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new',
        required=True,
        copy=False
    )
    facades = fields.Integer('Property Facades')
    description = fields.Text('Property Description', default="No description provided.")

    # Many-To-One Relations
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', required=False)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesman_id = fields.Many2one('res.users', string='Salesman', required=True, default=lambda self: self.env.uid)

    # Many-To-Many Relations
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    # One-To-Many Relations
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    # Computed Fields
    total_area =fields.Integer('Property Total Area', compute='_calculate_total_area')
    best_price = fields.Float('Property Best Offer', digits=(16, 2), readonly=True, copy=False, compute='get_best_price')

    @api.depends('offer_ids')
    def get_best_price(self):
        _best_offer = 0
        for property in self:
            for offer in property.offer_ids:
                _best_offer = max(_best_offer, offer.price)
            property.best_price = _best_offer

    @api.depends('living_area', 'garden_area')
    def _calculate_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
