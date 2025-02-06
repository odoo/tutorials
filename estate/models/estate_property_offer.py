from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This contains offer related configurations."

    price = fields.Float(string="Offer", required=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("accept", "Accepted"), 
            ("refuse", "Refused"), 
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    validity = fields.Integer(string="Validity (Days)", default=7)
    offer_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.offer_deadline = date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.offer_deadline-date).days
    
    def action_accept(self):
        for record in self:
            record.status = "accept"
                    # Find other records and set their status to "refused"
            other_records = self.search([('id', '!=', record.id), ('property_id', '=', record.property_id.id)])
            for other_record in other_records:
                other_record.status = 'refuse'
            bought_property = record.property_id
            bought_property.buyer_id = record.partner_id
            bought_property.selling_price = record.price
        return True

    def action_reject(self):
        for record in self:
            record.status = "refuse"
        return True
        