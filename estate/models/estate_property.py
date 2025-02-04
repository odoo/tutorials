from odoo import fields, models
# import for adding months with relativedelta
from dateutil.relativedelta import relativedelta 

class PropertyPlan(models.Model):
    _name = "estate.property"
    _description = "Estate property tables"

    name = fields.Char(string="Name",required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date Availability",copy=False, default=(fields.Date.today()+relativedelta(months=+3))) #Added 3 months
    expected_price = fields.Float(string="Expected Price",required=True)
    selling_price = fields.Float(string="Selling Price",readonly=True)
    bedrooms = fields.Integer(string="Bedrooms",default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    active = fields.Boolean(string="Active",default=True)

    #selection firld for "State"
    state = fields.Selection(
        string='Atate',
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