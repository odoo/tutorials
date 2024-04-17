from odoo import api, fields, models
from odoo.tools import date_utils

def date_in_3_months(*args):
    return date_utils.add(fields.Date.today(), months=3)

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "App to handle your real estate."

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", default=date_in_3_months, copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        default = 'new',
        copy=False
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
         for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for property in self:
            if len(property.offer_ids) == 0: 
                property.best_price = False
                continue
            property.best_price = max(property.offer_ids.mapped('price'))

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if(self.garden):
            self.garden_area = 10
            self.garden_orientation = "south"
        else:
            self.garden_area = False
            self.garden_orientation = False