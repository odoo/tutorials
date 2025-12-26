from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import ValidationError, UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"
    _order = "id desc"

    _positif_expected_price = models.Constraint("CHECK (expected_price >= 0)", "A price can't be negatif")
    _positif_selling_price = models.Constraint("CHECK (selling_price >= 0)", "A price can't be negatif")

    state = fields.Selection(selection=[
                            ("new", "New"),
                            ("offer_received", "Offer Received"),
                            ("offer_accepted", "Offer Accepted"),
                            ("sold", "Sold"),
                            ("cancelled", "Cancelled")
                            ], default='new')

    active = fields.Boolean('Active', default=True)
    name = fields.Char(required=True, default="Unknown", string="Name")
    description = fields.Text(string="description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=lambda self: fields.Datetime.today() + relativedelta(months=3))
    last_seen = fields.Date(string="Last Seen", default=lambda self: fields.Datetime.now())
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")
    bedrooms = fields.Integer(default=2, string="Number of bedrooms")
    living_area = fields.Integer(string="Living Area Size m^2")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Contains a Garage ?")
    garden = fields.Boolean(string="Contains a Garden ?")
    garden_area = fields.Integer(string="Garden Area Size m^2")
    garden_orientation = fields.Selection(string="Garden orientation", selection=[
                                        ('north', 'North'),
                                        ('south', 'South'),
                                        ('east', 'East'),
                                        ('west', 'West')])

    total_area = fields.Float(string="Total Area m^2", compute="_compute_total_area")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    seller_id = fields.Many2one("res.users", default=lambda self: self.env.user, string="Seller")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.user.company_id, string="Owned by")

    def sell_property(self):
        for record in self:
            if (record.state == "cancelled"):
                raise UserError(self.env._("Can't sell cancelled property."))
            record.state = "sold"
            return True

    def cancel_property(self):
        for record in self:
            if (record.state == "sold"):
                raise UserError(self.env._("Can't cancel sold property."))
            record.state = "cancelled"
            return True

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if (not record.offer_ids):
                record.best_price = 0
                continue
            record.best_price = max(record.offer_ids.mapped('price'))

    @api.onchange("offer_ids")
    def _on_change_offer_ids(self):
        if (self.state == 'new' and len(self.offer_ids) != 0):
            self.state = 'offer_received'

    @api.onchange("garden")
    def _on_change_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else ''

    @api.constrains('selling_price', 'expected_price')
    def _constrain_prices(self):
        for record in self:
            if float_is_zero(record.selling_price, 2):
                continue
            if (float_compare(record.selling_price, record.expected_price * 0.8, 2) == -1):
                raise ValidationError(self.env._("Selling price is too low %(price)s", price=record.selling_price))

    @api.ondelete(at_uninstall=False)
    def _unlink_excpet_cancel_new(self):
        for record in self:
            if (record.state != 'new' and record.state != 'cancelled'):
                raise UserError(self.env._("Can't delete non-new and non-cancelled property"))
