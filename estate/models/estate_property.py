from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _inherit = ['mail.thread', 'website.published.mixin']
    _order = 'id desc'

    name = fields.Char(string="Name", required=True, help="Name of the Property", tracking=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Datetime.today() + timedelta(days=90),
    )
    expected_price = fields.Float(string="Expected Price", required=True, tracking=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area(sqm)")
    total_area = fields.Float(compute="_compute_total_area", string="Total Area(sqm)")
    best_price = fields.Float(compute="_compute_best_price")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    active = fields.Boolean(string="Active", default=True)
    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
        readonly=True,
        tracking=True
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, readonly=True)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Property Offer")
    company_id = fields.Many2one("res.company", required=True,default=lambda self: self.env.company, string="Agency")
    image = fields.Image(store=True, verify_resolution=True)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_property_sold(self):
        for record in self:
            if record.status == "cancelled":
                raise UserError(_("A cancelled property cannot be sold!"))

            accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            if not accepted_offer:
                raise UserError(_("You need to accept an offer first!"))

            record.status = 'sold'
        return True

    def action_property_cancel(self):
        for record in self:
            if record.status == 'sold':
                raise UserError(_("A sold property cannot be cancelled!"))
            record.status = 'cancelled'
        return True

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_acceptable_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_acceptable_price, precision_digits=2) == -1:
                raise ValidationError(_("The selling price cannot be lower than 90% of the expected price!"))

    @api.ondelete(at_uninstall=False)
    def _check_state_on_delete(self):
        for record in self:
            if record.status not in ['sold', 'cancelled']:
                raise UserError(_("Only properties with 'New' or 'Cancelled' status can be deleted."))

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        if not self.env.user.has_group('estate.estate_group_manager'):
            if 'salesperson_id' in res:
                res['salesperson_id']['readonly'] = True
        return res
