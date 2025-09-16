from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "ESTATE Property"
    _order = "id desc"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True, default=1.0)
    selling_price = fields.Float('Selling Price', copy=False)
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        help="Choose the garden orientation",
    )
    estate_state = fields.Selection(
        string='Status',
        default='new',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        help="Choose the estate state",
    )
    total_area = fields.Integer('Total Area (sqm)', compute="_compute_total_area")  # Computed Field
    best_offer = fields.Float('Best Offer', compute="_compute_best_offer")  # Computed Field

    # Foreign_Key (Property Type)
    type_id = fields.Many2one(comodel_name="estate.property.type",
                                string="Property Type",
                                ondelete="set null")
    # Foreign_Key (Odoo User Salesperson)
    salesperson_id = fields.Many2one("res.users",
                                        string="Salesperson",
                                        index=True,
                                        default=lambda self: self.env.user)
    # Foreign_Key (Partner Contact)
    partner_id = fields.Many2one("res.partner",
                                    string="Partner",
                                    copy=False)
    # Many2Many (Property Tags)
    tag_ids = fields.Many2many(comodel_name="estate.property.tag", string="Property Tags")
    # One2Many (List of Offers for a Property)
    offer_ids = fields.One2many(comodel_name="estate.property.offer",
                                    inverse_name="property_id",
                                    string="Property Offers")

    # Computed Fields Methods
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = property.offer_ids and max(property.offer_ids.mapped('price')) or 0.0

    # SQL constraints
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'A property expected price must be strictly positive',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)',
        'A property selling price must be strictly positive',
    )

    # Python constraints
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for property in self:
            if float_is_zero(property.selling_price, precision_digits=2):
                continue
            if float_compare(property.selling_price, property.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price!")

    # Onchange Methods
    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else False

    # CRUD Method (on_delete a Property)
    @api.ondelete(at_uninstall=False)
    def _check_deletion(self):
        for property in self:
            if property.estate_state not in ['new', 'cancelled']:
                raise UserError("Only properties in 'New' or 'Cancelled' state can be deleted.")

    # Action Methods
    def action_sold(self):
        for property in self:
            if property.estate_state in ['cancelled']:
                raise UserError("Cancelled properties cannot be sold!")
            property.estate_state = 'sold'
        return True  # to avoid warning in logs as it's a public method

    def action_cancel(self):
        for property in self:
            if property.estate_state in ['sold']:
                raise UserError("Sold properties cannot be cancelled!")
            property.estate_state = 'cancelled'
        return True  # to avoid warning in logs as it's a public method
