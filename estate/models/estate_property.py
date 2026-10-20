from odoo import fields, models

from datetime import date, timedelta

default_availability_date = (date.today() + timedelta(days=90))


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    property_type_id = fields.Many2one("estate.property.type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: default_availability_date)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(selection=[
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West"),
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection(required=True, copy=False, default="new", selection=[
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("cancelled", "Cancelled"),
    ])
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
