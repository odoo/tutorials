from odoo import fields, models
from datetime import date, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "reals estate properties"

    name = fields.Char('Property Name',required=True)
    offer_ids=fields.One2many("estate.property.offer","property_id",string="Offers Received")
    tag_ids=fields.Many2many("estate.property.tags",string="Tags")
    buyer_id=fields.Many2one("res.partner",string="Buyer")
    salesperson_id=fields.Many2one("res.users",string="Sales Person",default=lambda self: self.env.user)
    property_type_id = fields.Many2one("estate.property.types", string="Property Type")
    description = fields.Text('The Descritption')
    postcode = fields.Char()
    date_availability = fields.Date(default=date.today()+ timedelta(days=90),copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False,readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area= fields.Integer()
    garden_orientation = fields.Selection([("North","North"),("South","South"),("East","East"),("West","West")])
    active = fields.Boolean(default=True)
    state = fields.Selection([("New","New"),("Offer Received","Offer Received"),("Offer Accpeted","Offer Accepted"),("Solde","Solde"),("Cancelled","Cancelled")],copy=False,default="New")
