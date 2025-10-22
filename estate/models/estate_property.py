from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class Estateproperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description', required=True)
    postcode = fields.Char('Postcode', required=True)
    date_availability = fields.Date('Available From', copy=False, default=fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East')],
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        help="Estate state",
        default=('new')
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    salesperson = fields.Many2one('res.partner', string='Salesperson')
    buyer = fields.Many2one('res.users', string='Buyer', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")


    @api.depends("garden_area","living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price") or [0])

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None
