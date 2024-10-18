from datetime import timedelta

from odoo import  api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Real estate App"
    _rec_name = "name"
    _order = "id desc"
    
    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, default = lambda self: fields.Date.today() + timedelta(days = 90))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True , copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection = [('north','North'),('south','South'), ('east','East'), ('west','West')],
        help = "Select one"
    )
    active = fields.Boolean(default = True)
    state = fields.Selection(
        required = True,
        string = 'Select the status',
        selection = [('new','New'),('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'),('sold','Sold'), ('cancelled','Cancelled')],
        help = "Select one",
        default = 'new',
        copy = False
    )

    property_type_id = fields.Many2one("estate.property.type", string = "Property Type")
    tag_id = fields.Many2many('estate.property.tags')
    buyer_id = fields.Many2one('res.partner', string = "Buyer")
    seller_id = fields.Many2one('res.users' ,string="Salesperson", default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer','property_id', string="Offers")
    total_area = fields.Integer(compute = '_compute_total_area')
    best_offer_price = fields.Float(compute = '_compute_bestprice') 
    
    _sql_constraints = [
        ("check_expected_price","CHECK(expected_price > 0)","Expected price must be greater than 0" ),
        ("Bedroom_check","CHECK(bedrooms < 4)","We only deal upto 3 BHK" ),
        ("selling_price_constraint","CHECK(selling_price >= 0)","Selling price cant be negative")
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price != 0 and record.selling_price < record.expected_price * 0.9:
                raise ValidationError("Selling price cant be lower than 90 percentage of expected price")

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_bestprice(self):
        # model = self.env["ir.ui.view"]
        # print(model)
        for record in self:
            record.best_offer_price = max(record.offer_ids.mapped('price'),default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        
        if(self.garden == True):
            self.garden_area = 10
            self.garden_orientation = 'north'

        if(self.garden == False):
            self.garden_area = 0
            self.garden_orientation = ''
    
    def action_sold(self):
        for record in self:
            if(record.state == 'cancelled'):
                raise UserError("Cancelled Property can not be sold")
            else:
                record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if(record.state == 'sold'):
                raise UserError("Sold Property can not be cancelled")
            else:
                record.state = 'cancelled'
        return True
