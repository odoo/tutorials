from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"

    name = fields.Char(default="Unknown", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=date.today() + relativedelta(months=3), copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    last_seen = fields.Datetime(default=fields.Datetime.now)
    garden_area = fields.Integer("Garden Area (sqm)")
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one('res.partner', string="Salesperson")
    buyer_id = fields.Many2one('res.users')
    property_type_id = fields.Many2one('estate.property.type')
    property_tag_id = fields.Many2many('estate.property.tags')
    offers_id = fields.One2many('estate.property.offer', 'property_id')
    garden_orientation = fields.Selection(
        selection=[
            ('east', "East"),
            ('west', "West"),
            ('north', "North"),
            ('south', "South"),
        ],
        help="This field tells us the direction of the garden"
    )
    state = fields.Selection(
        default='new',
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        help="This field tells us the state of the property."
    )
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Integer(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        self.total_area = (self.living_area or 0) + (self.garden_area or 0)

    @api.depends('offers_id')
    def _compute_best_price(self):
        for record in self:
            record.best_price = (
                max(record.offers_id.mapped('price')) if record.offers_id else 0.0
            )

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None
