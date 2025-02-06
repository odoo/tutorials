from odoo import fields, models

class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Estate Model"

    name = fields.Char(required=True)
    id = fields.Integer(required=True)
    create_uid = fields.Integer()
    create_date = fields.Date()
    write_uid = fields.Integer()
    write_date = fields.Date()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From" , copy = False , default=fields.Date.add(fields.Date.today() , days = 90))
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True , copy = False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ( 'offer_accepted', 'Offer Accepted'),
        ('sold' , 'Sold'),
        ('canceled' , 'Canceled')],
        required = True,
        default = "new" ,
        copy = False
      )
    active = fields.Boolean(default=True)
