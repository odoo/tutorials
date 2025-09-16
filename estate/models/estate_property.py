from datetime import timedelta
from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Property'
    _order = 'name'

    name = fields.Char("Property", required=True)
    description = fields.Text("Description")

    active = fields.Boolean(string="Active", default=True, required=True)
    state = fields.Selection(
        string="State",
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
    selling_price = fields.Float(
        string="Selling Price",
    )

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
