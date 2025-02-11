from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True, compute="_compute_best_offer")
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area", store=True)
    best_offer = fields.Float(compute="_compute_best_offer", store=True)
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string="Status",
        required=True,
        copy=False,
        default='new'
    )    
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        breakpoint()
        for record in self:
            record.total_area = record.living_area + record.garden_area
    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0)
            record.expected_price = max(record.offer_ids.mapped("price"), default=0)
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False  

    def action_set_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be sold.")
            if not record.offer_ids:
                raise UserError("You cannot sell a property without an accepted offer.")
            accepted_offers = record.offer_ids.filtered(lambda offer: offer.status == "accepted")
            if not accepted_offers:
                raise UserError("You must accept an offer before selling.")
            accepted_offer = accepted_offers.sorted(key=lambda o: o.price, reverse=True)[0]
            record.state = "sold"
            record.selling_price = accepted_offer.price
            record.buyer_id = accepted_offer.partner_id


    def action_set_cancel(self): 
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled.")
            record.state = "cancelled"

