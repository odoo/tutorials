from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer description"

    price = fields.Float(string="Price")
    property_offer_ids = fields.Integer(string="Offer")
    state = fields.Selection(
        string="Status",
        copy=False,
        selection=[("acepted", "Accepted"), ("refused", "Refused")],
    )
    validity = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(
        compute="_sum_date", inverse="_compute_validity", string="Deadline",
    )

    salesman_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity")
    def _sum_date(self):

        for record in self:
            record.date_deadline = record.model.now() + record.validity

    def _compute_validity(self):

        for record in self:
            record.validity = record.model.now() - record.date_deadline
