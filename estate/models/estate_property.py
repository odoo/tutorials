import datetime

from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "name, id"

    _sql_constraints = [
        ('estate_property_check_bedrooms', 'CHECK(bedrooms IS NULL OR bedrooms >= 0)',
         'Bedrooms must be a non-negative number or NULL.'),
        ('check_facades', 'check(facades is NULL OR (facades >= 0 AND facades <= 4))',
         'The number of facades must be 0 <= facades <= 4'),
    ]

    name = fields.Char("Name", required=True, index=True, help="Name of the property")
    description = fields.Text("Description", translate=True)
    postcode = fields.Char("Postcode", help="Postcode of the property")
    available_from = fields.Date("Date", required=True,
                                 default=lambda _: datetime.date.today() + datetime.timedelta(days=30 * 3))
    currency_id = fields.Many2one(
        'res.currency', string="Currency",
    )
    expected_price = fields.Monetary(
        required=True,
        help="The price you expect the property to be sold for",
    )
    selling_price = fields.Monetary("Selling price", compute="_compute_selling_price", readlonly=True, store=True)
    bedrooms = fields.Integer("Bedrooms", default=2, required=False, help="Number of bedrooms of your property")
    living_area = fields.Float("Living area (sqm)", default=0)
    facades = fields.Integer("Facades", required=False, help="Number of facades of your property")
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Has a garden", required=True, default=False, help="Whether the property has a garden")
    garden_area = fields.Float("Garden area (sqm)", default=0)
    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    state = fields.Selection(
        string="State",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        default="new",
        required=True,
        copy=False,
        help="State of the property.\n"
             "new: A new property that has just been listed.\n"
             "offer_received: An offer has been made on the property.\n"
             "offer_accepted: The seller has accepted an offer.\n"
             "sold: The property has been sold and the sale is finalized.\n"
             "canceled: The listing has been canceled.",
    )
    active = fields.Boolean('Active', default=True)
    property_type_id = fields.Many2one("estate.property.type", "Property types")
    buyer_id = fields.Many2one("res.partner", "Buyer")
    salesperson_id = fields.Many2one("res.users", "Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    def _compute_selling_price(self):
        return 42069
