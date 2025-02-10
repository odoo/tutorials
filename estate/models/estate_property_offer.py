from odoo import fields, models, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "All the available offer for the property"

    property_id = fields.Many2one("estate.property", required = True)
    price = fields.Float(string = 'Price', required = True)
    buyer_id = fields.Many2one('res.partner', required = True)
    status = fields.Selection(
        string = "Status",
        copy = False,
        selection = [
            ("refuse", "Refuse"),
            ("accepted", "Accepted")
        ],
    )
    validity = fields.Integer(string = 'Validity(days)', default = 7)
    date_deadline = fields.Date(compute = '_compute_date_deadline', inverse = '_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = fields.Date.add(record.create_date, days = record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_offer_accepted(self):
        for record in self:
            if record.status != 'refuse':
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.buyer_id
                record.property_id.state = 'offer accepted'
                other_offers = record.property_id.offer_ids.filtered(
                    lambda offer: offer.id != record.id
                    )
                other_offers.write({'status' : 'refuse'})

            else:
                raise UserError('One offer is already accepted')
        return True

    def action_offer_rejected(self):
        for record in self:
            if record.status != 'accepted':
                record.property_id.selling_price = 0
                record.property_id.buyer_id = False
            record.status = False
        return True

