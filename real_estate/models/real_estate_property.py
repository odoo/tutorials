from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

class RealEstate(models.Model):
    _name = "real.estate.property"
    _description = 'Real State propperties'

    name = fields.Char(string = 'Title', required = True)
    description = fields.Text(string = 'Description')
    postcode = fields.Char(string = 'Postcode')
    date_availability = fields.Date(string = 'Available From', copy = False, default = fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float(string = 'Expected Price', required = True)
    selling_price = fields.Float(string = 'Selling Price', readonly = True, copy = False)
    bedrooms = fields.Integer(string = 'Bedrooms', default = 2)
    living_area = fields.Integer(string = 'Living Area (sqm)')
    facades = fields.Integer(string = 'Facades')
    garage = fields.Boolean(string = 'Garage', )
    garden = fields.Boolean(string = 'Garden')
    garden_area = fields.Integer(string = 'Garden Area (sqm)')
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')

        ],
        string = 'Garden Orientation'

    )
    status = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default = 'new',
        string = 'Status',
        copy = False
    )
    active = fields.Boolean(string = "Active", default = True)
    
    property_type_id = fields.Many2one('real.estate.property.category', string = "Property Type")
    
    partner_id = fields.Many2one("res.partner", string = "Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string = "Salesman", default = lambda self: self.env.user)

    tag_id = fields.Many2many('real.estate.property.tag', string = "Tag")

    offer_id = fields.One2many('real.estate.property.offer', 'property_id', string = 'Offer', copy = False)

    total_area = fields.Float(compute = "_compute_total_area", string = "Total Area (sqm)", readonly = True)

    best_price = fields.Float(compute = "_compute_best_price", string = "Best Offer", readonly = True, default = 0, copy = False)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_id.price')
    def _compute_best_price(self):
        # print("hello",self.offer_id.price)
        for record in self:
            price_list = record.offer_id.mapped('price')
            if len(price_list) > 0:
                record.best_price = max(record.offer_id.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden_details(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = ''
            self.garden_orientation = ''
        


    