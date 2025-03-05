from odoo import models, fields
from datetime import datetime, timedelta

class TestModel(models.Model):
    _name = "test.model"
    _description = "Test Model"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")

    # Read-Only 
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    availability_date = fields.Date(
        string="Availability Date",
        default=lambda self: datetime.today() + timedelta(days=90), #3 months
        copy=False
    )
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()

    
    bedrooms = fields.Integer(string="Bedrooms", default=2)    
    active = fields.Boolean(string="Active", default=True)
    postcode = fields.Char()
    date_availability = fields.Date()
    # expected_price = fields.Float(required=True)
    selling_price = fields.Float() 
#   living_area=fields.Integer()
    living_area=fields.Integer()
    # State Field with Selection
    state = fields.Selection([
        ('new', "New"),
        ('offer_received', "Offer Received"),
        ('offer_accepted', "Offer Accepted"),
        ('sold', "Sold"),
        ('cancelled', "Cancelled"),
    ], string="State", required=True, default='new', copy=False)



























# # from odoo import models, fields
# # class AModel(models.Model):
# #     _name = 'a.model.name'

#     # field1 = fields.Char()


# from odoo import models, fields

# class TestModel(models.Model):
#     _name = "test.model"
#     _description = "First Model"
#     name = fields.Char(required=True)
#     # (required=True)

#     description = fields.Text()

#     postcode = fields.Char()
#     date_availability = fields.Date()
#     expected_price = fields.Float(required=True)
#     selling_price = fields.Float()
#     bedrooms = fields.Integer(required=True)
#     living_area=fields.Integer()
#     facades = fields.Integer()
#     garage = fields.Boolean()
#     garden = fields.Boolean()
#     garden_area = fields.Integer()
#     # garden_orientation = fields.Selection()
#     garden_orientation = fields.Selection([
#         ('north', 'North'),
#         ('south', 'South'),
#         ('east', 'East'),
#         ('west', 'West')
#     ], string="Garden Orientation")


# #     class TestModel(models.Model):
# #     _name = "test.model"
# #     _description = "First Model"

# #     name = fields.Char(string="Name", required=True)  # Required field
# #     description = fields.Text(string="Description", help="Detailed description of the property")
# #     postcode = fields.Char(string="Postcode", help="Postal code of the property location")
# #     date_availability = fields.Date(string="Date Availability", help="The date when the property will be available")
# #     expected_price = fields.Float(string="Expected Price", required=True, help="Expected selling price of the property")  # Required field
# #     selling_price = fields.Float(string="Selling Price", help="Final selling price after negotiation")
# #     bedrooms = fields.Integer(string="Bedrooms", help="Number of bedrooms in the property")
# #     living_area = fields.Integer(string="Living Area (sq ft)", help="Total living area size")
# #     facades = fields.Integer(string="Facades", help="Number of facades in the building")
# #     garage = fields.Boolean(string="Garage", help="Does the property have a garage?")
# #     garden = fields.Boolean(string="Garden", help="Does the property have a garden?")
# #     garden_area = fields.Integer(string="Garden Area (sq ft)", help="Size of the garden area")
# #     garden_orientation = fields.Selection([
# #         ('north', 'North'),
# #         ('south', 'South'),
# #         ('east', 'East'),
# #         ('west', 'West')
# #     ], string="Garden Orientation", help="The direction the garden faces")
