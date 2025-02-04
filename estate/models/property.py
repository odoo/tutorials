from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class Property(models.Model):
    # Model Attributes
    _name = 'estate.property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Estate Model'
    _order = 'id desc'

    # SQL Constraints
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0.00)', "The expected price must be strictly positive"),
        ('check_selling_price', 'CHECK(selling_price > 0.00)', "The selling price must be strictly positive")
    ]

    # Basic Fields
    name = fields.Char(string="Property Name", required=True, tracking=True)
    description = fields.Text(string="Description")
    image_1920 = fields.Image(string="Property Image")
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env.user.company_id,
        required=True
    )

    # Relational Fields
    property_type_id = fields.Many2one(
        'estate.property.type',
        default=lambda self: self.env.ref('estate.property_type_1'),
        string="Property Type"
    )
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user, tracking=True)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False, tracking=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    # Basic Fields
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Availability",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False, tracking=True)
    bedrooms = fields.Integer(string="No of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string = "Garden Orientation",
        selection = [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ]
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        readonly=True,
        string="Status",
        selection = [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled")
        ],
        default='new',
        tracking=True
    )

    # Computed Fields
    total_area = fields.Integer(compute='_compute_total', string="Total Area")
    best_price = fields.Float(compute='_compute_best_price', string="Best Price")

    # Computed Methods
    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    # Python Constraints
    @api.constrains('selling_price')
    def _check_selling_price_constrains(self):
        for record in self:
            if record.selling_price and record.selling_price < (record.expected_price * 0.9):
                raise ValidationError(_(f"Selling price cannot be lower than {record.expected_price * 0.9} (90% of the expected price)."))

    # Onchange Methods
    @api.onchange('garden')
    def _onchange_garden(self):
        self.write({
            'garden_area' : 10 if self.garden else 0,
            'garden_orientation' : 'north' if self.garden else False
        })

    # Actions
    def action_sold(self):
        self.ensure_one()
        for property in self:
            if property.state == 'cancelled':
                raise UserError(_("Cancelled property can not be sold."))
            elif property.state == 'sold':
                raise UserError(_("Property already sold."))
            accepted_offer = self.env['estate.property.offer'].search([
                ('property_id', '=', self.id),
                ('status', '=', 'accepted')
            ], limit=1)
            if not accepted_offer:
                raise UserError(_("You cannot sell a property without an accepted offer."))
            property.state = 'sold'

    def action_cancel(self):
        self.ensure_one()
        for property in self:
            if property.state == 'sold':
                raise UserError(_("Sold property can not be cancelled."))
            elif property.state == 'cancelled':
                raise UserError(_("Property already Cancelled."))
            property.state = 'cancelled'

    @api.ondelete(at_uninstall=False)
    def _unlink_prevent_if_state_new_or_cancelled(self):
        if any(record.state not in ['new', 'cancelled'] for record in self):
            raise UserError(_("You cannot delete a property whose state is not 'new' or 'cancelled'"))

    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'sold':
            message = (
                f"Property sold by {self.salesperson_id.name} to {self.buyer_id.name} "
                f"for a price of {self.selling_price}."
            )
            self.message_post(body=message)
            return self.env.ref('estate.estate_property_mt_state_change')
        return super(Property, self)._track_subtype(init_values)
