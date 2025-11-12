from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EstatePropertyOfferModel(models.Model):
    _inherit='estate.property.offer'

    sale_mode= fields.Selection(related="property_id.sale_mode", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_obj= self.env["estate.property"].browse(vals["property_id"])
            if property_obj.state=='sold':
                raise ValidationError("can not create offers for sold property")
            property_obj.state = "offer_received"
            if property_obj.sale_mode=='auction':
                if vals["price"]<property_obj.expected_price:
                    raise ValidationError("Offer Price must be greater than the expected price.")
            else:
                if vals["price"] < property_obj.best_offer:
                    raise ValidationError(
                        f"The offer must be higher than {property_obj.best_offer}"
                    )
        return models.Model.create(self, vals_list)
