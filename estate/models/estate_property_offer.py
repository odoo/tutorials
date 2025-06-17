from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer made for the property'
    _order = 'price desc'

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute='_compute_deadline', inverse='_inverse_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id')

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)', "An offer price must be strictly positive"),
    ]

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            if not record.validity:
                record.date_deadline = False
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if not record.date_deadline:
                record.validity = 0
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_confirm(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
            record.property_id.state = 'offer_accepted'

            for offer in record.property_id.property_offer_ids:
                if offer.id != record.id:
                    offer.action_refuse()

        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'

        return True

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val_property_id = val.get('property_id')
            property = self.env['estate.property'].browse(val_property_id)

            if property.best_offer >= val.get('price'):
                raise UserError(_("A new offer price needs to be greater than current best offer."))

            property.state = 'offer_received'

        return super().create(vals)
