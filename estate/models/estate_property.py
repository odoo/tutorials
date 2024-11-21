from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_is_zero, float_compare


class EstatePropertyModel(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _rec_name = "title"
    _inherit = ['mail.thread']

    title = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availablility = fields.Date(default=date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('east', 'East'), ('west', 'West'), ('south', 'South'), ('north', 'North')])
    state = fields.Selection([("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")], required=True, copy=False, default="new")
    estate_property_type_id = fields.Many2one("estate.property.type", string="Property Type", required=True)
    sales_person_id = fields.Many2one("res.users", string="Sales Person", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Price")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price", "expected_price")
    def _compute_best_price(self):
        self.best_price = 0
        for record in self:
            if len(record.offer_ids) != 0:
                record.best_price = max(offer.price for offer in record.offer_ids)

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else None

    @api.onchange("offer_ids")
    def _onchange_offer(self):
        if (self.offer_ids == False or len(self.offer_ids) == 0) and self.state == 'offer_received':
            self.state = "new"
        if self.offer_ids != False and len(self.offer_ids) > 0  and self.state == 'new':
            self.state = "offer_received"

    def action_set_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(_("Cancelled properties cannot be sold"))
            if record.state == "sold":
                raise UserError(_("property is already sold"))
        self.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("Sold properties cannot be cancelled"))
            if record.state == "cancelled":
                raise UserError(_("property is already cancelled"))
        self.state = "cancelled"
        return True

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price must be positive.')
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 1) and float_compare(record.selling_price, record.expected_price * 0.9, 1) < 0 :
                raise ValidationError(_("The selling price must be at least 90% of the expected price"))

    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_is_new_or_cancelled(self):
        if any(property.state != 'new' and property.state != 'cancelled' for property in self):
            raise UserError(_('Only "new" and "cancelled properties can be deleted"'))

