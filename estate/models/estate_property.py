from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property object"

    name = fields.Char(string="Name", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3),
                                    string="Available from")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection([('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
         ('cancelled', 'Cancelled')], default='new', copy=False, required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.uid, string="Salesperson")
    buyer_id = fields.Many2one("res.partner", copy=False, string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0.0
    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0.0
        self.garden_orientation = 'north' if self.garden else None
