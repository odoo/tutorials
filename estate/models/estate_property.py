from odoo import fields,models,api
from datetime import datetime, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description =" Good real estate"

    name= fields.Char(required=True)
    description=fields.Text()
    postcode=fields.Char()
    date_availability = fields.Date(default= datetime.now() + timedelta(days=90))
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    garden_area=fields.Integer()
    total_area= fields.Integer(compute='_compute_total_area')
    facades=fields.Integer()
    garage= fields.Boolean()
    garden= fields.Boolean()
    garden_orientation= fields.Selection(string='Garden orientation',
        selection=[
            ('North', 'North'),
            ('West', 'West'),
            ('South', 'South'),
            ('East', 'East')
        ]
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True,
        default='new',
        copy=False
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string='Offers')
    best_price= fields.Float(compute='_compute_best_price')
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', copy=False, string='Buyer')
    property_tags_ids=fields.Many2many('estate.property.tag')

    @api.depends('garden_area','living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area= record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price= max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'North'
            else:
                record.garden_area = 0
                record.garden_orientation = False
