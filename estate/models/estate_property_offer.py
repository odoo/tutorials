from dateutil.relativedelta import relativedelta
from odoo import api, models, fields
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is the estate property offer model"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        copy=False
    )
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Date Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days

    def action_offer_accepted(self):
        for record in self:
            if record.property_id:
                if record.status == "accepted":
                    raise UserError("The offer is already accepted!!!")
                else:
                    record.property_id.offer_ids.write({"status":"refused"})
                    record.status = "accepted"
                    record.property_id.buyer_id = record.partner_id
                    record.property_id.selling_price = record.price
                    return True

    def action_offer_refused(self):
        for record in self:
            if record.property_id:
                if record.status == "refused":
                    raise UserError("The offer is already refused!!!")
                else:
                    record.status = "refused"
                    record.property_id.buyer_id = False
                    record.property_id.selling_price = 0
                    return True
