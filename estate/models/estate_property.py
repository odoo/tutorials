from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Type",
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        default='new',
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
        context={"no_create": True}
    )
    buyer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Buyer",
        copy=False
    )
    salesperson_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )
    total_area = fields.Integer(
        compute="_compute_total_area",
    )
    
    @api.depends('living_area', 'garden_area', 'garden')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0) if record.garden else (record.living_area or 0)
    
    
    best_price = fields.Float(
        string="Best Price",
        compute="_compute_best_price",
    )
    
    
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0
