from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class Property(models.Model):
    # Model Attributes
    _name = 'estate.property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Estate Model'
    _order = 'id desc'

    # # SQL Constraints
    # _sql_constraints = [
    #     ('check_expected_price', 'CHECK(expected_price > 0.00)', "The expected price must be strictly positive"),
    #     ('check_selling_price', 'CHECK(selling_price > 0.00)', "The selling price must be strictly positive")
    # ]

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
    commission_fee = fields.Float(string="Commission", required=True, default=lambda self: self.env.user.commission_fee)

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
    is_rent_property = fields.Boolean(string="Is For Rent")
    rent_price = fields.Float(string="Rent Price")
    rent_deposit = fields.Float(string="Rent Deposit")
    rent_start_date = fields.Date(string="Rent Start Date")
    rent_duration = fields.Integer(string="Rent Duration (months)", help="Duration of rental agreement in months")
    rent_end_date = fields.Date(string="Rent End Date", compute='_compute_rent_end_date')
    tenant_id = fields.Many2one('res.partner', string="Tenant")

    # Computed Methods
    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.depends('rent_start_date', 'rent_duration')
    def _compute_rent_end_date(self):
        for record in self:
            if record.rent_start_date and record.rent_duration:
                record.rent_end_date = fields.Date.add(record.rent_start_date, months=record.rent_duration)
            else:
                record.rent_end_date = False

    @api.constrains('is_rent_property', 'rent_price')
    def _check_rent_price(self):
        for record in self:
            if record.is_rent_property and record.rent_price <= 0:
                raise ValidationError(_("Rent price must be strictly positive for rental properties."))

    @api.onchange('rent_price')
    def _onchange_rent_price(self):
        if self.rent_price:
            self.rent_deposit = self.rent_price * 2

    @api.constrains('expected_price', 'selling_price', 'is_rent_property')
    def _check_prices_for_sale(self):
        for record in self:
            if not record.is_rent_property:  # Only for Sale properties
                if record.expected_price <= 0:
                    raise ValidationError(_("The expected price must be strictly positive for sale properties."))
                if record.selling_price and record.selling_price <= 0:
                    raise ValidationError(_("The selling price must be strictly positive for sale properties."))

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
            if not (property.state == 'offer_accepted'):
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
