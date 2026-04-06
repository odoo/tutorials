from odoo import fields, models, api
from odoo.exceptions import ValidationError


class estate_property(models.Model):

    _name = "estate.property"
    _description = "A real estate model with many fields"
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Integer()
    date_availability = fields.Datetime()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')],
        help="Type is used to specify the garden orientation")

    @api.constrains('expected_price')
    def _check_price(self):
        for rec in self:
            if rec.expected_price <= 0:
                raise ValidationError("Price must be positive")
