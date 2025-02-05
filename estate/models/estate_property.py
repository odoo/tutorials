from odoo import models,fields
from datetime import timedelta

class estate_property(models.Model):
    _name = "estate_property"
    _description = "Estate Property models"
    
    name = fields.Char("Title",default = "Unknown",required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(copy = False,default = lambda self : fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Type',
        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    last_seen = fields.Datetime("Last Seen", default = fields.Datetime.now)
    active = fields.Boolean(default = True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], string="State", default='new', required=True, copy=False)

    property_type_id = fields.Many2one('estate_property.type',string = "Property Type")
    buyer_id = fields.Many2one('res.partner',string= 'Buyer', copy=False)
    seller_id = fields.Many2one('res.users', string = "salesperson",default=lambda self: self.env.user)

    tag_ids = fields.Many2many('estate_property.tag', string='Tags')

    offer_ids = fields.One2many('estate_property.offer', 'property_id', string='Offers')


class estate_property_type(models.Model):
    _name = "estate_property.type"
    _description = "estate property type"

    name = fields.Char("name",required=True)

class estate_property_tag(models.Model):
    _name = "estate_property.tag"
    _description = "estate property tag"

    name = fields.Char('Tag name',required=True)

class estate_property_offer(models.Model):
    _name = "estate_property.offer"
    _description= "Estate Property offers"

    price = fields.Float()
    status = fields.Selection([
        ('accepted','Accepted'),
        ('refused','Refused')
    ], copy=False)
    partner_id = fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate_property',required=True)
