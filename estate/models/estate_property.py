from odoo import models,fields
from datetime import date
from dateutil.relativedelta import relativedelta
class EstateProperty(models.Model):
    _name = "estate.property"
    _description= "This is a test description"
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default = date.today()+relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price= fields.Integer(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string ='Type',selection=[('north','North'),('south','South'),('east','East'),('west','West')])
    active = fields.Boolean('Active',default=True)
    state = fields.Selection(string="state",selection=[('new','New'),('offer received','Offer Received'),('offer accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')],required=True,copy=False,default='new')
    property_type_id = fields.Many2one("estate.property.type")
    buyer = fields.Many2one("res.partner",string="Buyer",copy=False)
    seller = fields.Many2one("res.partner",string="Seller",default = lambda  self: self.env.company.id)
    tag_ids= fields.Many2many("estate.property.tag")
    offer_ids = fields.Many2many("estate.property.offer")