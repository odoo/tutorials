from odoo import api, models, fields
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


def _default_date_availability():
    return fields.Date.today() + relativedelta(months=3)


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Information"

    name = fields.Char(required=True)
    description = fields.Text()
    property_tag_ids = fields.Many2many("estate.property.tag")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=_default_date_availability()
    )
    state = fields.Selection(
        string='Status',
        required=True,
        copy=False,
        default='new',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
    )
    expected_price = fields.Float(required=True)
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Orientation of the garden"
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
    )
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    offers_ids = fields.One2many('estate.property.offer', 'property_id')
    active = fields.Boolean(default=True)

    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Canceled properties cannot be set as sold.")
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.state = 'cancelled'
        return True

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offers_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offers_ids:
                record.best_price = max(record.offers_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
