from odoo import models, fields ,api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Storing Properties of Real Estate"

    name = fields.Char(string="name", required=True)
    description = fields.Text(string="description")
    postcode = fields.Char("postcode")
    date_availability = fields.Date(
        string="date availability",
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False,
    )
    expected_price = fields.Float(string="expected price", required=True)
    selling_price = fields.Float(
        string="selling price", readonly=True, copy=False
    )
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [("North", "north"), ("South", "south"), ("East", "east"), ("West", "west")]
    )

    property_type_id = fields.Many2one("estate_property_type")
    property_tag_ids = fields.Many2many("estate_property_tag")
    salesman_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    offer_property_ids = fields.One2many("estate_property_offer", "property_id")
    total_area = fields.Float("Total Area(sqm)", compute="_compute_total_area")
    best_price = fields.Float("Best Price", compute="_compute_best_price")

    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("New", "new"),
            ("Offer Received", "Offer Received"),
            ("Offer Accepted", "Offer Accepted"),
            ("Sold", "sold"),
            ("Cancelled", "cancelled"),
        ],
        default="New",
        copy=False,
    )

    _expected_price_positive_check=models.Constraint('CHECK(expected_price>0)',"The expected price must be strictly positive")
    _selling_price_positive_check=models.Constraint('CHECK(selling_price>=0)',"The selling price must be positive")


    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        self.total_area =self.garden_area +self.living_area


    @api.depends("offer_property_ids")
    def _compute_best_price(self):
            self.best_price = max(
                self.offer_property_ids.mapped("price"), default=0.0
            )


    @api.onchange("garden")
    def _onchange_gaden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "North"
        else:
            self.garden_area = 10
            self.garden_orientation = False


    def action_set_sold(self):
        if (self.state=='Cancelled'):
            raise UserError(message="The cancelled property cant be sold")
        self.state="Sold"
        return True
    

    def action_set_cancelled(self):
        if(self.state=="Sold"):
             raise UserError(message="sold property can not be cancelled")
        self.state="Cancelled"
        return True
