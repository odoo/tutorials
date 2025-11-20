from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "sequence"

    # Default fields
    name = fields.Char("Title", required=True)
    sequence = fields.Integer("Sequence", default=10)

    # Basic fields
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From",
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Number of Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean("Active", default=True)
    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        default="new",
        required=True,
        copy=False,
    )
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Partner", copy=False)

    # Relational fields
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Computed fields
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area", store=True)

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_offer = max(prices) if prices else 0.0

    best_offer = fields.Float("Best Offer", compute="_compute_best_offer", store=True)

    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            if not self.garden_area:
                self.garden_area = 10
            if not self.garden_orientation:
                self.garden_orientation = "north"
