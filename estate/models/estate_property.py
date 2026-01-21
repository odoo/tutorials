from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Char(string="Property Description")
    postcode = fields.Char(string="Postal Code")
    date_availability = fields.Date(
        string="Available From",
        default=fields.Date.add(value=fields.Date.today(), months=3),
        copy=False,
    )
    expected_price = fields.Float(string="Expected Selling Price", required=True)
    selling_price = fields.Float(
        string="Actual Selling Price", readonly=True, copy=False,
    )
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Float(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Float(string="Garden Area (sqm)", compute="_automate_garden")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        compute="_automate_garden",
    )
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_area")
    active = fields.Boolean(string="Active", default=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    property_offers_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("property_offers_ids.price")
    def _compute_best_offer(self):
        for record in self:
            # for offer in record.property_offers_ids:
            #     best_offer= max(offer.price, best_offer)
            record.best_offer = max(record.mapped("property_offers_ids.price"), default=0)

    @api.onchange("garden")
    def _automate_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None
