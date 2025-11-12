# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property Plans"
    _order = 'id desc'
    _sql_constraints = [
        ('check_expected_price', "CHECK(expected_price > 0)", "expected price must be strictly positive."),
        ('check_selling_price', "CHECK(selling_price >= 0)", "selling price must be positive.")
    ]

    name = fields.Char(string="Title")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date Availability", copy=False, default=lambda self:fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([
        ('north', "North"),
        ('south', "South"),
        ('east', "East"),
        ('west', "West")
    ], string="Garden Orientation")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection([
        ('new_offer', "New"),
        ('offer_received', "Offer Received"),
        ('offer_accepted', "Offer Accepted"),
        ('sold_offer', "Sold"),
        ('cancel_offer', "Cancelled"),
    ],
    help="New: A new property with no offers\n\
        Offer Received: Offer to receive\n\
        Offer Accepted: Offer to accept\n\
        Sold: Property to sold\n\
        Cancelled: Property to cancel",
    string="Status", required=True, default='new_offer', copy=False)
    property_image = fields.Image(string="Property Image", max_width=1024, max_height=1024, store=True)
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string="Property Type")
    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self: self.env.company, string="Company")
    buyer_id = fields.Many2one(comodel_name='res.partner', string="Buyer", copy=False)
    saleperson_id = fields.Many2one(comodel_name='res.users', string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string="Property Tag")
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', string="Offers")
    total_area = fields.Integer(compute='_compute_total', string="Total Area (sqm)")
    best_price = fields.Float(string="Best Offer", compute='_compute_best_price', store=True)

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property in self:
            if not float_is_zero(property.selling_price, precision_rounding=0.01):
                if property.selling_price < property.expected_price * 0.9:
                    raise ValidationError(_('The selling price cannot be lower than 90% of the expected price.'))

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price')) if property.offer_ids else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else False

    @api.ondelete(at_uninstall=False)
    def _restrict_property_unlink(self):
        if any(property.state not in ('new_offer', 'cancel_offer') for property in self):
                raise UserError(_('You can only delete properties in "New" or "Cancelled" state.'))

    def action_sold(self):
        if 'cancelled' in self.mapped('state'):
            raise UserError("Cancelled property cannot be sold")
        if any(not property.buyer_id or not property.selling_price or property.state != "offer_accepted" for property in self):
            raise UserError("Property must have an accepted offer before being sold")
        self.write({'state': 'sold_offer'})
        return True

    def action_cancel(self):
        if 'sold_offer' in self.mapped('state'):
            raise UserError(_("Sold property can't be cancelled!"))
        self.write({'cancel_offer'})
        return True
