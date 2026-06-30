from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class AwesomeEstateProperty(models.Model):
    _name = 'awesome.estate.property'
    _description = 'Real Estate Property'
    _rec_name = 'name'
    _order = 'id desc'

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        string="Garden Orientation",
    )
    property_type_id = fields.Many2one(
        'awesome.estate.property.type',
        string="Property Type",
        ondelete='restrict',
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        readonly=True,
        copy=False,
    )
    salesperson_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        'awesome.estate.property.tag',
        string="Tags",
    )
    offer_ids = fields.One2many(
        'awesome.estate.property.offer',
        'property_id',
        string="Offers",
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('canceled', "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default='new',
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute='_compute_total_area',
        store=True,
        help="Total area computed by summing the living area and the garden area.",
    )
    best_price = fields.Float(
        string="Best Offer",
        compute='_compute_best_price',
        store=True,
        help="Best offer received.",
    )

    # -----------------------------------------------------------------------
    # SQL Constraints
    # -----------------------------------------------------------------------
    _check_living_area = models.Constraint(
        'CHECK (living_area >= 0 AND living_area <= 100000)',
        'Living area must be between 0 and 100,000 sqm. Please enter a realistic value.',
    )
    _check_garden_area = models.Constraint(
        'CHECK (garden_area >= 0 AND garden_area <= 100000)',
        'Garden area must be between 0 and 100,000 sqm. Please enter a realistic value.',
    )
    _check_expected_price = models.Constraint(
        'CHECK (expected_price > 0)',
        'Expected price must be greater than zero.',
    )
    _check_selling_price_positive = models.Constraint(
        'CHECK (selling_price >= 0)',
        'The selling price must be positive.',
    )
    _check_bedrooms = models.Constraint(
        'CHECK (bedrooms >= 0)',
        'Bedrooms cannot be negative.',
    )
    _check_facades = models.Constraint(
        'CHECK (facades >= 0)',
        'Facades cannot be negative.',
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and record.expected_price:
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                    raise ValidationError(
                        _("The selling price cannot be lower than 90%% of the expected price.")
                    )

    # -----------------------------------------------------------------------
    # Computed Fields
    # -----------------------------------------------------------------------
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(
                record.offer_ids.mapped('price'), default=0.0)

    # -----------------------------------------------------------------------
    # Onchange Methods
    # -----------------------------------------------------------------------
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # -----------------------------------------------------------------------
    # Action Methods
    # -----------------------------------------------------------------------
    def action_sold(self):
        self.ensure_one()
        if self.state == 'canceled':
            raise UserError(_("Canceled properties cannot be sold."))
        if self.state == 'sold':
            raise UserError(_("Property is already sold."))
        self.state = 'sold'
        return True

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'sold':
            raise UserError(_("Sold properties cannot be canceled."))
        if self.state == 'offer_accepted':
            raise UserError(_("Cannot cancel a property with an accepted offer."))
        self.state = 'canceled'
        return True

    def action_reset(self):
        """Reset sold or canceled property back to 'new' state."""
        self.ensure_one()
        if self.state not in ('sold', 'canceled'):
            raise UserError(_("Only sold or canceled properties can be reset."))
        was_sold = self.state == 'sold'
        self.write({
            'state': 'new',
            'selling_price': 0.0,
            'buyer_id': False,
        })
        if was_sold:
            self.offer_ids.write({'status': False})
        return True

    # -----------------------------------------------------------------------
    # Deletion Guard
    # -----------------------------------------------------------------------
    @api.ondelete(at_uninstall=False)
    def _unlink_except_active_or_sold(self):
        if any(record.state not in ('new', 'canceled') for record in self):
            raise UserError(_("You cannot delete a property with an active or sold status."))
