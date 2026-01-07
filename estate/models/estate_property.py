from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


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
        string="Status",
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

    # SQL Constraint
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)', "The expected price must be strictly positive")
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)', "The selling price must be  positive")

    # Python Constriant
    @api.constrains('selling_price', 'expected_price')
    def _check_price(self):
        if self.buyer and self.selling_price < (self.expected_price * 0.9):
            raise ValidationError(
                "The selling price must be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer.")

    # Compute Methods
    # Depends Decorator
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

    # Onchange Decorator
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = "10"
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    # Action Methods
    def action_sold(self):
        if 'cancelled' in self.mapped('state'):
            raise UserError("Cancelled properties cannot be sold.")
        return self.write({'state': 'sold'})

    def action_cancel(self):
        if 'sold' in self.mapped('state'):
            raise UserError("Sold properties cannot be cancelled.")
        return self.write({'state': 'cancelled'})
