from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'real estate property offer'

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
        ('accepted','Accepted'),
        ('refused','Refused'),],
        copy=False
     )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Date Dealine",compute="_compute_date_deadline" ,  inverse="_inverse_date_deadline")
    _sql_constraints = [
        (
            'positive_offer_price', 'CHECK(price > 0)', 'Offer price must be strictly positive'
        ),
    ]
    
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            current_date = fields.Date.today()
            record.date_deadline = current_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            current_date = fields.Date.today()
            if record.date_deadline:
                record.validity = relativedelta(record.date_deadline, current_date).days
            else:
                record.validity = 0

    ##############################################################################
    #  Offer Accept and Refuse
    ##############################################################################

    def action_accept_offer(self):
    
        self.status = "accepted"
        self.property_id.state = "offer_accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id
        
        other_offers = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),  
            ('id', '!=', self.id),
            ('status', '!=', 'refused')
        ])
        other_offers.write({'status': 'refused'})   

    def action_refuse_offer(self):
        self.status = "refused"
        return True
