from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "real estate properties"

    name = fields.Char('Title', default="Unknown", required=True)
    description = fields.Char('Descrption')
    postcode = fields.Char('Postcode', required=True, default='00000')

    availability_date = fields.Date('Availability', copy=False, default=(fields.Date.today() + relativedelta(days=30)))
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2, required=True)
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    expected_price = fields.Float('Expected Price', required=True)
    living_area = fields.Float('Living Area (sqm)')
    facades = fields.Integer('Facades', required=True)
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Float('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('west', 'West'),
            ('east', 'East'),
            ('south', 'South'),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Property State',
        selection=[
            ('new', 'New'),
            ('offer Received', 'Offer Received'),
            ('offer Accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
    )

    Property_type_id = fields.Many2one('estate.property.type', 'Property Type')
    partner_id = fields.Many2one('res.partner', 'Partner')
    seller_id = fields.Many2one('res.users', 'Salesperson', default=lambda self: self.env.user, copy=False)
    tag_ids = fields.Many2many('estate.property.tag', 'property_tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float('Total Area', compute="_compute_total_area")
    best_offer = fields.Float('Best Offer', compute="_compute_best_offer")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids and record.offer_ids.price:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 20
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
