from odoo import api, exceptions, fields, models, tools
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "My Estate Property"

    name = fields.Char(required = True, string = "Name")
    postcode = fields.Char(string = "Postcode")
    date_availability = fields.Date(copy = False, default = fields.Date.today() + relativedelta(months = 3), string = "Available From")
    expected_price = fields.Float(required = True, string = "Expected Price")
    selling_price = fields.Float(readonly = True, copy = False, string = "Selling Price")
    bedrooms = fields.Integer(default = 2, string = "Bedrooms")
    living_area = fields.Integer(string = "Living Area")
    facades = fields.Integer(string = "Facades")
    garage = fields.Boolean(string = "Garage")
    garden = fields.Boolean(string = "Garden")
    garden_area = fields.Integer(string = "Garden Area")
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], string = "Garden Orientation")
    active = fields.Boolean(default = True, string = "Active")
    state = fields.Selection([('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
                             required = True, copy = False, default = 'new', string = "Status")
    description = fields.Char("Description.", default = "Description of a house.", readonly = True)

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesman = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', index=True, copy = False)

    tag_ids = fields.Many2many('estate.property.tag', string = 'Property Tags')
    offer = fields.One2many('estate.property.offer', 'property_id', string = 'Offers')

    total_area = fields.Float(compute = "_compute_area", string = "Total Area (sqm)")

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Integer(compute = "_compute_price", string = "Best Price")

    @api.depends("offer")
    def _compute_price(self):
        for record in self:
            # record.best_price = max(record.offer.mapped('price'))
            record.best_price = 0
            for item in record.offer:
                record.best_price = max(record.best_price, item.price)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = False
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if self.state == "cancelled":
                raise exceptions.UserError("Cancelled property cannot be sold.")
            self.state = "sold"

    def action_cancel(self):
        for record in self:
            if self.state == "sold":
                raise exceptions.UserError("Sold property cannot be cancelled.")
            self.state = "cancelled"

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "Expected price should be positive."),
        ("check_selling_price", "CHECK(selling_price > 0)", "Selling price should be positive."),
        ("check_offer_price", "CHECK(selling_price > 0)", "Selling price should be positive.")
    ]

    @api.constrains("expected_price", "sellling_price")
    def _check_selling_price(self):
        print("Entered the method.")
        for record in self:
            if 0 < record.selling_price < 0.9 * record.expected_price:
                raise exceptions.ValidationError("Less than 90% of expected price.")
    
 