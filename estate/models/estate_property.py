from odoo import models, fields
import odoo.tools.date_utils as date_utils


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    # Basics
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    tag_ids = fields.Many2many(comodel_name="estate.property.tag", string="Tags")

    # Sales info
    type_id = fields.Many2one(comodel_name="estate.property.type", string="Type")
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda x: date_utils.add(
            fields.Date.today() + date_utils.relativedelta(months=3)
        ),
    )
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    salesman_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesman",
        default=lambda self: self.env.user.id,
    )

    # General information
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()

    # Garden information
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )

    # State
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ]
    )
