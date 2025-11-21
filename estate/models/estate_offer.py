from odoo import fields, models, api
from odoo.exceptions import UserError


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "property offer"
    _order = "price desc"

    price = fields.Float(string='Price')
    partner_id = fields.Many2one('res.partner', required=True, string='Partner')
    property_id = fields.Many2one('estate.property', required=True, string='Property')
    date_creation = fields.Date(readonly=True, default=fields.Date.today)
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        string='Deadline', compute="_compute_deadline", inverse="_inverse_deadline"
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id", stored=True)

    _check_price = models.Constraint(
        'CHECK(price >= 0)', 'The offer price must be positive'
    )

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                fields.Date.today(), days=record.validity
            )

    @api.onchange('date_deadline')
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            for offers in record.property_id.offer_ids:
                offers.status = "refused"
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            return True

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.state = "offer_received"
                record.property_id.selling_price = 0.0
                record.property_id.buyer_id = None

            record.status = "refused"
            return True

    @api.ondelete(at_uninstall=False)
    def _unlink_offer(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("You can't delete an accepted offer.")
