from odoo import fields, models


class properties(models.Model):
    _name = "estate_properties"
    _description = "Estate properties"

    name = fields.Char('name')
    description = fields.Text("description")
    postcode = fields.Char("Postal code")
    date_availability = fields.Date("Date availability")
    expected_price = fields.Float("Expected price")
    selling_price = fields.Float("Selling price")
    bedrooms = fields.Integer("Bedrooms")
    living_area = fields.Integer("Living area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden area")
    garden_orientation = fields.Selection(string='Type',
                                          selection=[("North"), ('South'), ("East"), ("West")])
