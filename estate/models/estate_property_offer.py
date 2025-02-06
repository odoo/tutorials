from odoo import api, fields, models, exceptions
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
    validity = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    # store=True means the value of date_deadline is stored in the database, so it can be used in searches, filters, and views.
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

    def action_accept(self):
        for record in self:
            if record.status == 'accepted' or record.status == 'refused':
                raise exceptions.UserError("Property is already accepted or refused.")
            else:
                all_offers = record.property_id.offer_ids  # Geting all offers og property
                for offer in all_offers:
                    if offer.id != record.id:  # Excluding the current offer
                        offer.status = 'refused'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.status = 'accepted' 

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted' or record.status == 'refused':
                raise exceptions.UserError("Property is already accepted or refused.")
            else:
                record.status = 'refused'
