from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[("accepted", "Acepted"), ("refused", "Refused")]
    )
    partner_id = fields.Many2one(
        "res.partner",
        required=True
    )
    property_id = fields.Many2one(
        "estate.property",
        required=True
    )
    validity = fields.Integer(
        default=7,
        string="Validity (days)"
    )
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline"
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = fields.Date.today()
            record.date_deadline = fields.Date.add(fields.Date.to_date(record.create_date), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (fields.Date.to_date(record.date_deadline) - fields.Date.to_date(record.create_date)).days
