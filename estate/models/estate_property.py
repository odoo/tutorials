from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    living_area = fields.Integer()
    postcode = fields.Char()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    date_availability = fields.Date(
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        copy=False,
    )
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    bedrooms = fields.Integer(default=2)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one(comodel_name="estate.property.type")
    buyer_id = fields.Many2one(comodel_name="res.partner", copy=False)
    salesperson_id = fields.Many2one(
        comodel_name="res.users", string="Salesperson", required=True, default=lambda self: self.env.user
    )
