from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta

class EstatePropertyModel(models.Model):
    _name = "estate.property"
    _description = "Estate Property"


    title = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availablility = fields.Date(default=date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('EAST','East'),('WEST','West'), ('SOUTH','South'), ('NORTH','North')])
    state = fields.Selection([("NEW","New"), ("OFFER_RECEIVED","Offer Received"), ("OFFER_ACCEPTED","Offer Accepted"), ("SOLD","Sold"), ("CANCELLED","Cancelled")], required=True, copy=False, default="NEW")
    estate_property_type_id = fields.Many2one("estate.property.type", string="Property Type", required=True)
    sales_person_id = fields.Many2one("res.users", string="Sales Person", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Price")
    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    @api.depends("offer_ids.price", "expected_price")
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids)==0:
                record.best_price = 0
            else:
                record.best_price = max(offer.price for offer in record.offer_ids)
                #record.best_price = max(record.offer_ids.mapped('price'))

    @api.onchange("garden")
    def _onchange_garden(self):

        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'NORTH' if self.garden else None