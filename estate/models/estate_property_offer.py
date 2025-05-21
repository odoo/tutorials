from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An Offer on a property"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )

    validity = fields.Integer(string="Offer validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    # Relations
    property_id = fields.Many2one(comodel_name="estate.property", string="Property")
    partner_id = fields.Many2one("res.partner", string="Partner", copy=False)

    # Computed Fields
    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today(self) + relativedelta(days=10)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.date_deadline = fields.Date.today(self) + relativedelta(days=10)

    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price >= 0)', 'Offer price should be > 0'),
    ]
