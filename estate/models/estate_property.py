from odoo import models, fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    
    name = fields.Char(required=True)
    tags= fields.Many2many("estate.property.tag", string="tags")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=fields.Datetime.today()+relativedelta(days=90))
    salesperson = fields.Many2one('res.partner',string='Salesperson',default= lambda self :self.env.user.partner_id)
    buyer= fields.Many2one('res.partner',string='Buyer')
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    property_type_id=fields.Many2one('estate.property.type')
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('east', 'East'),('west','West'),('south','South')],
        help="Type is used to separate Leads and Opportunities")
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer received', 'Offer Received'),('offer accepted','Offer Accepted'),('sold','Sold'),('cancelled','cancelled')],
        help="Type is used to separate Leads and Opportunities",
        required = True,
        default = "new",
        copy = False 
        )
    active = True
    offer_ids= fields.Many2many("estate.property.offer","property_id")
