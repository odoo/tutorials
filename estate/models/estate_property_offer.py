from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=True
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        required=True
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_set_date_deadline",
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(
                    record.create_date,
                    days=record.validity,
                )
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(),
                    days=record.validity,
                )

    def _set_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                    record.date_deadline -
                    record.create_date.date()
                ).days
