from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatepropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offers"

    price = fields.Float()
    status = fields.Selection(
    selection=[
        ('accepted', "Accepted"),
        ('refused', "Refused"),
    ],
    copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(
        string="Validity (days)",
        default=7
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(
                    record.create_date, days=record.validity,
                )
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity,
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                    record.date_deadline -
                    record.create_date.date()
                ).days

    def action_accept(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("This property is already sold!")
            if 'accepted' in record.property_id.offer_ids.mapped('status'):
                raise UserError("An offer has already been accepted!")
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )
