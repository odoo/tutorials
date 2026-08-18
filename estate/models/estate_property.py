from dateutil.relativedelta import relativedelta

from odoo import fields, models, api

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Management"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From", 
        default=lambda _ : fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        string="Type of State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        default="new",
        copy=False
    )
    property_type_id = fields.Many2one(
        string="Property Type",
        comodel_name="estate.property.type"
    )
    partner_id = fields.Many2one(
        string="Buyer",
        comodel_name="res.partner",
        copy=False
    )
    user_id = fields.Many2one(
        string="Salesman",
        comodel_name="res.users",
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many(
        string="Property Tags",
        comodel_name="estate.property.tag"
    )
    offer_ids = fields.One2many(
        string="Offers",
        comodel_name="estate.property.offer",
        inverse_name="property_id"
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
        readonly=True
    )
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
        readonly=True
    )
    active = fields.Boolean(default=True)

    # Methods
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False
