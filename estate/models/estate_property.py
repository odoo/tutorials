from odoo import exceptions, api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False, compute="_compute_selling_price")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')])
    active = fields.Boolean(default=True)
    stage = fields.Selection([('new', 'New'), ('offer_received', 'Offer received'), ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], required=True, copy=False, default='new', string="Status")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", compute='_compute_buyer_id')
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area')
    best_price = fields.Char(compute='_compute_best_price', string='Best Offer')

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.depends('offer_ids')
    def _compute_selling_price(self):
        for record in self:        
            if record.offer_ids and "accepted" in record.offer_ids.mapped("status"):
                for offer in record.offer_ids:
                    if offer.status == "accepted":
                        record.selling_price = offer.price
            else:
                record.selling_price = None

    @api.depends('offer_ids')
    def _compute_buyer_id(self):
        for record in self:
            if record.offer_ids and "accepted" in record.offer_ids.mapped("status"):
                for offer in record.offer_ids:
                    if offer.status == "accepted":
                        record.buyer_id = offer.partner_id
            else:
                record.buyer_id = None

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = None
            self.garden_area = None

    def action_sell(self):
        for record in self:
            if record.stage != 'cancelled':
                record.stage = 'sold'
                return True
            else:
                raise exceptions.UserError("Cannot sell a property that is already cancelled.")

    def action_cancel(self):
        for record in self:
            if record.stage != 'sold':
                record.stage = 'cancelled'
                return True
            else:
                raise exceptions.UserError("Cannot cancel a property that is already sold.")
