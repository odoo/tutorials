from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price>0)', 'The expected price must be strictly positive!'),
        ('check_selling_price', 'CHECK(selling_price>=0)', 'The selling price must be positive!')
    ]

    name = fields.Char("Property Name", required=True, help="Property Name")
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), days=30))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area(sqm)")
    garden_orientation = fields.Selection(
        string = "Garden Orientation",
        selection = [
            ("north", "North"), 
            ("south", "South"), 
            ("east", "East"), 
            ("west", "West")
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        default="new", copy=False, string="State",
        selection = [
            ("new", "New"), 
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ]
    )
    property_type_id = fields.Many2one(string="Property Type", comodel_name="estate.property.type")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False )
    salesperson = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    total_area = fields.Float(compute="_compute_total")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0) 

    @api.onchange("garden")
    def _onchange_garden(self):
        if(self.garden):
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            min_price = record.expected_price * 0.9 
            if not fields.float_is_zero(record.selling_price, precision_digits=2) and fields.float_compare(record.selling_price, min_price, precision_rounding=2) < 0:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price!")
            
    def action_set_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(("Cancelled Property can't be Sold!"))
            record.state = "sold"
            
    def action_set_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError(("Sold Property can't be Cancelled!"))
            record.state = "cancelled"
            