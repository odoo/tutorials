from dateutil.relativedelta import relativedelta
from odoo import api, models, fields, exceptions


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    notes = fields.Html()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True, copy=False, compute="_compute_selling_price_and_buyer")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], default='new', required=True, copy=False)
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer",
                               copy=False, compute="_compute_selling_price_and_buyer")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.uid)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(
        compute="_compute_total_area", string="Total Area (sqm)")
    best_offer = fields.Float(
        compute="_compute_best_offer", string="Best Offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for property in self:
            if property.offer_ids:
                property.best_offer = max(property.offer_ids.mapped('price'))
            else:
                property.best_offer = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = None
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'

    def action_set_sold(self):
        for property in self:
            if property.state != 'cancelled':
                property.state = 'sold'
            else:
                raise exceptions.UserError(
                    "Cancelled properties cannot be sold.")

    def action_set_cancelled(self):
        for property in self:
            if property.state != 'sold':
                property.state = 'cancelled'
            else:
                raise exceptions.UserError(
                    "Sold properties cannot be cancelled.")

    @api.depends('offer_ids')
    def _compute_selling_price_and_buyer(self):
        for property in self:
            accepted_offers = property.offer_ids.filtered(
                lambda o: o.status == 'accepted')
            if accepted_offers:
                best_offer = max(accepted_offers, key=lambda o: o.price)
                property.selling_price = best_offer.price
                property.buyer_id = best_offer.partner_id
            else:
                property.selling_price = 0.0
                property.buyer_id = None
