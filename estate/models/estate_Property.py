from odoo import api
from odoo import fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class estate_Property(models.Model):
    _name = "estate_model"  
    _description = "This is the description for esatet properties model:"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Integer()
    date_availability = fields.Date(copy=False,default=fields.Date.today())
    expected_price = fields.Float(required=True, string="Expected_Price")
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
                            selection = [
                                ('north', 'North'), 
                                ('east', 'East'), 
                                ('south', 'South'),
                                ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(copy=False,
                            required=True, 
                            default='new',
                            selection = [
                                ('new', 'New'), 
                                ('offer_received', 'Offer_Received'), 
                                ('offer_accepted', 'Offer_accepted'), 
                                ('sold', 'Sold'), 
                                ('cancelled', 'Cancelled')]
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    property_type_id = fields.Many2one("estate_property_type_model", name="Property Type")
    salesman = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer')
    tag_ids = fields.Many2many("estate_property_tag_model", string="Tag")
    offer_ids = fields.One2many('estate_property_offer_model', 'property_id', string="Offers")
    total_area = fields.Float(compute="_compute_total_area", readonly=False)
    best_price = fields.Float(compute="_compute_best_price", store=True)

    ##### compute methods ######

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)
        
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    ###### action button ######

    def sold_action(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Property is solded")  
            if record.state == "cancelled":
                raise UserError("poperty is allready cancelled thats why we can not able to marked it as sold")
            record.state = "sold"
        return True
        
    def cancle_action(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Property is already cancelled")
            if record.state == "sold":
                raise UserError("property is already solded thats why we can not mareked it as cancelled")
            record.state = "cancelled"
        return True

    ###### constrains ######
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "Expected price should be strictly pisitive"),
        ("selling_price", "CHECK(selling_price > 0)", "Selling_price must be positive")
    ]