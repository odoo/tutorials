from odoo import api, fields, models
import datetime as dt

from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property information"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()

    date_availability = fields.Date(copy=False, default=fields.Date.today() + dt.timedelta(weeks=3*4))

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(compute="_compute_selling_price", copy=False)

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    total_area = fields.Integer(compute="_compute_area")

    active = fields.Boolean(default=True)

    state = fields.Selection(
        required=True, copy=False,
        selection=[
            ('new', 'New'), 
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new')

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, compute="_compute_buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)

    tag_ids = fields.Many2many("estate.property.tag", string='Tags')

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    best_offer = fields.Float(compute="_compute_best_offer")

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_offer = max(prices, default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else None

    def action_set_property_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properties cannot be cancelled!')    
            record.state = 'cancelled'
        return True

    def action_set_property_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('Cancelled properties cannot be sold!')
            record.state = 'sold'
        return True


    @api.depends('offer_ids.status')
    def _compute_selling_price(self):
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offer:
                record.selling_price = accepted_offer.mapped('price')[0] # fallback to first if somehow multiple record, TODO: constraints later?
            else:
                record.selling_price = 0.0

    @api.depends('offer_ids.status')
    def _compute_buyer(self):
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offer:
                record.buyer_id = accepted_offer.mapped('partner_id')[0]
            else:
                record.buyer_id = None
