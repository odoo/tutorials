from odoo import models, fields


class TestModal(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _postcode = "estate.postcode"
    _date_avalilabilty = "estate.date_availability"
    _expected_price = "estete.expected_price"
    _selling_price = "estate.selling_price"
    _bedrooms = "estate.bedrooms"
    _living_area = "estate.living_area"
    _facades = "estate.facades"
    _garage = "estate.garage"
    _garden = "estate.garden"
    _garden_area = "estate.garden_area"
    _garden_orientation = "estate.garden_orientation"

    name = fields.Char(required=True)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(required=True)
    facades = fields.Integer(required=True)
    garage = fields.Boolean(required=True)
    garden = fields.Boolean(required=True)
    garden_area = fields.Integer(required=True)
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South")], required=True
    )
    description = fields.Text()
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
