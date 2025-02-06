from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Property Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.datetime.today() + fields.date_utils.relativedelta(months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    fascades = fields.Integer(string="Fascades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    # define default value for it in future
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    # Following active field refer to the visiblity of field in search
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        "State",
        required=True,
        default="new",
    )
    # Relational Field for defining type of property (Many2one)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    # Relational Field for defining sales person and buyer for property
    property_buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_seller_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    # Relational Field for tag's (Many2Many)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    # Relation Field for offer (one2Many)
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    # computed field total area which is just some of two areas
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    # computation methods
    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.mapped("offer_ids.price"))

    @api.onchange("garden")
    def _change_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None
