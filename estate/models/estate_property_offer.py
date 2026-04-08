from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property_offer"
    _description = "Offers received for property"
    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", required=True
    )
    property_id = fields.Many2one(
        comodel_name="estate_property", string="Property", required=True
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                (
                    record.create_date.date()
                    if record.create_date
                    else fields.Date.context_today(record)
                ),
                days=record.validity,
            )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (
                    record.date_deadline
                    - (
                        record.create_date.date()
                        if record.create_date
                        else fields.Date.context_today(record)
                    )
                ).days
