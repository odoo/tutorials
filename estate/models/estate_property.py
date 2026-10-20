from datetime import timedelta

from odoo import fields, models


class EstateProperty(models.Model):

    _name = 'estate.property'
    _description = 'Real Estate'

    name = fields.Char(required=True, default="Unknown")
    description = fields.Text(default="Unknown")
    postcode = fields.Char(default="Unknown")
    date_available = fields.Date(copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("east", "East"), ("west", "West"), ("north", "North"), ("south", "South")],
    )
    active = fields.Boolean()
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_recieved", "Offer recieved"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")],
        default="new",
    )
    estate_property_type_id = fields.Many2one("estate.property.type", string="Estate")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
