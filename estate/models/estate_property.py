from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"
    name = fields.Char(required=True, string='Title')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,
                                    default=lambda self: fields.Date.today() + relativedelta(months=3),
                                    string='Available From')
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden area (sqm)')
    garden_orientation = fields.Selection(
        selection=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')])
    active: bool = fields.Boolean(default=True)
    state = fields.Selection(copy=False, default='New', required=True, string='Status',
                             selection=[('New', 'New'), ('Offer Received', 'Offer Received'),
                                        ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'),
                                        ('Cancelled', 'Cancelled')])
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(string='Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price', string="Best Offer")

    @api.depends( "living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            self.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"))  # max(offer.price for offer in record.offer_ids)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_set_sold(self):
        for record in self:
            if record.state == 'Cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            record.state = 'Sold'
        return True

    def action_set_cancelled(self):
        for record in self:
            if record.state == 'Sold':
                raise UserError("Sold properties cannot be cancelled.")
            record.state = 'Cancelled'
        return True

    def accept_offer(self, accepted_offer):
        if self.state == 'Offer Accepted':
            raise UserError("An offer has already been accepted.")
        self.state = 'Offer Accepted'
        self.buyer_id = accepted_offer.partner_id
        self.selling_price = accepted_offer.price
        accepted_offer.status = 'Accepted'

        # Refuse other offers
        for offer in self.offer_ids:
            if offer != accepted_offer:
                offer.status = 'Refused'
