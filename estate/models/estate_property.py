from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

# A property cannot be sold below this ratio of its expected price.
MIN_SELLING_PRICE_RATIO = 0.9
# Values suggested when the garden option is enabled on a property.
DEFAULT_GARDEN_AREA = 10
DEFAULT_GARDEN_ORIENTATION = "north"
# States in which a property is closed: it is kept as history and cannot
# be modified anymore.
CLOSED_STATES = ("sold", "cancelled")
# Fields that can still be written on closed properties (archiving them).
CLOSED_WRITABLE_FIELDS = {"active"}


class EstateProperty(models.Model):
    """A property (house, apartment...) advertised by the real estate agency."""

    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    def _default_date_availability(self):
        """Properties are available three months after their creation by default."""
        return fields.Date.add(fields.Date.today(), months=3)

    # Description of the property
    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=_default_date_availability,
    )
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string="Garden Orientation",
    )

    # Prices: the selling price and the buyer are only set by accepting an
    # offer, hence read-only.
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)

    # Workflow
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string="Status",
        required=True,
        copy=False,
        # Computed from the offers, but still writable so that the action
        # buttons can set the sold and cancelled states. Precomputed because
        # the field is required and must be set before the record is inserted.
        compute="_compute_state",
        store=True,
        readonly=False,
        precompute=True,
    )

    # Relations
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Computed values
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive.',
    )

    @api.depends("offer_ids.status")
    def _compute_state(self):
        """Derive the state of open properties from their offers.

        Sold and cancelled are set by the action buttons and are never
        overwritten here, even when the offers change.
        """
        for record in self:
            if record.state in CLOSED_STATES:
                continue
            if "accepted" in record.offer_ids.mapped("status"):
                record.state = "offer_accepted"
            elif record.offer_ids:
                record.state = "offer_received"
            else:
                record.state = "new"

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            # default=0.0 avoids an error when the property has no offer.
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_ratio(self):
        """The selling price must reach a minimum ratio of the expected price."""
        for record in self:
            # The selling price is zero until an offer is accepted.
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_price = record.expected_price * MIN_SELLING_PRICE_RATIO
            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError(self.env._(
                    "The selling price cannot be lower than %(percent)d%% of the expected price.",
                    percent=MIN_SELLING_PRICE_RATIO * 100,
                ))

    @api.onchange("garden")
    def _onchange_garden(self):
        """Suggest garden values when the garden is enabled, clear them otherwise."""
        if self.garden:
            self.garden_area = DEFAULT_GARDEN_AREA
            self.garden_orientation = DEFAULT_GARDEN_ORIENTATION
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_or_cancelled(self):
        """Properties with offers in progress or sold are kept as history."""
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError(self.env._(
                    "Only new and cancelled properties can be deleted."
                ))

    def write(self, vals):
        """Prevent modifying sold or cancelled properties, except archiving them."""
        if set(vals) - CLOSED_WRITABLE_FIELDS and any(
            state in CLOSED_STATES for state in self.mapped("state")
        ):
            raise UserError(self.env._(
                "Sold or cancelled properties cannot be modified."
            ))
        return super().write(vals)

    def action_sold(self):
        """Mark the properties as sold.

        All the checks are done before writing, so that either all the
        properties are sold or none of them. Modules extending this method
        (e.g. estate_account) rely on these checks.
        """
        for record in self:
            if record.state == "sold":
                raise UserError(self.env._("This property is already sold."))
            if record.state == "cancelled":
                raise UserError(self.env._("Cancelled properties cannot be sold."))
            # The buyer is only set when an offer is accepted.
            if not record.buyer_id:
                raise UserError(self.env._(
                    "A property can only be sold once an offer has been accepted."
                ))
        self.write({"state": "sold"})
        return True

    def action_cancel(self):
        """Cancel the properties, unless they are already sold or cancelled."""
        for record in self:
            if record.state == "sold":
                raise UserError(self.env._("Sold properties cannot be cancelled."))
            if record.state == "cancelled":
                raise UserError(self.env._("This property is already cancelled."))
        self.write({"state": "cancelled"})
        return True
