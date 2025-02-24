from markupsafe import Markup
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order= 'id desc'

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3)
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
        string="Garden Orientation",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ]
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled")
        ],
        default='new'
    )
    active = fields.Boolean(string="Active", default=True)
    property_type_id = fields.Many2one(string="Property Type", comodel_name='estate.property.type')
    buyer_id = fields.Many2one(string="Buyer", comodel_name='res.partner', copy=False)
    sales_id = fields.Many2one(string="Salesman", comodel_name='res.users', default=lambda self: self.env.user)
    tag_ids = fields.Many2many(string="Tags", comodel_name='estate.property.tag')
    offer_ids = fields.One2many(string="Offers", inverse_name='property_id', comodel_name='estate.property.offer')
    total_area = fields.Integer(string="Total Area(sqm)", compute='_compute_total_area', readonly=True)
    best_price = fields.Float(string="Best Offer", compute='_compute_best_price', readonly=True)
    image = fields.Image(string="Property Image",
        max_width=1024,
        max_height=1024,
        help="Upload an image of the property.")
    company_id = fields.Many2one(string="Company",
        comodel_name='res.company',
        default=lambda self: self.env.user.company_id,
        required=True
    )

    _sql_constraints = [
        (
            'check_expected_price',
            'CHECK(expected_price > 0)',
            "Expected price must be strictly positive",
        ),
        (
            'check_selling_price',
            'CHECK(selling_price >= 0)',
            "Selling price must be non-negative",
        ),
    ]

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.garden_area + property.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.mapped('offer_ids.price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.write({
                    'garden_area': 10,
                    'garden_orientation':'north'
                })
            else:
                property.write({
                    'garden_area': 0,
                    'garden_orientation':''
                })

    def action_sold(self):
        self.ensure_one()
        if not any(self.offer_ids.filtered(lambda offer: offer.status == 'accepted')):
            raise UserError("You cannot sell a property with no accepted offers.")
        # Validation: Ensure buyer is set
        if not self.buyer_id:
            raise UserError("Please specify a buyer for the property.")
        # Validation: Ensure selling price is set and is a positive value
        if not self.selling_price or self.selling_price <= 0.0:
            raise UserError("Please specify a valid selling price greater than 0.")
        self.state = "sold"
        message = Markup(
            "The property has been marked as <b>Sold</b>.<br/>"
            "<b>Buyer:</b> %(buyer_name)s<br/>"
            "<b>Selling Price:</b> %(selling_price)s"
        ) % {
            "buyer_name": self.buyer_id.name or "N/A",
            "selling_price": self.selling_price or 0.0
        }
        self.message_post(
            body=message,
            message_type='comment',
        )

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'sold':
            raise UserError("Sold Property can't be cancelled")
        self.state='cancelled'

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property in self:
            if (
                not float_is_zero(property.selling_price, precision_digits=2)
                and float_compare(property.selling_price, property.expected_price * 0.9,
                precision_digits=2) == -1
            ):
                # If selling price is zero, don't apply constraint(at the creation of new property)
                raise ValidationError("Selling price must be at least 90% of the expected price!")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_neworcancelled(self):
        restricted_properties = self.filtered(lambda p: p.state not in ['new', 'cancelled']).mapped('name')
        if restricted_properties:
            raise UserError(f"You can only delete properties that are in 'New' or 'Cancelled' state.\nThe following properties cannot be deleted: {', '.join(restricted_properties)}")
