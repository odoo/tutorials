from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

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
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _check_price = models.Constraint('CHECK (price > 0)', 'An offer price must be strictly positive')

    def action_accept(self):
        for record in self:
            already_accepted = record.property_id.offer_ids.filtered(lambda offer: offer.status == 'accepted')

            if already_accepted:
                raise UserError("Property cannot have several accepted offers")

            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
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

    @api.model
    def create(self, vals_list):

        for vals in vals_list:
            property_id = vals.get('property_id')
            property_record = self.env['estate.property'].browse(property_id)
            property_record.state = 'offer_received'

            if vals.get('price') < property_record.best_price:
                raise UserError(f'The offer must be higher than {property_record.best_price}')

        return super().create(vals_list)
