from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(
        string="Property Name",
        required=True,
        help="Property Name"
    )
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Availability Date",
        copy=False,
        default=fields.Datetime.today() + relativedelta(days=90),
    )
    expected_price = fields.Float(
        "Expected Price",
        required=True,
        help="Expected Price"
    )
    selling_price = fields.Float(
        "Selling Price",
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(
        "Bedrooms", 
        default=2
    )
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        required=True,
        copy=False,
        default="new",
    )
    
    property_type_id=fields.Many2one(string="Property Type", comodel_name="estate.property.type")
    buyer=fields.Many2one(string="Buyer", comodel_name="res.partner", copy=False, readonly=True)
    salesperson=fields.Many2one(
        string="Salesperson",
        comodel_name="res.users",
        default=lambda self: self.env.user
    )

    tag_ids=fields.Many2many(string="Tags", comodel_name="estate.property.tag")
    offer_ids=fields.One2many(string="Offers", comodel_name="estate.property.offer", inverse_name="property_id")
    total_area=fields.Integer(compute="_compute_total_area")
    best_price=fields.Integer(compute="_compute_best_price", help="Best price from offers")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)
    
    @api.onchange("garden")
    def _onchange_garden_availability(self):
        if self.garden:
            self.garden_area=10
            self.garden_orientation="north"
        else:
            self.garden_area=0
            self.garden_orientation=""
    
    def action_mark_property_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold")
            elif record.state == "sold":
                raise UserError("Already sold property")
            else:
                record.state = "sold"
        return True
    
    def action_mark_property_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled")
            elif record.state == "cancelled":
                raise UserError("Already cancelled property")
            else:
                record.state = "cancelled"
        return True
