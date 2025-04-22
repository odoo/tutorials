from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "manage properties"

    name = fields.Char(string = "Name", required=True, default="Unknown")
    description = fields.Text(string = "Description")
    postcode = fields.Char(string = "PostCode")
    date_availability = fields.Date(string = "Availability", copy=False, default=fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float(string = "Excepted price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area")
    garden_orentation = fields.Selection(string="Garden orientation", selection=[('north', 'North'),('south', 'South'), ('ouest', 'West'), ('east', 'East')])