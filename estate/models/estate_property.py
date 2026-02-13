from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True, string="Title")
    description = fields.Text(string="Description")
    postcode = fields.Char(required=True)
    available_from = fields.Date(
        string="Availble From",
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer(default=0)
    living_area = fields.Integer(required=True)
    garage = fields.Boolean(required=True)
    garden = fields.Boolean(required=True)
    garden_area = fields.Integer(required=True)
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        required=True,
    )
    description = fields.Text()
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        copy=False,
    )
    total_area = fields.Float(compute="_compute_total_area")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    user_id = fields.Many2one(
        "res.users", string="SalesPerson", default=lambda self: self.env.user
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="offers",
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
