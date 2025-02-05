from odoo import fields, models
from dateutil.relativedelta import relativedelta


class estate_property(models.Model):
    _name="estate.property"
    _description="Estate Model"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode=fields.Char()
    date_availability = fields.Date(
        copy=False,
        default= (fields.Date.today() + relativedelta(months=3))
        # default=fields.Date.add(fields.Date.today() , months=3)
    )    
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(defualt=2 )
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'),('east', 'East'),('west', 'West')],
    )
    active = fields.Boolean(default = 'True')
    status = fields.Selection(
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted','Offer Accepted'), ('sold','Sold'), ('cancelled','cancelled')],
        default = 'new'
    )
