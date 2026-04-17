from odoo import fields, models, api
from datetime import date, timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([
        ('accepted', "Accepted"),
        ('refused', "Refused")
    ], copy=False)

    property_id = fields.Many2one('estate.property', required=True)
    partner_id = fields.Many2one('res.partner', required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_validity')
    property_type = fields.Many2one(related="property_id.property_type_id", string="Property Type")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:

            create_date = record.create_date.date() if record.create_date else date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:

            create_date = record.create_date.date() if record.create_date else date.today()
            record.validity = (record.date_deadline - create_date).days

    def action_accept_offer(self):
        for record in self.property_id.offer_ids:
            record.status = 'refused'

        for record in self.property_id.offer_ids:
            if record.status == 'accepted':
                raise UserError('Offer is already accepted')
                return False

        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id
        self.status = 'accepted'
        return True

    def action_reject_offer(self):

        self.status = 'refused'
        self.property_id.selling_price = 0
        self.property_id.buyer = ""
        return True
