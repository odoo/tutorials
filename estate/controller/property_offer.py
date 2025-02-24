from odoo.http import request, route
from odoo import http

class EstatePropertyOfferController(http.Controller):
    # ------------------------------------------------------------
    # MAKE OFFER
    # ------------------------------------------------------------
    @route('/property/make_offer/<int:property_id>', auth='public', website=True)
    def make_offer(self, property_id, **kwargs):

        property_data = request.env['estate.property'].sudo().browse(property_id)

        if not property_data:
            return request.not_found()

        return request.render("estate.estate_make_offer", {
            "property": property_data
        })

    # ------------------------------------------------------------
    # CREATE OFFER
    # ------------------------------------------------------------
    @route('/property/create_offer', auth="public", methods=['POST'], website=True, csrf=False)
    def create_offer(self, **kwargs):
        property_id = kwargs.get('property_id')
        offer_price = kwargs.get('price')
        validity = kwargs.get('validity')

        try:
            if property_id and offer_price:
                property_id = int(property_id)
                offer_price = float(offer_price)
                validity = int(validity)
                partner_id = request.env.user.partner_id.id

                property_data = request.env['estate.property'].sudo().browse(property_id)

                if property_data:
                    if property_data.best_price > offer_price:
                        message = "The offer price must be higher than best price!"
                    else:
                        property_data.offer_ids.sudo().create({
                            'property_id': property_id,
                            'partner_id': partner_id,
                            'price': offer_price,
                            'validity': validity
                        })
                        
                        message="Offer Created Successfully!"

        except Exception:
            message = "An error occured while creating the offer"

        return request.render("estate.estate_web_property_details", {
            "property": property_data,
            "message": message
        })
