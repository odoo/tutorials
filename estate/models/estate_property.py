from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Management"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From", 
        default=lambda _ : fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        default="new",
        copy=False
    )
    property_type_id = fields.Many2one(
        string="Property Type",
        comodel_name="estate.property.type"
    )
    partner_id = fields.Many2one(
        string="Buyer",
        comodel_name="res.partner",
        copy=False,
        readonly=True
    )
    user_id = fields.Many2one(
        string="Salesman",
        comodel_name="res.users",
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many(
        string="Property Tags",
        comodel_name="estate.property.tag"
    )
    offer_ids = fields.One2many(
        string="Offers",
        comodel_name="estate.property.offer",
        inverse_name="property_id"
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
        readonly=True
    )
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
        readonly=True
    )
    active = fields.Boolean(default=True)

    _check_positive_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected price must be a positive amount.'
    )
    _check_positive_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price must be a positive amount.'
    )

    # Methods
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.onchange("offer_ids")
    def _onchange_offer_received_state(self):
        if self.offer_ids:
            self.state = "offer_received"
        else:
            self.state = "new"

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_new_or_cancelled(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError("Only new or cancelled properties can be deleted.")

    def action_sold(self):
        self.ensure_one()

        if self.state == "cancelled":
            raise UserError("Cancelled properties cannot be sold.")
        
        self.state = "sold"

    def action_cancel(self):
        self.ensure_one()

        if self.state == "sold":
            raise UserError("Sold properties cannot be cancelled.")
        
        self.state = "cancelled"
