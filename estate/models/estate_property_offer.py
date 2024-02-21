from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(
                    record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline -
                                   fields.Date.to_date(record.create_date)).days
            else:
                record.validity = (record.date_deadline -
                                   fields.Date.today()).days

    def action_accept(self):
        for record in self:
            if record.property_id.buyer_id:
                raise UserError(
                    "This property already has an accepted offer."
                )
            else:
                record.property_id.buyer_id = record.partner_id.id
                record.property_id.state = 'offer_accepted'
                record.status = 'accepted'
                record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
