from dateutil.relativedelta import relativedelta
from odoo import api, models, fields
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
       
     ]

    # === Fields ===
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        default='new',
        copy=False
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    company_id = fields.Many2one(
    'res.company',
    string='Agency',
    required=True,
    default=lambda self: self.env.company
)
    total_area = fields.Float(compute="_compute_total_area", string="Total Area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "Expected price must be strictly positive."),
        ("check_selling_price", "CHECK(selling_price >= 0)", "Selling price must be positive."),
        ("unique_name", "UNIQUE(name)", "Property name must be unique."),
    ]

    # === Compute Methods ===
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped("price")) if prop.offer_ids else 0.0

    # === Onchange Methods ===
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "North"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # === Constraints ===
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for prop in self:
            if not float_is_zero(prop.selling_price, precision_digits=2):
                min_price = 0.9 * prop.expected_price
                if float_compare(prop.selling_price, min_price, precision_digits=2) < 0:
                    raise ValidationError(
                        f"Selling price ({prop.selling_price}) cannot be lower than 90% of "
                        f"the expected price ({prop.expected_price}). Minimum allowed: {min_price}"
                    )

    # === Business Logic ===
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            record.state = 'cancelled'
        return True

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
                    # ✅ Check for accepted offer
            if not any(offer.status == 'accepted' for offer in record.offer_ids):
                raise UserError("Cannot sell a property without an accepted offer.")
            
            if record.state == 'sold':
               raise UserError("Property is already sold.")
            
            record.state = 'sold'
        return True

    # === Deletion Rule ===
    @api.ondelete(at_uninstall=False)
    def _check_state_before_deletion(self):
        for prop in self:
            if prop.state not in ['new', 'cancelled']:
                raise UserError("Cannot delete properties not in 'New' or 'Cancelled' state!")
