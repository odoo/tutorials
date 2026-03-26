from odoo import fields, models, api, tools
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate properties"
    _order = 'id desc'

    active = fields.Boolean(default=True)
    state = fields.Selection([
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ], 
        default='new'
    )
    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, 
        default=lambda self: fields.Date.add(fields.Date.today(), months=3), string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
    )
    property_type_id = fields.Many2one('estate.property.type', 
                                       string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesman_id = fields.Many2one('res.users', string="Salesman", 
                                  default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Float(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price', 
                              string="Best Offer")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        "The expected price of a property must be strictly positive.",
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        "The selling price of a property must be positive.",
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('property_offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if len(record.property_offer_ids) > 0:
                record.best_price = max(record.property_offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.constrains('selling_price', 'expected_price')
    def _check_date_end(self):
        for record in self:
            if (len(record.property_offer_ids) != 0) and tools.float_utils.float_compare(record.expected_price * 0.9, record.selling_price, precision_digits=2) == 1:
                raise ValidationError("The selling price cannot be inferior to 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _check_state_before_unlink(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("Only new or cancelled properties can be deleted...")
            
    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            else:
                record.state = 'sold'
        return True

    def action_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            else:
                record.state = 'cancelled'
        return True

