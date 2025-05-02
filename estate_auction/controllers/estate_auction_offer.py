from odoo.exceptions import AccessError, MissingError, UserError, ValidationError
from odoo.http import Controller, request, route


class EstateAuctionOfferController(Controller):
    @route('/offer/create', type='http', auth='public', website=True, methods=['POST'])
    def create_offer(self, **payload):
        request.validate_csrf(payload.get('csrf_token'))
        try:
            property_id = int(payload.get('property_id'))
            offer_price = float(payload.get('offer_price'))
            partner_id = int(payload.get('partner_id'))
        except ValueError:
            return request.redirect(
                f'/property/{payload.get("property_id")}?error=Invalid input'
            )

        estate_property = request.env['estate.property'].sudo().browse(property_id)
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if not estate_property.exists() or not partner.exists():
            return request.redirect(
                f'/property/{payload.get("property_id")}?error=Property or Partner not found'
            )

        try:
            request.env['estate.property.offer'].sudo().create({
                'price': offer_price,
                'partner_id': partner_id,
                'property_id': property_id,
            })

            return request.redirect(f'/offer/success/{property_id}')
        except ValidationError as e:
            return request.redirect(
                f'/property/{property_id}?error=Invalid+data:+{e!s}'
            )
        except (AccessError, MissingError):
            return request.redirect(
                f'/property/{property_id}?error=Permission+or+Not+Found'
            )
        except UserError as e:
            return request.redirect(f'/property/{property_id}?error={e!s}')

    @route(
        '/offer/success/<int:property_id>',
        type='http',
        auth='public',
        website=True,
        methods=['GET'],
    )
    def offer_success(self, property_id):
        estate_property = request.env['estate.property'].sudo().browse(property_id)
        if not estate_property.exists():
            return request.not_found()

        return request.render(
            'estate_auction.template_property_offer_success',
            {'property': estate_property},
        )
