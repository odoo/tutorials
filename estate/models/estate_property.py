from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Table that stores the estate properties"

    name = fields.Char(required=True)
    description = fields.Text()
    notes = fields.Html()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From", 
        copy=False, 
        default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False)
    best_offer = fields.Float(copy=False, compute="_compute_best_offer")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north','North'), 
            ('south','South'), 
            ('east','East'), 
            ('west','West')
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'), 
            ('received', 'Received'), 
            ('accepted', 'Accepted')
        ]
    )
    total_area = fields.Integer(
        compute="_compute_total_area",
        store=True,
        string="Total Area (sqm)",
    )
    # relations
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner")
    salesman_id = fields.Many2one("res.users")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max((offer.price for offer in record.offer_ids), default=0)         
    

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"   
            