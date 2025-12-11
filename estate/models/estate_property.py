from dateutil.relativedelta import relativedelta
from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"
    state = fields.Selection(selection = [("New","New"), ("Offer_Received","Offer Received") ,("Offer_Accepted","Offer Accepted"), ("Sold","Sold"), ("Cancelled","Cancelled")])
    active = fields.Boolean('Active',default=True)
    name = fields.Char(required=True,default="Unkown")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From",copy=False,default= fields.Datetime.today() + relativedelta(months=3))
    last_seen= fields.Date("Last Seen", default=fields.Datetime.now)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('North','North'),('South','South'),('East','East'),('West','West')])
    property_type_id = fields.Many2one("estate.property.type",string="Type")
    buyer_id = fields.Many2one("res.partner",string="Buyer")
    seller_id = fields.Many2one("res.users",default=lambda self : self.env.user,string="Seller")
    tag_ids = fields.Many2many("estate.property.tag",string="Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id",string="Offers")
    