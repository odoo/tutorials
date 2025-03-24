from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offer'
    _order = 'price desc'
    

    creation_date = fields.Date('Creation Date', default=fields.Date.today())
    price = fields.Float('Price')
    status = fields.Selection(string='Status', selection=[
        ('accepted', 'Accepted'), 
        ('refused', 'Refused')
    ], copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', string='Property')
    validity = fields.Integer('Validity', default=7, help='Number of days the offer is valid.')
    date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='_inverse_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    
    
    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK (0 < price)', 'Check that the offer price is strictly positive.'),
    ]


    @api.depends('validity')	
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.creation_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            delta = record.date_deadline - record.creation_date
            record.validity = delta.days

    def refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.state = 'offer_received'
                record.property_id.selling_price = 0 
                record.property_id.buyer = None
            record.status = 'refused'

    def accept_offer(self):
        for record in self:
            if record.property_id.selling_price != 0:
                raise exceptions.UserError('An offer as already been accepted for this property.')
            record.property_id.state = 'offer_accepted'
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
    @api.model
    def create(self, vals):
        estate_property = self.env['estate.property'].browse(vals["property_id"])
        if vals["price"] < estate_property.best_price:
            raise exceptions.UserError(f'Offer must be higher than the current best offer({estate_property.best_price})')
        if estate_property.state == 'new':
            estate_property.state = 'offer_received'
        return super().create(vals)
