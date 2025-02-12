from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property model to store all the information about property such as name , price , area etc..."
    _order = "id desc"

    name = fields.Char("Property Name", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available from",copy=False, default=fields.Date.today()+relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer()
    living_area = fields.Integer(default=0)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(default=0)
    total_area = fields.Integer(compute="_compute_total_area",)
    best_price = fields.Integer(compute="_compute_best_price",)
    garden_orientation = fields.Selection( 
        string="Garden Orientation",
        selection=[
            ('north', 'North'), 
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ])
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type" , string="Property Type")
    partner_id = fields.Many2one("res.partner" , string="Buyers" , copy=False)
    user_id = fields.Many2one("res.users" ,default=lambda self : self.env.user, string="Sellers")
    tag_ids = fields.Many2many("estate.property.tag" ,relation="estate_property_tag_rel" ,string="Tags")
    offer_ids = fields.One2many("estate.property.offer" ,inverse_name="property_id" ,string="Offers")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 
         'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 
         'The selling price must be positive or zero.')
    ]

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
    
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price') or [0])

    @api.onchange('garden')
    def _ontoggle_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:    
            self.garden_orientation = None
            self.garden_area = 0


    def action_sold(self):
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
            record.partner_id = accepted_offer.partner_id


    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled!")
            record.state = "cancelled"
    

    def action_back_to_draft(self): 
        for record in self:
            accepted_offers = record.offer_ids.filtered(lambda o: o.status == "accepted")
            accepted_offers.write({'status': 'refused'})
            record.state = "new"
