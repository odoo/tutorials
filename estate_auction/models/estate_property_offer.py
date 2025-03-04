from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    # -------------------------------------------------------------------------
    # CONSTRAINTS METHODS
    # -------------------------------------------------------------------------

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.property_id.sale_type == 'auction':
                if record.price < record.property_id.expected_price:
                    raise ValidationError("The price must be higher than the expected price.")
            else:
                return super(EstatePropertyOffer, self)._check_price()

        return True

    # -------------------------------------------------------------------------
    # CRUD METHODS
    # -------------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property_obj = self.env['estate.property'].browse(val['property_id'])
            if property_obj.sale_type != 'auction':
                return super(EstatePropertyOffer, self).create(vals)

            if property_obj.state == 'sold':
                raise ValidationError("You cannot make an offer on a sold property.")

            if property_obj.state == 'new' or not property_obj.state:
                self.env['estate.property'].browse(val['property_id']).state = 'offer_received'

            min_price = self.env['estate.property'].browse(val['property_id']).expected_price
            if val['price'] <= min_price:
                raise ValidationError("The price must be higher than the expected price.")

            return models.Model.create(self, vals)

    # -------------------------------------------------------------------------
    # ACTION METHODS
    # -------------------------------------------------------------------------

    def action_confirm(self):
        if self.property_id.sale_type == 'auction':
            raise UserError("You cannot confirm an offer on an auction property.")

        super(EstatePropertyOffer, self).action_confirm()

    def action_cancel(self):
        if self.property_id.sale_type == 'auction':
            raise UserError("You cannot cancel an offer on an auction property.")

        super(EstatePropertyOffer, self).action_cancel()
