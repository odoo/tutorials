from odoo import fields, models
from dateutil.relativedelta import relativedelta


class Property_Plan(models.Model):
    _name = "estate.property"
    _description = "Test Model"
   
    name = fields.Char(required=True,string="Title")

    tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    #One2Many
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="OfferID")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer',copy=False)

    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=fields.Date.today()+ relativedelta(months=3),string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[("north","North"), ("south","South"),("east","East"),("west","West")],
        help="Type is used for direction"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ],required=True,copy=False,default='new')
