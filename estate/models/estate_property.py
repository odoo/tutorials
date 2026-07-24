from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate properties"

    title = fields.Char(required=True, default="Unknown")
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    description = fields.Text()
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From",
        default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    active = fields.Boolean(default=True)
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East')],
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.types", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)
    tags_id = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(
        "Total Area (sqm)",
        compute="_compute_total_area",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
