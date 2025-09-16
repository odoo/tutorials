from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Property'
    _order = 'name'

    name = fields.Char("Property", required=True)
    description = fields.Text("Description")

    active = fields.Boolean(string="Active", default=True, required=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )

    date_availability = fields.Date(
        string="Available From",
        default=(lambda _: fields.Date.today() + timedelta(days=90)),
        copy=False,
    )

    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        string='Property Type',
    )

    tag_ids = fields.Many2many(
        comodel_name='estate.property.tag',
        string='Tags',
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
    )

    buyer_id = fields.Many2one(
        comodel_name='res.partner',
        string="Buyer",
        copy=False,
    )

    seller_id = fields.Many2one(
        comodel_name='res.users',
        string="Seller",
        default=lambda self: self.env.user,
    )

    # Price fields:
    expected_price = fields.Float(
        string="Expected Price",
        required=True,
    )
    _check_expected_price = models.Constraint(
        'CHECK(expected_price IS NULL OR expected_price > 0)',
        "Expected price must be positive.",
    )

    selling_price = fields.Float(
        string="Selling Price",
    )

    _check_selling_price_nonnegative = models.Constraint(
        'CHECK(selling_price IS NULL OR selling_price >= 0)',
        "Selling price cannot be negative.",
    )
    
    @api.constrains('selling_price')
    def _check_selling_price_not_too_low(self):
        for record in self:
            if (
                record.selling_price
                and not float_is_zero(record.selling_price, 2)
                and float_compare(record.selling_price, 0.9 * record.expected_price, 2) < 0
            ):
                raise ValidationError("Property selling price cannot be lower than 90% of the expected price.")


    best_price = fields.Float(
        string="Best Offer",
        compute='_compute_best_price',
    )

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max((offer.price for offer in record.offer_ids), default=None)

    # Address fields:
    postcode = fields.Char("Postcode")

    # Amenity fields:
    bedrooms = fields.Integer(string="Bedrooms", default=2, help="Number of bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)", help="Habitable area of the property (m^2)")
    facades = fields.Integer(string="Facades", help="Number of facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)", help="Size of the garden (m^2)")
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[
            ('n', 'North'),
            ('s', 'South'),
            ('e', 'East'),
            ('w', 'West'),
        ],
        help="Direction the garden faces",
    )

    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            if record.living_area is None or record.garden_area is None:
                record.total_area = None
            else:
                record.total_area = record.living_area + record.garden_area


    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'n'
        else:
            self.garden_area = 0
            self.garden_orientation = None


    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Can't cancel a property that's already sold")
            else:
                record.state = 'cancelled'
        return True


    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Can't sell a cancelled property")
            else:
                record.state = 'sold'
        return True
