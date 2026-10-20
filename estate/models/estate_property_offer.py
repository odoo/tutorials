# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta  # , datetime
from odoo.exceptions import UserError
from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate property offer"

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )

    property_id = fields.Many2one('estate.property', required=True)
    price = fields.Float(string='Price', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    status = fields.Selection(
        string='Status',
        selection=[
            ('refused', 'Refused'),
            ('accepted', 'Accepted'),
            ('pending', 'Pending')
        ]
    )
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Deadline',
                                compute="_compute_date_deadline",
                                inverse="_inverse_date_deadline")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            creation_date = record.create_date.date(
            ) if record.create_date else fields.Date.today()
            record.date_deadline = creation_date + \
                timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            creation_date = record.create_date.date(
            ) if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - creation_date).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.offer_ids.filtered(lambda o: o.status == "accepted"):
                raise UserError(
                    "An offer has already been accepted for this property.")
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer = offer.partner_id
            offer.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True
