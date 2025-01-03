from odoo import fields, models , api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class TestProperty(models.Model):
    _name = "test.property"
    _description = "Test Model"

    name = fields.Char('name',required=True,default="My new House")
    description=fields.Text('description')
    postcode=fields.Char()
    date_availability=fields.Date('availability',default=(datetime.today() + relativedelta(months=3)).date(),copy=False)
    expected_price=fields.Float(readonly=True)
    best_price=fields.Float(readonly=True,compute="_compute_best_price")
    selling_price=fields.Float(readonly=True,copy=False)
    bedrooms=fields.Integer('bedrooms',default=2)   
    active = fields.Boolean("Active", default=True)

    garden_area = fields.Integer()
    living_area = fields.Integer()
    total_area = fields.Integer(compute='_compute_total_area')


    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_orientation=fields.Selection(selection = [('north', 'NORTH'), ('south', 'SOUTH'), ('east', 'EAST'), ('west', 'WEST')])
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        default="new",
        string="Status",
        required=True
    )
    property_types_id = fields.Many2one('test.property.type',ondelete='restrict')
    property_tags_id = fields.Many2many('test.property.tags')
    
    partner_id = fields.Many2one("res.partner", string="Buyer")
    sales_person_id=fields.Many2one('res.users', ondelete='restrict',default=lambda self: self.env.user)

    property_offers_id = fields.One2many('test.property.offer', 'property_id', string='offer')



    # @api.depends('living_area','garden_area')
    # def _compute_total_area(self):
    #     for record in self:
    #         record.total_area=record.living_area+record.garden_area


    @api.depends("property_offers_id.price")
    def _compute_best_price(self):
        for record in self:
            if record.property_offers_id:
                record.best_price = max(record.property_offers_id.mapped('price'))
            else:
                record.best_price = 0




    @api.depends("garden_area" , "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area


    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
            return {'warning': {
                'title': ("Warning"),
                'message': ('you have checked garden button')}}
        else:
            self.garden_area = 0
            self.garden_orientation = ""