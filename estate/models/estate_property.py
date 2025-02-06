from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError 
from odoo import fields, models, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, default=None)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type", default=None
    )
    property_tag_id = fields.Many2many("estate.property.tags", string="Property Tags")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )
    date_availability = fields.Date(
        string="Availability Date",
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True, default=0.0)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Float(string="Living Area (sq.m.)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Float(string="Garden Area (sq.m.)")
    total_area = fields.Float("Total Area", compute="_compute_total_area")
    state = fields.Selection([("not sold", "Not Sold"), ("sold", "Sold"), ("cancelled", "Cancelled")], string="State")
    best_price = fields.Float(
        "Best Buyer Price", compute="_compute_best_price", store=True
    )
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden Orientation",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        self.total_area = self.living_area + self.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            record.state = 'cancelled'
        return True

    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            record.state = 'sold'
        return True

    # SQL constraint to ensure that expected price is greater than 0
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be positive'),('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]
