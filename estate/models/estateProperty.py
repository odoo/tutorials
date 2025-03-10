from odoo import models, fields, api # type: ignore
from odoo.exceptions import UserError # type: ignore
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero # type: ignore

class EstateProperty(models.Model):
    _name = 'estate.property'  # Database table name
    _description = 'Real Estate Property'

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From" , copy=False , default=datetime.today() + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default="2")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )

    state = fields.Selection(
        [('new' , "New"), ('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'), ('sold','Sold'), ('cancelled','Cancelled')],
        string="State" ,
        default="new",
        copy=False,
        required=True,
    )
    

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    buyer_id = fields.Many2one(
        "res.partner", 
        string="Buyer", 
        copy=False
    )
    salesperson_id = fields.Many2one(
        "res.users", 
        string="Salesperson", 
        default=lambda self: self.env.user
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store=True)

    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area", store=True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0.0) + (record.garden_area or 0.0)


    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    # action for property sold button
    def action_do_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A canceled property cannot be sold!")
            acceptOffer = False
            for offer in record.offer_ids:
                if offer.status == "accepted":
                    acceptOffer = True
                    break
            if not acceptOffer:
                raise UserError("Accept any offer before sold!")
            record.state = "sold"
        return True
    
    # action for property cancelled button
    def action_do_cencelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be canceled!")
            record.state = "cancelled"
        return True

    # property constraits
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive."),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The selling price must be positive.")
    ]

    # define constrains for selling price not less than 90% of expected price
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            # Ignore validation if selling_price is 0 (no offer validated yet)
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            # Compare selling_price with 90% of expected_price
            min_acceptable_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_acceptable_price, precision_digits=2) == -1:
                raise models.ValidationError(
                    "The selling price cannot be lower than 90% of the expected price!"
                )