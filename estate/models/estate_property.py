from odoo.fields import float_compare, float_is_zero
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class estate_property(models.Model):
    _name = "estate.property"  
    _description = "real estate property"
    _order = "id desc"
    
    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text() 
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=fields.Date.add(fields.Date.today(), months=+3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False,default=0.0)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()  
    state = fields.Selection(
        selection=[('New', 'New'), ('Offer Received', 'Offer Received'), ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Cancelled', 'Cancelled')],
        copy=False,
        required=True,
        default='New')
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    salesman_id = fields.Many2one("res.users", string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    property_type_id = fields.Many2one("estate.property.type")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id", string= "Offers")
    total_area = fields.Integer(compute="_compute_total_area")   
    best_offer = fields.Float(compute="_compute_best_offer")

    sequence = fields.Integer(string="Sequence", default=1) 
    company_id = fields.Integer(default=lambda self: self.env.user.company_id)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0 AND selling_price >= 0)', 'The expected price and selling price should be greater than equal to zero.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            all_sequences = record.offer_ids.mapped('price')
            record.best_offer = max(all_sequences) if all_sequences else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden: 
                record.garden_area = 1000
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = ""


    def action_set_property_as_cancle(self):
        if(self.state == 'Sold'):
            raise UserError(("Sold property can't be cancelled"))
        else: 
            self.state = 'Cancelled'

    def action_set_property_as_sold(self):
        if(self.state == 'Cancelled'):
            raise UserError(("Cancelled property can't be sold"))
        else: 
            self.state = 'Sold'

    def action_accept_offer(self):
        # Logic to accept the offer for the property
        for offer in self.offer_ids:
            offer.action_accept_offer()
        return True
    
    def action_refuse_offer(self):
        # Logic to refuse the offer for the property
        for offer in self.offer_ids:
            offer.action_refuse_offer()
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=2):
                continue
            min_price = 0.9 * record.expected_price
            if float_compare(record.selling_price, min_price, precision_rounding=2) < 0:
                raise ValidationError(
                    ("The selling price (%.2f) cannot be lower than 90%% of the expected price (%.2f).")
                    % (record.selling_price, min_price)
                )


    @api.ondelete(at_uninstall=False)
    def _check_deletion_state(self):
        for record in self:
            if record.state not in ['New', 'Cancelled']:
                raise UserError("You cannot delete a property unless its state is 'New' or 'Cancelled'.")




