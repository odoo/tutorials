from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real state property"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Type",
    )
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.today() + relativedelta(months=3),
        string="Available From",
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
    active = fields.Boolean(default=True)
    seller = fields.Many2one(
        comodel_name="res.users",
        string="Salesman",
        default=(lambda self: self.env.user),
    )
    buyer = fields.Many2one(
        comodel_name="res.partner",
        copy=False,
    )
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )
