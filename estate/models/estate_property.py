from odoo import api, fields, models
from datetime import timedelta

today = fields.date.today()
three_months_later = (today + timedelta(days=90)).strftime("%Y-%m-%d")


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Test Model"

    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Avaliable From', default=three_months_later, copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default='2')
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], copy=False, default='new', required=True)
    active = fields.Boolean(string='Active', default=True)
    property_type_id = fields.Many2one("estate.property.type")
    salesman = fields.Many2one("res.users", default=lambda self: self.env.user or False)
    buyer = fields.Many2one("res.partner", copy=False)
    tag_id = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

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
