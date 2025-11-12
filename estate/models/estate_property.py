from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Propery Model"
    _order = "id desc"
    _inherit = ["mail.thread"]
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "The selling price must be strictly positive",
        ),
    ]

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        default=(fields.Date.add(fields.Date.today(), months=3)),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    is_garage = fields.Boolean()
    is_garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("west", "West"),
            ("east", "East"),
        ],
    )
    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "cancelled"),
        ],
        default="new",
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner")
    seller_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id")
    total_area = fields.Float(compute="_compute_area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")
    image = fields.Image()

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        self.best_price = max(self.offer_ids.mapped("price")) if self.offer_ids else 0

    @api.onchange("is_garden")
    def _onchange_is_garden(self):
        if self.is_garden is True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.ondelete(at_uninstall=False)
    def _unlink_if_status_sold_or_new(self):
        if any(
            record.status in ["offer_received", "offer_accepted", "sold"]
            for record in self
        ):
            raise UserError("Only new or cancelled properties can be deleted")

    def action_sold(self):
        for record in self:
            if record.status == "cancelled":
                raise UserError("cancelled properties cannot be sold!")
            if record.offer_ids:
                for offer in record.offer_ids:
                    if offer.status == "accepted":
                        record.status = "sold"
            raise UserError(
                "You cannot sold properties which don't have any accepted offers"
            )

    def action_cancelled(self):
        for record in self:
            if record.status == "sold":
                raise UserError("Sold properties cannot be cancelled!")
            record.status = "cancelled"
