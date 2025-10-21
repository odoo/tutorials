from odoo import models, fields, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    ####################################################
    # FIELDS DECLARATION
    ####################################################

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

    ####################################################
    # FUNCTIONS DECLARATION
    ####################################################

    def accept_offer_button(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == "accepted" and offer.partner_id != record.partner_id:
                    raise exceptions.UserError("You can only accept one offer !")
                    break
            record.status = "accepted"
            record.property_id.partner_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def refuse_offer_button(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.partner_id = ""
                record.property_id.selling_price = 0
            record.status = "refused"
        return True

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = fields.Date.today()
            record.date_deadline = fields.Date.add(fields.Date.to_date(record.create_date), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (fields.Date.to_date(record.date_deadline) - fields.Date.to_date(record.create_date)).days
