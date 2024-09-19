import datetime

from odoo import models, fields, api


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
    expected_price = fields.Float(
        required=True,
        help="The price you expect the property to be sold for",
    )
    selling_price = fields.Float("Selling price", compute="_compute_selling_price", readlonly=True, store=True)
    bedrooms = fields.Integer("Bedrooms", default=2, required=False, help="Number of bedrooms of your property")
    living_area = fields.Float("Living area (sqm)", default=0)
    facades = fields.Integer("Facades", required=False, help="Number of facades of your property")
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Has a garden", required=True, default=False, help="Whether the property has a garden")
    garden_area = fields.Float("Garden area (sqm)", default=lambda self: self._garden_area_default())
    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        default=lambda self: self._garden_orientation_default()
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
    total_area = fields.Float("Total area", compute="_compute_total_area", store=True)
    best_offer = fields.Float("Best offer", compute="_compute_best_offer", store=True)

    def _garden_area_default(self):
        return 10

    def _garden_orientation_default(self):
        return 'north'

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = self.garden and self._garden_area_default() or None
        self.garden_orientation = self.garden and self._garden_orientation_default() or None

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0)

    def _compute_selling_price(self):
        pass
