from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    postcode = fields.Char(required=True)
    available_from = fields.Date(
        string="Availble From",
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer(default=0)
    living_area = fields.Integer(required=True)
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
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
