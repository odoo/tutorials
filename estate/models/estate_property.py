from . import fields, models

class TestModel(models.Model):
    _name = "real_esate"
    _description = "Real estate module for managing property listings and transactions!"


    name = fields.Char()
    description= fields.text()
    postcode=fields.char()
    date_availability=fields.Date()
    expected_price=fields.Float()
    expected_price=fields.Float()
    bedrooms=fields.Integer()
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.selection(
        String="Type",
        selection=[
            ('north', 'north'),
            ('south', 'south'),
            ('east', 'east'),
            ('west', 'west')
        ]
    )
