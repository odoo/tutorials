from odoo import _, api, exceptions, fields, models
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "Properties of our managed estates"

    _check_positive_amounts = models.Constraint(
        'CHECK ('
        'expected_price >= 0 AND selling_price >= 0'
        ' AND living_area >= 0 AND facades >= 0'
        ' AND garden_area >= 0'
        ')', 'Values must be positive!')

    name = fields.Char(string='Name', default="Unknown", required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(required=True, default='new', copy=False, selection=[
        ('new', 'New')
        , ('offer_received', 'Offer Received')
        , ('offer_accepted', 'Offer Accepted')
        , ('sold', 'Sold')
        , ('cancelled', 'Cancelled'),
    ])
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    description = fields.Text(string='description')
    postcode = fields.Char(string='postcode')
    date_availability = fields.Date(string='Available from', default=lambda _: fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(string='expected price', required=True)
    selling_price = fields.Float(string='selling price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='# bedrooms', default=2)
    living_area = fields.Integer(string='living area size')
    facades = fields.Integer(string='# facades')
    garage = fields.Boolean(string='Has garage')
    garden = fields.Boolean(string='Has garden')
    garden_area = fields.Integer(string='garden area size')
    garden_orientation = fields.Selection(string='garden orientation',
    selection=[
        ('north', 'North')
        , ('south', 'South')
        , ('east', 'East')
        , ('west', 'West')])

    total_area = fields.Float(string="Total area", compute="_compute_total_area")
    best_price = fields.Float(string="Best offer", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            record.garden_area = 10 if record.garden else 0
            record.garden_orientation = 'north' if record.garden else None

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError(_("Cancelled properties cannot be sold!"))
            #
            record.state = "sold"
        return True

    def action_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError(_("Sold properties cannot be cancelled!"))
            #
            record.state = "cancelled"
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property in self:
            if float_is_zero(property.selling_price, 2):
                return
            if float_compare(property.selling_price, 0.9 * property.expected_price, 2) == -1:
                raise exceptions.ValidationError(_("The accepted price is less than 90% of the expected price!"))

    def confirm_sale(self):
        for property in self:
            accepted_offer = property.offer_ids.filtered(lambda r: r.status == 'accepted')
            accepted_offer.ensure_one()
            property.selling_price = accepted_offer.price
            property.buyer = accepted_offer.partner_id
            # Refuse all other offers
            (property.offer_ids - accepted_offer).action_cancel()
