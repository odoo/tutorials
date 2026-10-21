from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    def action_accept(self):
        for record in self:
            already_accepted = record.property_id.offer_ids.filtered(lambda offer: offer.status == 'accepted')

            if already_accepted:
                raise exceptions.UserError("Property cannot have several accepted offers")

            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date if record.create_date else fields.Date.today(self)
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date if record.create_date else fields.Date.today(self)
            record.date_deadline = fields.Date.add(base_date, days=record.validity * -1)
