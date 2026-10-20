from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
    )
    date_deadline = fields.Date(
        compute="_compute_deadline",
        inverse="_compute_validity",
        string="Deadline",
    )

    @api.depends("date_deadline", "create_date")
    def _compute_validity(self):
        for record in self:
            date_created = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - date_created).days

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            date_created = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(date_created, days=record.validity)
