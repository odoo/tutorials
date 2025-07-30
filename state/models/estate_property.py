from dateutil.relativedelta import relativedelta
from odoo import api,fields, models
from odoo.exceptions import UserError

class StateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char('Title', required=True)
    postcode = fields.Char('Postcode')
    description = fields.Text('Description')
    date_availability = fields.Date(
        string='Available From',
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    best_price = fields.Float('Best Price', compute="_compute_best_price")
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', copy=False)
    total_area = fields.Integer('Total Area (sqm)', compute="_compute_total_area")
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garden_area = fields.Integer('Garden Area (sqm)')
    active = fields.Boolean('Active',default=True)
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    property_type_id = fields.Many2one('estate.property.type', 'Property Type', required=True)
    partner_id = fields.Many2one(
        'res.partner', string='Buyer', index=True,
        help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")
    user_id = fields.Many2one('res.users', string='Salesman', index=True, default=lambda self: self.env.user)
    tags_ids = fields.Many2many('estate.property.tags', string="Tags")
    offer_ids = fields.One2many('estate.property.offer','property_id', string="Offer")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north','North'),('south','South'),('east','East'),('west','West')],
        help="Select de garden orientation"
    )
    state = fields.Selection(
        selection=[('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')],
        string = "Status",
        required=True,
        copy=False,
        default='new',
        compute='_compute_state_based_on_offers',
        store=True
    )

    _sql_constraints = [
        ('check_expected_price_positive','CHECK(expected_price >= 0.0)','The expected price should be positive.'),
        ('chech_selling_price_positive','CHECK(selling_price >= 0.0)','The selling price should be positive'),
    ]

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.depends('offer_ids')
    def _compute_state_based_on_offers(self):
        for record in self:
            if record.state in ('offer_accepted', 'sold'):
                continue  # No cambiar el estado si ya está avanzado
            record.state = 'offer_received' if record.offer_ids else 'new'

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_cancelled(self):
        for record in self:
            if record.state not in ('new','cancelled'):
                raise UserError("You can only delete properties that are in 'new' or 'cancelled' state.")
    
    def cancelled_property(self):
        for record in self:
            if record.state not in ('sold','cancelled'):
                record.state = 'cancelled'
            else:
                raise UserError("Can't cancel a sold or already cancelled property")
        return True
    
    def sold_property(self):
        for record in self:
            if record.state not in ('cancelled', 'sold'):
                record.state = 'sold'
            else:
                raise UserError("You cannot sell a cancelled or already sold property.")
        return True