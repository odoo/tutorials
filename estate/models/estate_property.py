from odoo import api, fields, models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Test Model"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Avaliable From', default=fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default='2')
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], copy=False, default='new', required=True)
    active = fields.Boolean(string='Active', default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property")
    salesman = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user or False)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_id = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Property")
    total_area = fields.Float(string="Total area", compute="_compute_total_area")
    best_offer = fields.Float(string="Best offer", compute="_compute_best_offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(offer_id.price for offer_id in record.offer_ids)
            else:
                record.best_offer = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_cancel_property(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
            else:
                raise UserError("Sold properties can't be canceled")
        return True

    def action_sold_property(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
            else:
                raise UserError("Canceled properties can't be sold")
        return True
