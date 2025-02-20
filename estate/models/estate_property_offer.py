from odoo import fields, models, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ]
    )

    partner_id = fields.Many2one('res.partner', string='Buyer', required=True) 
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    
    validity = fields.Integer(default=7)
    create_date = fields.Date(default=fields.Date.today(), readonly=True)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=+record.validity)

    @api.onchange("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def action_validate(self):
        if self.property_id.state == 'offer-accepted':
            raise exceptions.UserError("An offer has already been accepted.")
        self.status = 'accepted'
        self.property_id.state = 'offer-accepted'
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id
        
    def action_refuse(self):
        if self.status == 'accepted':
            self.property_id.selling_price = 0.0
            self.property_id.partner_id = None
            self.property_id.state = 'offer-received'
        self.status = 'refused'


    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)',
         'The offer price of a property must be positive.') 
    ]
