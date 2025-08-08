# -*- coding: utf-8 -*-

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request


class AutomatedRealEstateAuction(http.Controller):
    @http.route('/property/<model("estate.property"):property>/add_offer', auth='public', website=True)
    def object(self, property, **kwargs):
        return http.request.render('automated_real_estate_auction.add_offer', {
            'property': property
        })

    @http.route(['/property/<model("estate.property"):property>'], type='http', auth="public", website=True)
    def property_details(self, property, **kwargs):
        return http.request.render('estate.property_details_template', {
            'property': property,
        })

    @http.route(['/congratulations'], type='http', auth="public", website=True)
    def property_details(self, offer_maker, offer_price,  **kwargs):
        return http.request.render('automated_real_estate_auction.congratulations_page', {
            'offer_maker' : offer_maker,
            'offer_price' : offer_price
        })

    @http.route(['/properties', '/properties/page/<int:page>'], auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        Property = http.request.env['estate.property'].sudo()
        per_page= 6
        domain = [('status', 'not in', ['sold', 'cancelled'])]
        total_properties = Property.search_count(domain)
        properties = Property.search(domain, offset=(page-1) * per_page, limit=per_page)
        pager = http.request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=per_page
        )
        return http.request.render('estate.property_listing_template', {
            'properties': properties,
            'pager': pager
        })

    @http.route(['/estate/property/<int:property_id>/offer/submit'], type='http', auth="user", website=True, methods=['POST'])
    def property_offer_submit(self, property_id, **post):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        try:
            amount = float(post.get('amount', 0))
            partner_id = request.env.user.partner_id.id  # Ensures the logged-in user submits the offer

            if amount <= 0:
                raise ValidationError("Offer amount must be greater than zero.")

            offer_values = {
                'price': amount,
                'partner_id': partner_id,
                'property_id': property_id,
            }
            request.env['estate.property.offer'].sudo().create(offer_values)

            return request.redirect(f"/congratulations?offer_maker={request.env.user.name}&offer_price={amount}")

        except ValidationError as e:
            values = {
                'property': property_obj,
                'error': str(e),
            }
            return request.render("automated_real_estate_auction.add_offer", values)
