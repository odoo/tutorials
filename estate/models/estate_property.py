from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import _, float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float(string="Living Area (sq. m)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float(string="Garden Area (sq. m)")
    total_area = fields.Float(string="Total Area (sq. m)", compute="_computed_total_area", store=True)
    garden_orientation = fields.Selection([
        ('north', "North"),
        ('east', "East"),
        ('west', "West"),
        ('south', "South")
    ])
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection([
        ('new', "New"),
        ('offer_received', "Offer Received"),
        ('offer_accepted', "Offer Accepted"),
        ('sold', "Sold"),
        ('cancelled', "Cancelled")
    ], copy=False, default='new')
    property_type_id = fields.Many2one('estate.property.type', string="Property Type", ondelete="cascade")
    sales_person_id = fields.Many2one('res.users', string='Sales Person', ondelete='cascade', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', ondelete='cascade')
    property_tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    best_price = fields.Float(string="Best Offer", compute="_computed_best_price", store=True)
    visit_ids = fields.One2many('estate.property.visit', 'property_id', string="Visits")
    visit_count = fields.Integer(compute="_compute_visit_count")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price >= 1)',
        'The expected price must be strictly positive.'
    )

    @api.depends("living_area", "garden_area")
    def _computed_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends("offer_ids.price")
    def _computed_best_price(self):
        for rec in self:
            prices = rec.offer_ids.mapped('price')
            if prices:
                rec.best_price = max(prices)
            else:
                rec.best_price = 0.0

    @api.depends('visit_ids')
    def _compute_visit_count(self):
        visits = self.env['estate.property.visit']._read_group(
            domain=[
                ('property_id', 'in', self.ids),
                ('state', '=', 'scheduled')
            ], groupby=['property_id'], aggregates=['__count']
        )

        count_dict = {
            prop.id: count for prop, count in visits
        }

        for rec in self:
            rec.visit_count = count_dict.get(rec.id, 0)

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for rec in self:
            if float_is_zero(rec.selling_price, precision_digits=2):
                continue
            limit_price = rec.expected_price * 0.9
            if float_compare(rec.selling_price, limit_price, precision_digits=2) < 0:
                raise ValidationError(_("selling price cannot be lower than 90% of the expected price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _check_state(self):
        for rec in self:
            if rec.state not in ['new', 'cancelled']:
                raise UserError(_("As this property state in %s therefor you can not delete it.", rec.state))
        return True

    def action_property_cancelled(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError(_("%s property of %s can not be cancelled.", rec.state, rec.name))
            rec.state = 'cancelled'
        return True

    def action_property_sold(self):
        for rec in self:
            if rec.state == 'cancelled':
                raise UserError(_("%s property of %s can not be sold.", rec.state, rec.name))
            elif not rec.selling_price:
                raise UserError(_("Property can not be sold without selling price"))
            else:
                rec.state = 'sold'
        return True

    def action_best_offer(self):
        self.ensure_one()
        best_offer = self.offer_ids.filtered(lambda o: o.price == self.best_price)
        best_offer.action_accept_offer()
        return True
