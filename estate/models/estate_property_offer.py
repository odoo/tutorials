from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _order = "price desc"
    _check__price = models.Constraint(
        'CHECK(price > 0)',
        'The price of an offer must be strictly positive.'
    )

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline"
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = start_date + relativedelta(days=+record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start_date).days

    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"
            for offer in record.property_id.offer_ids:
                if offer.id != record.id:
                    offer.status = "refused"
        return True

    def action_reject_offer(self):
        for record in self:
            record.status = "refused"
        return True
