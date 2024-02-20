from odoo import fields, models, api


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Application"

    name = fields.Char(string="Title", required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        copy=False,
        required=True,
        default="new",
        string="State",
        selection=[
            ("new", "New"),
            ("offer_recieved", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
    )
    total_living_area = fields.Integer(compute="_calculate_total_area")
    best_price = fields.Float(compute="_get_max_offer")

    @api.depends("living_area","garden_area")
    def _calculate_total_area(self):
        for record in self:
            record.total_living_area=record.living_area+record.garden_area

    @api.depends("offer_ids.price")
    def _get_max_offer(self):
        for record in self:
            record.best_price=max(record.offer_ids.mapped("price")) if record.offer_ids else 0
    
    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10  if self.garden else 0
        self.garden_orientation = "north"  if self.garden else None

    
