from odoo import fields, models
from dateutil.relativedelta import relativedelta


class Properties(models.Model):
    _name = "estate.properties"
    _description = "Information of Properties"

    name = fields.Char(required=True, string="Title")
    expected_price = fields.Float(required=True)
    description = fields.Text()
    Postcode = fields.Char()
    date_avaibility = fields.Date(string = "Available From",copy = False,default = fields.Date.today() + relativedelta(months=+3))
    expected_price = fields.Float(string = "Expected Price")
    Selling_price = fields.Float(readonly=True,copy=False,default=500)
    Bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string = "Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string = "Garden Area (sqm)")
    garden_orientation = fields.Selection([('north','North'),('south' , 'South'),('east','East'),('west','West')],string = "Garden Orientation")
    # active = fields.Toggle_active()
    active = fields.Boolean('Active', default=True)
    status = fields.Selection([('new','New'),('offer recieved' , 'Offer Recieved'),('offer accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')], default="new")