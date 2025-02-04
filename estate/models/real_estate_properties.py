from odoo import fields, models

class realEstateProperty(models.Model):
    _name = "estate_property"
    _description = "Real Estate property table :)"

    id = fields.Integer()
    create_uid = fields.Integer()
    create_date = fields.Datetime('Write Date', readonly=True)
    write_uid = fields.Integer()
    write_date = fields.Datetime('Write Date', readonly=True)
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char('postcode')
    date_availability = fields.Date('date_availability', readonly=True)
    expected_price = fields.Float('expected_price', required=True)
    selling_price = fields.Float('selling_price')
    bedrooms = fields.Integer('bedrooms')
    living_area = fields.Integer('living_area')
    facades = fields.Integer('facades')
    garage = fields.Boolean('garage')
    garden = fields.Boolean('garden')
    garden_area = fields.Integer('garden_area')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='garden_orientation')