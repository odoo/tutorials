from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer's"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(
        string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (
                    record.create_date
                    + fields.date_utils.relativedelta(days=record.validity)
                )
            else:
                record.date_deadline = (
                    fields.Datetime.now()
                    + fields.date_utils.relativedelta(days=record.validity)
                )

    # This method calculate the validity based on change in deadline
    # here type of create_date is datetime while type of date_deadline is date so need type conversion to date
    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days
            else:
                record.validity = (record.date_deadline - fields.Datetime.now()).days
