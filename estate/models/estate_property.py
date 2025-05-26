from datetime import datetime, timedelta
from odoo import api, fields, models, exceptions, tools


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property's properties"
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK (expected_price > 0)', "The expected price must be greater than 0"),
        ('check_selling_price', 'CHECK (selling_price >= 0)', "The selling price must be greater or equal to 0"),
    ]

    name = fields.Char('Property name', required=True, default='Unknown')
    description = fields.Text('Property Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability', copy=False,
                                    default=lambda self: datetime.now() + timedelta(days=90))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection([('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')],
                                          default='north')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([
        ('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], default='new', required=True, copy=False)

    total_area = fields.Float('Total Area', compute='_compute_total_area')
    best_price = fields.Float('Best Offer', compute='_compute_best_price')
    is_state_set = fields.Boolean('Is State Set', compute='_compute_is_state_set')

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            best_offer = record.get_best_offer()
            if best_offer is None:
                record.best_price = 0
                continue
            record.best_price = best_offer.price

    def get_best_offer(self):
        if len(self.offer_ids) == 0:
            return None
        return self.offer_ids.sorted(lambda offer: offer.price)[-1]

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_orientation = 'North'
                record.garden_area = 10
            else:
                record.garden_orientation = None
                record.garden_area = 0

    def action_sold(self):
        valid_records = self.filtered(lambda r: r.state != 'cancelled')
        if not valid_records:
            raise exceptions.UserError(self.env._("Can't sell a cancelled offer"))
        for record in valid_records:
            best_offer = record.get_best_offer()
            if best_offer is None:
                raise exceptions.UserError(self.env._("The offers for property %s are empty", record.name))
            record.mark_as_sold(best_offer)

    def mark_as_sold(self, offer):
        offer.status = 'accepted'
        self.state = 'sold'
        self.buyer_id = offer.partner_id
        self.selling_price = offer.price

    def action_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError(self.env._("Can't cancel a sold offer"))
            record.state = 'cancelled'

    @api.constrains('selling_price', 'expected_price')
    def _check_prices(self):
        for record in self:
            if not tools.float_is_zero(record.selling_price, 3) and record.selling_price < record.expected_price * 0.9:
                raise exceptions.ValidationError(
                    self.env._("The selling price cannot be lower than 90%% of the expected price (min %d€)",
                               record.expected_price * 0.9))

    @api.depends('state')
    def _compute_is_state_set(self):
        for record in self:
            record.is_state_set = record.state == 'cancelled' or record.state == 'sold'

    @api.ondelete(at_uninstall=False)
    def _on_delete(self):
        for record in self:
            if not (record.state in ('cancelled', 'new')):
                raise exceptions.UserError(self.env._("Can only delete a 'New' or 'Cancelled' property (this property is '%s').", record.state))
