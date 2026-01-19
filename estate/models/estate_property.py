from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property Planning'
    _order = 'id desc'  # defaultvalue = asc

    name = fields.Char(required=True, default="Unknown")
    description = fields.Text()
    postcode = fields.Float()
    date_availability = fields.Date(
        "Available From", copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3)
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
        default='new',
    )
    property_type_id = fields.Many2one(
        'estate.property.type', string="Property Type")
    seller_id = fields.Many2one(
        'res.users', string="Salesman", default=lambda self: self.env.user
    )
    buyer_ids = fields.Many2one('res.partner', string="Buyer", copy=False)
    tags_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(compute='_compute_total_area')
    best_price = fields.Float(
        "Best offer", compute='_compute_best_price', store=True)

    property_maintenance_requests = fields.One2many(
        'estate.property.maintenance.requests', 'property_id')
    total_maintenance_cost = fields.Float(
        compute='_compute_total_maintenance_cost', string="Total Maintenance Cost")

    # SQL Constraint
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)', "The expected price must be strictly positive")
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)', "The selling price must be  positive")

    # Python Constriant
    @api.constrains('selling_price', 'expected_price')
    def _check_price(self):
        if self.buyer_ids and self.selling_price < (self.expected_price * 0.9):
            raise ValidationError(
                "The selling price must be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer.")

    # Compute Methods
    # Depends Decorator
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = (
                max(record.offer_ids.mapped('price')
                    ) if record.offer_ids else 0.0
            )

    @api.depends('property_maintenance_requests.cost')
    def _compute_total_maintenance_cost(self):
        for record in self:
            record.total_maintenance_cost = (
                sum(record.property_maintenance_requests.mapped('cost')
                    ) if record.property_maintenance_requests else 0.0
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
        else:
            for record in self:
                if record.property_maintenance_requests.status != 'done':
                    raise UserError(
                        "Property cannot be sold if there is any maintenance request not done.")
        return self.write({'state': 'sold'})

    def action_cancel(self):
        if 'sold' in self.mapped('state'):
            raise UserError("Sold properties cannot be cancelled.")
        return self.write({'state': 'cancelled'})

    # Ondelete Decorator
    @api.ondelete(at_uninstall=False)
    def _check_state(self):
        for record in self:
            if record.state in ('offer_received', 'offer_accepted'):
                raise UserError(
                    "Only new and canceled properties can be deleted.")
