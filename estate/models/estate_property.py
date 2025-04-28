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
    garden_area = fields.Integer(string="Garden Area (sqm)", default=10)
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
    tag_ids = fields.Many2many("estate.property.tag", string = "Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(string = "Total area", compute="_compute_total_area", store = True)
    best_price = fields.Float(string = "Best Offer", compute= "_compute_best_offer", store = True)

    @api.constrains('selling_price', 'expected_price')
    def _check_price(self):
        for property in self:
            if float_compare(property.selling_price, property.expected_price * 0.9, precision_digits=2) == -1:
                raise UserError(_("The selling price must be at least 90% of the expected price"))

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self: 
            property.total_area = property.living_area + property.garden_area
    
    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'), default=0.0)
    
    @api.onchange('garden')
    def _onchange_garden(self):
        for property in self:
            if not property.garden:
                property.garden_area = 10

    def action_set_canceled(self):
        for property in self:
            if property.state == 'sold':
                raise UserError(_("A sold property cannot be canceled, create a new property instead."))
            elif property.state == 'canceled':
                raise UserError(_("Cannot cancel a canceled property."))
            property.state = 'canceled'
        return True
    
    def action_set_sold(self):
        
        for property in self:
            if property.state == 'canceled':
                raise UserError(_("Cannot sell a canceled property."))
            elif property.state == 'sold':
                raise UserError(_("Cannot sell an already sold property."))
            property.state = 'sold'
        return True

    @api.ondelete(at_uninstall = False)
    def _ondelete(self):
        for property in self:
            if property.state not in {'new', 'deleted'}:
                raise ValidationError(_("Cannot delete property which is not new or deleted"))

