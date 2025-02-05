from odoo import fields, models
# import for adding months with relativedelta
from dateutil.relativedelta import relativedelta 

class PropertyPlan(models.Model):
    _name = "estate.property"
    _description = "Estate property tables"

    name = fields.Char(string="Title",required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From",copy=False, default=(fields.Date.today()+relativedelta(months=+3))) #Added 3 months
    expected_price = fields.Float(string="Expected Price",required=True)
    selling_price = fields.Float(string="Selling Price",readonly=True)
    bedrooms = fields.Integer(string="Bedrooms",default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    active = fields.Boolean(string="Active",default=True)

    #selection firld for "State"
    state = fields.Selection(
        string='State',
        required=True,
        default="new",
        copy=False,
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        help="Used to decide the state of Garden")

    #selection firld for "Garden Orientation"
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Used to decide the direction of Garden")
    #Many2one field for property id
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    #Many2many field for property tag
    tag = fields.Many2many("estate.property.tag", string="Property Tag")
    buyer = fields.Char(string="Buyer", copy=False)
    #Many2one field for user name
    sales_person = fields.Many2one('res.users',string="Salesman",default=lambda self: self.env.user)
    #One2many field for partner id from property offer table
    offer_ids = fields.One2many('estate.property.offer','property_id', string='Price')