from dateutil.relativedelta import relativedelta
from odoo import api,fields, models

#Class of EstateProperty to define fields of database table
class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Properties'

    name = fields.Char(string='Name',required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', copy=False, default=fields.Date.add(fields.Date.today()+ relativedelta(months=3)))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price ', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area(sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area(sqm)')
    garden_orientation = fields.Selection(
        string ='Garden Orientation',
        selection=[('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West')])
    active = fields.Boolean('Active',default=True)
    state = fields.Selection(
        selection=[
            ('new','New'),
            ('offer_received','Offer Received'),
            ('offer_accepted','Offer Accepted'),
            ('sold','Sold'),('cancelled','Cancelled')],
        string='State',
        required=True,
        copy=False,
        default='new')
    total_area = fields.Float(string='Total Aream(sqm)',compute='_compute_total_area')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    user_id=fields.Many2one(res.users', string='Salesperson', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer',copy=False)
    tag_ids = fields.Many2many('estate.property.tags',string='Tags')
    offer_ids = fields.One2many('estate.property.offer','property_id',string='Offers') #One2Many field
    best_prices = fields.Float(string='Best Offer',compute='_compute_best_offer')

    #Function of computing total area
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area=record.living_area+record.garden_area
    
    #Fucntion of deciding best price among available prices
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for property in self:
            if property.offer_ids:
                property.best_prices = max(property.offer_ids.mapped('price'),default=0.0)
            else:
                property.best_prices=0.0

    @api.onchange('garden')
    def onchange_check_garden_status(self):
        if self.garden:
            self.garden_area =10
            self.garden_orientation ='north'
        else:
            self.garden_area =0
            self.garden_orientation =''
            