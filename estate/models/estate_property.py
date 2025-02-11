from odoo import api, fields, models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char("Property Name", required=True)
    active = fields.Boolean(default=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postal Code")
    date_availability = fields.Date(
        "Availability Date",
        copy=False,
        default= lambda self: fields.Datetime.now() + relativedelta(months=3)
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Number of bedrooms", default=2)
    living_area = fields.Float("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Float("Garden Area (sqm)")
    buyer = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Property Tag"
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers"
    )
    salesman = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user
    )
    garden_orientation = fields.Selection(
        selection = [
            ('north', 'North'),
            ('south', 'South'),
            ('west', 'West'),
            ('east', 'East')
        ]
    )
    state = fields.Selection(
        selection = [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True, copy=False, default="new"
    )
    total_area = fields.Float("Total Area(sqm)", compute="_compute_total_area")
    best_price = fields.Float("Best Price", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            max_price=0
            for offer in record.offer_ids:
                if offer.price > max_price:
                    max_price = offer.price
            record.best_price = max_price

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

    def sold_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold")
            else:
                record.state = 'sold'

    def cancelled_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled")
            else:
                record.state = 'cancelled'
