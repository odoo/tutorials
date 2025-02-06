# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Contains offer made to properties"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ]
    )
    partner_id = fields.Many2one(
        string="Partner", comodel_name="res.partner", required=True
    )
    property_id = fields.Many2one(
        string="Property", comodel_name="estate.property", required=True
    )

    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )

    @api.depends("validity")
    def _compute_deadline(self):
        if not self.create_date:
            self.date_deadline = fields.Date.add(
                fields.date.today(), days=self.validity
            )
            return

        if self.validity >= 0:
            self.date_deadline = fields.Date.add(
                self.create_date, days=self.validity
            )
            return

        self.date_deadline = fields.Date.subtract(
            self.create_date, days=self.validity
        )

    def _inverse_deadline(self):
        if not self.create_date:
            self.validity = (self.date_deadline - fields.Date.today()).days
            return

        self.validity = (self.date_deadline - self.create_date.date()).days
