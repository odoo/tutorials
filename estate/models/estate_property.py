from dateutil.relativedelta import relativedelta
from odoo import fields, api, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _sql_constraints = [
        ("expected_price_positive", "CHECK(expected_price >= 0)", "A property expected price must be strictly positive"),
        ("selling_price_positive", "CHECK(selling_price >= 0)", "A property selling price must be positive"),
    ]
    _order = 'id desc'
    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string = 'Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], required=True, copy=False, default='new')
    property_type_id = fields.Many2one("estate.property.type")
    sales_person = fields.Many2one("res.users", string = "Salesman", default = lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string = "Buyer", copy=False)
    tags = fields.Many2many("estate.property.tag", string = "Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(string = "Total area", compute="_compute_total_area", store = True)
    best_price = fields.Float(string = "Best Offer", compute= "_compute_best_offer", store = True)

    @api.constrains('selling_price')
    def _check_price(self):
        for record in self:
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                raise UserError("The selling price must be at least 90% of the expected price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self: 
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)
    
    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if not record.garden:
                record.garden_area = 0.0
    
    def action_set_canceled(self):
        for record in self:
            current_state = self.browse(record.id).state
            if current_state == 'sold':
                raise UserError("A sold property cannot be canceled, create a new property instead.")
            elif current_state == 'canceled':
                raise UserError("Cannot cancel a canceled property.")
            record.state = 'canceled'
        return True
    
    def action_set_sold(self):
        for record in self:
            current_state = self.browse(record.id).state
            if current_state == 'canceled':
                raise UserError("Cannot sell a canceled property.")
            elif current_state == 'sold':
                raise UserError("Cannot sell an already sold property.")
            record.state = 'sold'
        return True

    @api.ondelete(at_uninstall=True)
    def _ondelete(self):
        for record in self:
            if record.state in {'new', 'cancelled'}:
                raise ValidationError("New or Cancelled property cannot be deleted")
