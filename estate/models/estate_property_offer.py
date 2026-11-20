from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(required=True)
    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("waiting", "Waiting for approval")
        ],
        default="waiting"
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    validity = fields.Integer(default=7)

    _check_price = models.Constraint(
        'CHECK(price >= 0)',
        'The price can\'t be negative.',
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = fields.Date.to_date(record.create_date)
            record.validity = (record.date_deadline - create_date).days

    def action_do_accept(self):
        for record in self:
            if any(state == "accepted" for state in record.property_id.mapped("offer_ids.state")):
                raise UserError(_("There is already an accepted offer."))
            record.property_id.offer_ids.write({"state": "refused"})
            record.state = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id.id
        return True

    def action_do_refuse(self):
        for record in self:
            if record.state == "accepted":
                record.property_id.selling_price = 0
                record.property_id.buyer_id = False
            record.state = "refused"
        return True
