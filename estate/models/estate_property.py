from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperties(models.Model):
    _name = "estate.property"
    _description = " Estate Properties"
    _order = "id desc"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        'Available From', default=fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='State',
        default='new',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ]
    )
    property_type_id = fields.Many2one(
        'estate.property.types', string="Property Type")
    buyer = fields.Many2one('res.partner', string="Buyer")
    salesperson = fields.Many2one(
        'res.users', string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", store=True)
    best_price = fields.Float(
        compute="_compute_best_price", string="Best Offer")

    # -------------------------------------------------------------------------
    # SQL Constraints
    # -------------------------------------------------------------------------

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be positive'),
    ]

    # -------------------------------------------------------------------------
    # Python Constraints
    # -------------------------------------------------------------------------

    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        for property in self:
            if float_is_zero(property.selling_price, precision_digits=2):
                continue

            valid_selling_price = property.expected_price * 0.9
            if float_compare(property.selling_price, valid_selling_price, precision_digits=2) < 0:
                raise ValidationError(
                    "Selling price should not be less than 90% of the expected price!")

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.mapped('offer_ids.price')) if property.offer_ids else 0

    # -------------------------------------------------------------------------
    # OnChange METHODS
    # -------------------------------------------------------------------------

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def action_set_sold_property(self):
        if self.state == 'cancelled':
            raise UserError("Cancelled property can't be sold!")
        if self.state in ['new', 'offer_received']:
            raise UserError("To sell a property, it must have an offer and the state must be 'offer accepted'.")
        self.state = 'sold'
        return True

    def action_cancel_property_conditional(self):
        if self.state == 'offer_accepted':
            # Show confirmation wizard
            return {
                'type': 'ir.actions.act_window',
                'name': 'Confirm Cancellation',
                'res_model': 'estate.property.cancel.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_property_id': self.id,
                    'default_property_name': self.name,
                },
            }
        else:
            return self.action_cancel_property()

    def action_cancel_property(self):
        if self.state != 'sold':
            self.state = 'cancelled'
            return True
        else:
            raise UserError("Sold property can't be cancelled")

    # ------------------------------------------------------------
    # OnDelete Method
    # ------------------------------------------------------------

    @api.ondelete(at_uninstall=False)
    def _check_state_before_delete(self):
        for record in self:
            if record.status not in ['new', 'cancelled']:
                raise UserError("Only new and cancelled property can be deleted!")
