from odoo import fields, models, api,exceptions
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for property"

    price = fields.Float()
    status= fields.Selection(
        selection=[("accepted","Accepted"), ("refused","Refused")],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property',required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline",inverse="_inverse_date_deadline", store=True)
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
               
                    delta = record.date_deadline - fields.Date.today()
                    record.validity = delta.days
            else:
                record.validity=7
    
    def action_confirm(self):
        for record in self:
           
            existing_accepted_offer = self.env['estate.property.offer'].search([
                ('property_id', '=', record.property_id.id),
                ('status', '=', 'accepted')
            ], limit=1)

            if existing_accepted_offer:
                raise exceptions.UserError("An offer has already been accepted for this property. You cannot accept another offer.")
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True
    
    def action_cancel(self):
        for record in self:
            existing_accepted_offer = self.env['estate.property.offer'].search([
                ('property_id', '=', record.property_id.id),
                ('status', '=', 'accepted')
            ], limit=1)

            if existing_accepted_offer:
                raise exceptions.UserError("An offer has already been accepted. You cannot refuse any other offer.")

            record.status = "refused"

        return True