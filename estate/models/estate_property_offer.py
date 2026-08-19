from datetime import date, timedelta
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Price')
    status = fields.Selection(
        string='Status',
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
        readonly=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True,
    )
    property_id = fields.Many2one(
        comodel_name='estate.property',
        string='Property',
        required=True,
    )
    validity = fields.Integer(
        string='Validity (days)',
        default=7,
        required=True,
    )
    # Computed Field
    date_deadline = fields.Date(
        string='Date of Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    _check_price = models.Constraint(
        'check(price > 0)',
        'The offer price must be a positive amount and cannot be zero!',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = self._get_date_or_today(record.create_date) + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date_or_today = self._get_date_or_today(record.create_date)
            record.validity = (record.date_deadline - create_date_or_today).days

    @staticmethod
    def _get_date_or_today(datetime_to_evaluate):
        """ Returns the date part of a given datetime if present, otherwise returns today's date """
        return datetime_to_evaluate.date() if datetime_to_evaluate else date.today()

    # ACTIONS

    def action_accept_offer(self):
        for record in self:
            # If an offer is already accepted we can't accept another one
            record.property_id.ensure_no_accepted_offers(error_message="An offer was already accepted")

            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"

        return True
