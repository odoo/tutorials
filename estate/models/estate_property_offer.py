from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

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
    partner_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('estate.property')
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Date Dealine",compute="_compute_date_deadline" ,  inverse="_inverse_date_deadline")
    property_type_id=fields.Many2one(related="property_id.property_type_id", store=True)

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
        if self.property_id.state == 'cancelled':
            raise UserError("This property is already cancelled")
        self.status = "accepted"
        self.property_id.state = "offer_accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        
        other_offers = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),  
            ('id', '!=', self.id),
            ('status', '!=', 'refused')
        ])
        other_offers.write({'status': 'refused'})   

    def action_refuse_offer(self):
        self.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        property_ids = {vals['property_id'] for vals in vals_list}
        properties = self.env['estate.property'].browse(property_ids)
        if properties.state == 'sold':
            raise UserError("This property has already been sold and cannot receive new offers.")
        self.env['estate.property'].browse(property_ids).write({'state': 'offer_received'})

        offers = self.search([('property_id', 'in', list(property_ids))])
        best_offers = {offer.property_id.id: offer.price for offer in offers.sorted('price', reverse=True)}

        if any(vals['price'] <= best_offers.get(vals['property_id'], 0) for vals in vals_list):
            raise UserError("The offer price must be higher than the existing best offer!")

        return super().create(vals_list)
