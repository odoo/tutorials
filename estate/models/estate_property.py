from odoo import api, models, fields
from datetime import date, timedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"

    name = fields.Char("Estate name", required=True, translate=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From", default=lambda _: date.today() + timedelta(91), copy=False
    )
    expected_price = fields.Float()
    selling_price = fields.Float("Actual Price", readonly=True)
    bedrooms = fields.Integer(default=2, copy=False)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        copy=False,
        default="new",
        required=True,
    )
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        help="Orientation of the estate property",
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    seller_id = fields.Many2one('res.users', string="Salesman")
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    best_price = fields.Float(compute="_compute_best_offer")

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            record.best_price = 0
            for offer in record.offer_ids:
                if record.best_price < offer.price:
                    record.best_price = offer.price

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
