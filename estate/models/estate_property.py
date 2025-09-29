from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Properties"
    _order = 'id desc'
    _check_company_auto = True

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    property_type_id = fields.Many2one('estate.property.type')
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([
        ('north', "North"),
        ('south', "South"),
        ('east', "East"),
        ('west', "West")
    ])
    state = fields.Selection([
        ('new', "New"),
        ('offer_received', "Offer Received"),
        ('offer_accepted', "Offer Accepted"),
        ('sold', "Sold"),
        ('cancelled', "Cancelled"),
    ], required=True, default='new', copy=False)
    company_id = fields.Many2one(
        'res.company',
        required=True,
        default=lambda self: self.env.company,
    )
    tag_ids = fields.Many2many('estate.property.tag')
    salesman_id = fields.Many2one('res.users', check_company=True)
    buyer_id = fields.Many2one('res.partner', copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(compute="_compute_total_area", store=True)
    best_offer = fields.Float(compute="_compute_best_price", store=True)

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        "The expected amout should be strictly positive"
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)',
        "The selling amout should be strictly positive"
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_price_difference(self):
        for record in self:
            minimum_acceptable_price = record.expected_price * 0.9
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, minimum_acceptable_price, precision_digits=2) < 0:
                raise ValidationError("The selling price must be at least 90% of the expected price.")
        return True

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0)
    
    @api.ondelete(at_uninstall=False)
    def _unlink_only_new_and_canceled(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError(_("Only properties in 'New' or 'Cancelled' state can be deleted."))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_("Cancelled properties cannot be sold."))

            if not record.offer_ids.filtered(lambda offer: offer.status == 'accepted'):
                raise UserError(_("A property can only be sold if an offer has been accepted."))

            record.state = 'sold'
        return True

    def action_set_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("Sold properties cannot be cancelled."))
            record.state = 'cancelled'
        return True
