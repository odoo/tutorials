from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True, default="Unknown")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    description = fields.Text()
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
    salesman_id = fields.Many2one(
        "res.partner", string="Salesman", default=lambda self: self.env.user.id
    )
    buyer_id = fields.Many2one(
        "res.users", string="Buyer", default=lambda self: self.env.user.id, copy=False
    )
    postcode = fields.Char()
    date_availability = fields.Date(copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    offer_ids = fields.One2many(
        "estate.property.offers", "property_id", string="Offers"
    )
