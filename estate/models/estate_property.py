from odoo import models, fields

class estate_property(models.Model):
    _name = "estate.property"
    _description = "estate property"

    name= fields.Char("Plan Name", required = True ) # required make property not nullable 
    description =  fields.Text("Plan desc")
    postcode = fields.Char('postcode')
    date_availability = fields.Date(copy=False,default=fields.Date.add(fields.Date.today() , months=3))  
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default='2')
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientations",
        selection=[('north', 'North'),('east','East'),('west','West'),('south','South')],
        help='this is used to select orientations of garden'
    )


    active = fields.Boolean('Active', 
        default=True
        )

    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ]
    )