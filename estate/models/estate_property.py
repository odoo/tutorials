from odoo import models, fields, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "name"

    name = fields.Char(required=True, default="Unknown")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    description = fields.Text()
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
    salesman_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user.id
    )
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", default=lambda self: self.env.user.id, copy=False
    )
    postcode = fields.Char()
    date_availability = fields.Date(copy=False)
    expected_price = fields.Float(required=True, default=15.6)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
        readonly=True,
    )
    offer_ids = fields.One2many(
        "estate.property.offers", "property_id", string="Offers"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for realEstateProperty in self:
            realEstateProperty.total_area = (
                realEstateProperty.living_area + realEstateProperty.garden_area
            )

    # @api.onchange("living_area", "garden_area")
    # def _compute_total_area(self):
    #     for record in self:
    #         record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        self.best_price = max(self.offer_ids.mapped("price")) if self.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def set_sold(self):
        if self.state == "cancelled":
            raise UserError("Cancelled Properties Cannot be Sold")
        else:
            self.state = "sold"
        return True

    def set_cancel(self):
        if self.state == "sold":
            raise UserError("Sold Properties cannot be Cancelled")
        else:
            self.state = "cancelled"
        return True
