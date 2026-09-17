from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstatePropertyModel(models.Model):
    _name = "estate_property"
    _description = "The details of a property"

    name = fields.Char('Estate Name', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(default=0)
    facades = fields.Integer()
    has_garage = fields.Boolean()
    has_garden = fields.Boolean()
    garden_area = fields.Integer(default=0)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
           ('east', 'East'),
           ('west', 'West'),
           ('north', 'North'),
           ('south', 'South'),
           ('', ''),
        ],
    )
    state = fields.Selection(
        string='State',
        selection=[
           ('new', 'New'),
           ('offer_received', 'Offer Received'),
           ('offer_accepted', 'Offer Accepted'),
           ('sold', 'Sold'),
           ('cancelled', 'Cancelled'),
        ],
        default='new',
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate_property_type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    property_tags_ids = fields.Many2many("estate_property_tag", string="Tags")
    offers_ids = fields.One2many("estate_property_offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", readonly=True)
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer", readonly=True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offers_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offers_ids:
                record.best_price = max(record.offers_ids.mapped('price'))

    @api.onchange("has_garden")
    def _onchange_has_garden(self):
        self.garden_area = 10 if self.has_garden else 0
        self.garden_orientation = 'south' if self.has_garden else ''
