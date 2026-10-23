from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'
    _rec_name = 'display_name'

    price = fields.Float(required=True)
    status = fields.Selection(selection=[('pending', 'Pending'), ('accepted', 'Accepted'), ('refused', 'Refused')], required=True, default="pending")
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    display_name = fields.Char(compute="_compute_display_name", store=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)

    _check_price_positive = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be greater than 0.'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_obj = self.env['estate.property'].browse(vals['property_id'])

            if property_obj.state in ['offer_accepted', 'sold', 'cancelled']:
                raise UserError(self.env._('Cannot create an offer for a property that is accepted, sold or cancelled'))

            if property_obj.best_price > vals['price']:
                raise ValidationError(self.env._('Cannot create an offer with a lower price than the best offer for that property.'))

            if property_obj.state == 'new':
                property_obj.state = 'offer_received'

        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _ondelete(self):
        self._unlink_prevent_accepted()
        self._unlink_update_property_state()

    def _unlink_prevent_accepted(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError(self.env._('Cannot delete an accepted offer'))

    def _unlink_update_property_state(self):
        properties = self.mapped('property_id')
        for p in properties:
            if not p.offer_ids and p.state == 'offer_received':
                p.state = 'new'

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Datetime.now()
            record.date_deadline = fields.Date.add(base_date.date(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = (record.create_date or fields.Datetime.now()).date()
            deadline_date = record.date_deadline or base_date
            record.validity = (deadline_date - base_date).days

    @api.depends('partner_id.name', 'price')
    def _compute_display_name(self):
        for record in self:
            if record.partner_id and record.price:
                record.display_name = f"{record.partner_id.name}'s offer ({record.price})"
            else:
                record.display_name = "New Offer"

    def action_accept(self):
        for record in self:
            if record.property_id.state in ['sold', 'cancelled']:
                raise UserError(self.env._("Cannot accept an offer for a sold or cancelled property."))

            if bool(record.property_id.accepted_offer_id):
                raise UserError(self.env._("There is already an accepted offer for this property"))

            other_offers = record.property_id.offer_ids - record
            other_offers.write({'status': 'refused'})

            record.status = 'accepted'
            record.property_id.accepted_offer_id = record
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'

        return True

    def action_refuse(self):
        for record in self:
            if record.property_id.state in ['sold', 'cancelled']:
                raise UserError(self.env._("Cannot refuse an offer for a sold or cancelled property."))

            if record.status == 'accepted':
                raise UserError(self.env._('Cannot refuse an accepted offer, you need to cancel it first.'))
            record.status = 'refused'

        return True

    def action_revert_pending(self):
        for record in self:
            record.status = 'pending'
            if record == record.property_id.accepted_offer_id:
                record.property_id.state = 'offer_received'
                record.property_id.selling_price = None
                record.property_id.buyer_id = None
                record.property_id.accepted_offer_id = None

        return True
