from odoo import fields, models ,api
from datetime import datetime, timedelta
from odoo.exceptions import UserError,ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"
    

    name = fields.Char(required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson = fields.Many2one('res.users', string="Sales Person", default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string="buyer", copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags ID")
    postcode = fields.Char()
    description = fields.Text()
    availability_date = fields.Date(default=lambda self: datetime.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(default=10000,readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new',
        string="Status",
    )
    total_area = fields.Float(compute="_compute_total")
    best_offer = fields.Float(compute="_compute_price")

    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
    
    @api.depends("offer_ids.price")
    def _compute_price(self):
        for record in self:
            if record.offer_ids:
                record.best_offer =  max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0
    
    @api.onchange("garden")
    def _onchange_(self):
        if(self.garden):
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None
        
    @api.constrains('expected_price','selling_price')
    def _check_price(self):
        for record in self:
            if record.expected_price <= 0 or record.selling_price <0 :
                raise ValidationError("The price must be greater than zero.")
    
    @api.constrains('selling_price','expected_price')
    def _check_selling(self):
        for record in self:
            if record.selling_price < 0.9*record.expected_price:
                raise ValidationError("You can not make offer if the price is much lower")

    def action_set_sold(self):
        for record in self:
            if(record.state == "canceled"):
                raise UserError("You can not change status to sold if it is canceled")
            else:
                record.state = "sold"
        return True

    def action_set_cancel(self):
        for record in self:
            if(record.state == "sold"):
                raise UserError("You can not change status to canceled if it is sold")
            else:
                record.state = "canceled"
        return True
    
    


    

