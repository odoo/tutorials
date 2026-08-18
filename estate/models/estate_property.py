from odoo import models, fields
from datetime import timedelta


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Availability Date", copy=False, default=fields.Date.to_date(fields.Date.today() + timedelta(days=3 * 30)))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Number of Bedrooms", default=2)
    living_area = fields.Integer("Living Area m²")
    facades = fields.Integer("Number of Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area m²")
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')])
    state = fields.Selection(string="State", required=True, copy=False, selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], default='new')
    active = fields.Boolean("Active", default=True)

    type = fields.Many2one(string="Type", comodel_name="estate.property.type")
    buyer = fields.Many2one(string="Buyer", comodel_name="res.partner", copy=False)
    seller = fields.Many2one(string="Salesperson", comodel_name="res.users", default=lambda self: self.env.user)

    tags = fields.Many2many(string="Tags", comodel_name="estate.property.tag")

    offers = fields.One2many(string="Offers", comodel_name="estate.property.offer", inverse_name="property")
