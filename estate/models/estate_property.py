from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

GARDEN_ORIENTATIONS = [
    ('north', 'North'),
    ('south', 'South'),
    ('east', 'East'),
    ('west', 'West'),
]

PROPERTY_STATUS = [
    ('new', 'New'),
    ('offer received', 'Offer Received'),
    ('offer accepted', 'Offer Accepted'),
    ('sold', 'Sold'),
    ('cancelled', 'Cancelled'),
]


class Property(models.Model):
    _name = "estate.property"
    _description = "An estate property model"

    # === FIELDS ===#

    name = fields.Char(
        required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: self._default_date_availability())
    expected_price = fields.Float(
        required=True)
    selling_price = fields.Float(
        copy=False,
        readonly=True)
    bedrooms = fields.Integer(
        default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=GARDEN_ORIENTATIONS,
    )
    active = fields.Boolean(
        default=True)
    state = fields.Selection(
        copy=False,
        default='new',
        required=True,
        selection=PROPERTY_STATUS,
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string='Property Type')
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user)
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False)
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id")
    total_area = fields.Float(
        compute='_compute_total_area',
        string='Total Area')
    best_price = fields.Float(
        compute='_compute_best_price',
        string='Best Offer')

    # === COMPUTE METHODS ===#

    # Default method to set date_availability to three months from today
    def _default_date_availability(self):
        return fields.Datetime.today() + relativedelta(months=3)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.mapped('offer_ids.price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
