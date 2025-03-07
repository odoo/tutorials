from odoo import api, models, fields, exceptions # type: ignore
from odoo.exceptions import ValidationError # type: ignore
from datetime import date
from dateutil.relativedelta import relativedelta

class property(models.Model):
    _name = 'estate.property' 
    _description = 'property'

    name = fields.Char(string="Property Name", required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids= fields.One2many("estate.property.offer", "property_id", string="Property Offers")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", default=date.today()+relativedelta(months=+3), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True, default=1)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    salesperson_user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_user_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )
    status=fields.Selection(
        [('new', 'New'),('offer_received','Offer Received'), ('offer_accepted', 'Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')],
        string="Status",
        default='new',
        copy=False
    )
    active = fields.Boolean(string="Active", default=True)
    total_area= fields.Float(compute="_compute_total_area", readonly=True, copy=False)
    best_price= fields.Float(compute="_compute_best_price", readonly=True, default= 0.0)

    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0 )', 'The selling price should be positive and greater than 0.'),
        ('check_expected_price', 'CHECK(expected_price > 0 )', 'The expected price should be positive and greater than 0.')
    ]
   
    @api.constrains('selling_price')
    def check_selling_price(self):
        if self.selling_price < (0.90*self.expected_price):
            raise ValidationError("The selling price cannot be less than 90% of expected price")
    

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area= record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        
        for record in self:
            if record.offer_ids:
                if len(record.offer_ids):
                    for tuple in record.offer_ids:
                        record.best_price= max(tuple.price,record.best_price)
            else:
                record.best_price= 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if(self.garden):
            self.garden_area=10
            self.garden_orientation="north"
        else:
            self.garden_area=0
            self.garden_orientation=False

    def set_sold(self):      
        if self.status != "cancelled":
            self.status = "sold"  
        else:
            raise exceptions.UserError("Cancelled properties cannot be sold")
                
        return True
    
    def set_cancel(self):
        self.status = "cancelled"
        return True
    