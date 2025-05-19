from odoo import fields, models

class EstateModel(models.Model):
    _name = "test_estate_model"
    _description = "Unreal estate moves a lot more than real one"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection = [("North","North"),("South","South"),("East","East"),("West","West")])
