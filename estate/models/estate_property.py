from datetime import timedelta

from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date availability", copy=False, default=fields.Date.today() + timedelta(days=+90))
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West')
    ], string = "Garden Orientation", help = "It is used to define the garden orientation")
    state = fields.Selection([
        ('new', 'New'),
        ('offerreceived', 'Offer Received'),
        ('offeraccepted', 'Offer Accepted'), 
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], string="State", default = "new")
    active = fields.Boolean("Active", default=True)
    seller_id = fields.Many2one(comodel_name="res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type")
    tag_ids = fields.Many2many(comodel_name="estate.property.tag", string="Tags")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id")
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")
    best_offer = fields.Integer(string="Best Offer", compute="_compute_best_offer")

    # === COMPUTE METHODS === #
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in (self):
            record.best_offer = max(record.offer_ids.mapped('price'), default=0)
    
    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # === Actions === #
    def action_sold(self):
        for record in self:
            if record.state== "cancelled":
                raise UserError("Cancelled properties cannot be sold")
            else:
                record.state = "sold"
    def action_cancelled(self):
        for record in self:
            if record.state== "sold":
                raise UserError("sold properties cannot be cancelled")
            else:
                record.state = "cancelled"
    
    # === SQL Constraints === #
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "Expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price > 0)", "Selling price must be strictly positive")  
    ]

    # === Python Constraints === #
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        if self.selling_price > 0 and self.selling_price < self.expected_price * 0.9:
            raise ValidationError("Selling price cannot be lower than 90% of the expected price.")
