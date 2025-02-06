from odoo import fields, models, api
from datetime import timedelta

class Estateproperty(models.Model):
    _name = "estate.property"
    _description = "Estate property table"

    name = fields.Char('Property Name', required=True, default="unknown")

    property_type_id = fields.Many2one('estate.property.type', "Property Type")

    salesperson_id = fields.Many2one('res.users', string='Salesperson', default= lambda self: self.env.user)
    buyer_id= fields.Many2one('res.partner', string='Buyer', copy=False)

    tag_ids= fields.Many2many('estate.property.tag', "Tags")

    offer_ids = fields.One2many('estate.property.offer', 'property_id', 'Offers')

    description = fields.Text('Description', compute='_compute_desc')

    @api.depends("salesperson_id.name")
    def _compute_desc(self):
        for record in self:
            record.description = "Test for salesperson %s" % record.salesperson_id.name

    postcode= fields.Char('PostCode')
    date_availability= fields.Date('Available From',copy=False, default= lambda self: fields.Datetime.today() + timedelta(days=90))
    expected_price= fields.Float('Expected Price',required=True)
    selling_price= fields.Float('Selling Price',readonly=True, copy=False)
    bedrooms= fields.Integer('Bedrooms',default=2)
    living_area= fields.Integer('Living Area')
    facades= fields.Integer('Facades')
    garage= fields.Boolean('Garage')
    garden= fields.Boolean('Garden')
    garden_area= fields.Integer('Garden Area')
    garden_orientation= fields.Selection(
        string='Type',
        selection=[('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state= fields.Selection(
        string='State',
        selection=[('new', 'New'),('offered_rec', 'Offer recieved'),('offer_acc', 'Offer Accepted'),('sold', 'Sold'),('cancel', 'Cancelled')],
        required=True,
        copy=False,
        default='new'
        
    )

    #computed fields

    total_area = fields.Integer('Total Area', compute='_compute_total_area')

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    best_price = fields.Float('Best Price', compute='_compute_best_price')

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            prices = property.offer_ids.mapped('price')
            property.best_price = max(prices)

