from dateutil.relativedelta import relativedelta

from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is my fourth model"

    # Atomic fieldss

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", 'Accepted'),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # Relational fields

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    # Compute methods
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.today()

            record.date_deadline = start_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.today()

            record.validity = (record.date_deadline - start_date.date()).days

    # Button logic
    def accept_button(self):
        for record in self:
            offer_recordset = record.property_id.offer_ids
            for offer in offer_recordset:
                if offer.status == 'accepted' and offer != record:
                    error_message = "You can not accept multiple offer!"
                    raise exceptions.UserError(error_message)

            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.status = 'accepted'

    def refuse_button(self):
        for record in self:
            record.status = 'refused'
