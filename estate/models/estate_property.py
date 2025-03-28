from dateutil.relativedelta import relativedelta

from odoo import _, api, exceptions, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_utils

class EstateProperty(models.Model):
    '''Estate property'''
    _name = "estate.property"
    _description = "Property of an estate"
    _order = "sequence, id desc"

    # ==================== Default Methods ====================

    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    # ==================== Fields ====================

    name = fields.Char(required = True, string="Title")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From",
        copy = False,
        default = lambda self: self._default_date_availability()
    )
    expected_price = fields.Float("Expected Price", required = True)
    selling_price = fields.Float("Selling Price", readonly = True, copy = False)
    bedrooms = fields.Integer("Bedrooms", default = 2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string = "Orientation",
        selection = [('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')]
    )
    active = fields.Boolean("Active", default = True)
    state = fields.Selection(
        string = "Status",
        selection = [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default = 'new',
        required = True,
        copy = False
    )
    property_type_id = fields.Many2one("estate.property.type", string = "Property Type")
    buyer_id = fields.Many2one("res.partner", copy = False, string = "Buyer")
    salesperson_id = fields.Many2one("res.users", default = lambda self: self.env.user, string = "Salesperson")
    tag_ids = fields.Many2many("estate.property.tag", string = "Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string = "Offers")
    total_area = fields.Float(compute = "_compute_area", string = "Total Area")
    best_price = fields.Float(compute = "_compute_best_price", string = "Best Offer")

    # ==================== Constaints  ====================

    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.')
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_expected_price(self):
        for property in self:
            if not float_utils.float_is_zero(property.selling_price, precision_rounding = 0.01):
                if self.selling_price < 0.9 * property.expected_price:
                    raise ValidationError("The selling price cannot be less than 90% of the expected price")

    # ==================== Compute Methods ====================

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area


    @api.depends("offer_ids")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'), default=0)

    # ==================== onChange Methods ====================

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else ''
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_offer_not_new_or_cancelled(self):
        for property in self:
            if property.state not in {'new', 'cancelled'}:
                raise ValidationError("You cannot delete a property that is not new or cancelled")

    # ==================== Actions Methods ====================

    def action_cancel_property(self):
        '''Cancel a property selling'''
        for property in self:
            if property.state == 'sold':
                raise exceptions.UserError(_("Sold property cannot be cancelled"))

            property.state = 'cancelled'

        return True

    def action_sell_property(self):
        '''Mark an estate property as sold'''
        for property in self:
            if property.state == 'cancelled':
                raise exceptions.UserError(_("Cancelled property cannot be sold"))

            property.state = 'sold'

        return True

    
