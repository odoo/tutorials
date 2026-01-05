from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property Planning'

    name = fields.Char(required=True, default="Unknown")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From", copy=False, default=fields.Datetime.now
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('west', "West"),
            ('east', "East"),
            ('south', "South"),
        ],
        help="Direction for the garden"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default="new",
    )
    property_type_id = fields.Many2one(
        'estate.property.type', string="Property Type")
    seller = fields.Many2one(
        'res.users', string="Salesman", default=lambda self: self.env.user
    )
    buyer = fields.Many2one('res.partner', string="Buyer", copy=False)
    tags = fields.Many2many('estate.property.tag')
    offer = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(compute='_compute_total')
    best_price = fields.Float("Best offer", compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer')
    def _compute_best_price(self):
        for record in self:
            record.best_price = (
                max(record.offer.mapped('price')) if record.offer else 0.0
            )

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = "10"
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None
