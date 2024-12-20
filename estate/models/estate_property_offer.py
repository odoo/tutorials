from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyType(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for real state properties"

    validity = fields.Integer(string="Validity (Days)", default=7)

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    property_id = fields.Many2one(comodel_name="estate.property")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Buyer")

    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    _sql_constraints = [
        ("check_price", "CHECK(price >= 0)", "Offer prices MUST be postive."),
    ]

    def action_accept(self):
        for record in self:
            record.property_id.action_process_accept(record)
            record.status = "accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = fields.Date.today()
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
