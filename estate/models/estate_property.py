from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is property tabel."

    name = fields.Char("Property Name", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today()+relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer()
    living_area = fields.Integer(default=0)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(default=0)
    total_area = fields.Integer(compute="_compute_total_area", store=True)
    best_price = fields.Integer(compute="_compute_best_price", store=True)
    garden_orientation = fields.Selection( 
        string="Garden Orientation",
        selection=[
            ('north', 'North'), 
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ])
    active = fields.Boolean(default=True)
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
    buyer_id = fields.Many2one("res.partner" , string="Buyers" , copy=False)
    seller_id = fields.Many2one("res.users" ,default=lambda self : self.env.user, string="Sellers")
    tag_ids = fields.Many2many(comodel_name="estate.property.tag" ,relation="property_tag_rel" ,string="Tags")
    offer_ids = fields.One2many(comodel_name="estate.property.offer" ,inverse_name="property_id" ,string="Offers")

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        self.total_area = self.garden_area+self.living_area
    
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price') or [0])

    @api.onchange('garden')
    def _conchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:    
            self.garden_orientation = None
            self.garden_area = 0
