# type: ignore
from datetime import timedelta
from odoo import api, exceptions, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Description"
    _inherit = 'mail.thread'
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price must be positive.'),
    ]

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description of Property")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", default=lambda self: fields.date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Float(string="Total Area", compute="_compute_total_area")
    garden_orientation = fields.Selection(string="Garden Orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ])
    status = fields.Selection(string="Status",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True,
        default="new",
        copy=False,
        tracking=True
    )
    active = fields.Boolean(string="Active", default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user, tracking=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers", tracking=True)
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    property_image = fields.Binary()

    # Compute Total Area
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # Compute
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        """Set default values when garden is enabled/disabled"""
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def write(self, vals):
        """Ensure values are reset when garden is unchecked in backend operations."""
        if 'garden' in vals and not vals['garden']:
            vals.update({'garden_area': 0, 'garden_orientation': False})
        return super().write(vals)

    def action_set_sold(self):
        if self.status == "cancelled":
            raise UserError("A cancelled property cannot be sold!")

        accepted_offer = self.offer_ids.filtered(lambda o: o.status == 'accepted')
        if not accepted_offer:
            raise UserError("Cannot sell a property without an accepted offer")
        self.status = "sold"

    def action_set_cancelled(self):
        if self.status == "sold":
            raise UserError("A sold property cannot be cancelled!")
        self.status = "cancelled"

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                min_acceptable_price = record.expected_price * 0.9
                if float_compare(record.selling_price, min_acceptable_price, precision_digits=2) == -1:
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _check_state_on_delete(self):
        for property in self:
            if property.status not in ['new', 'cancelled']:
                raise exceptions.UserError("You can only delete properties that are in 'New' or 'Canceled' state.")
