from odoo import api, models, fields
from odoo.tools.date_utils import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate model"

    name = fields.Char(required=True )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda _: fields.Datetime.today() + relativedelta(month=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()

    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
            string="state",
            selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')]
    )
    
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    property_tags_ids = fields.Many2many("estate.property.tag", string="Property Categories")
    offer_ids = fields.One2many("estate.property.offer", string="Offers", inverse_name="property_id")

    total_area = fields.Integer(compute="_compute_total_area", readonly=True)
    best_offer = fields.Integer(compute="_compute_best_offer", readonly=True) 

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.mapped('offer_ids.price')) if len(record.offer_ids) > 0 else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else ""
