from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class EstatePortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'property_inquiry_count' in counters:
            inquiry_count = request.env['crm.lead'].search_count([
                ('type', '=', 'lead'),
                ('description', 'ilike', 'Property Inquiry'),
                ('partner_id', '=', request.env.user.partner_id.id)
            ])
            values['property_inquiry_count'] = inquiry_count

        if 'purchased_property_count' in counters:
            property_count = request.env['estate.property'].search_count([
                ('buyer_id', '=', request.env.user.partner_id.id),
                ('state', '=', 'sold')
            ])
            values['purchased_property_count'] = property_count

        return values

    @http.route(['/my/properties', '/my/properties/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_properties(self, page=1, sortby=None, search=None, search_in='all', **kwargs):
        values = self._prepare_portal_layout_values()

        PropertyInquiry = request.env['crm.lead']

        searchbar_sortings = {
            'date': {'label': 'Date', 'order': 'create_date desc'},
            'name': {'label': 'Property Name', 'order': 'name'},
            'stage': {'label': 'Stage', 'order': 'stage_id'},
        }

        searchbar_inputs = {
            'all': {'input': 'all', 'label': 'Search in All'},
            'name': {'input': 'name', 'label': 'Search in Property Name'},
            'description': {'input': 'description', 'label': 'Search in Description'},
        }

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if search and search_in:
            search_domain = []
            if search_in in ['all', 'name']:
                search_domain.append(('name', 'ilike', search))
            if search_in in ['all', 'description']:
                search_domain.append(('description', 'ilike', search))
        else:
            search_domain = []

        domain = [
            ('type', '=', 'lead'),
            ('description', 'ilike', 'Property Inquiry'),
            ('partner_id', '=', request.env.user.partner_id.id)
        ] + search_domain

        inquiry_count = PropertyInquiry.search_count(domain)

        pager = portal_pager(
            url="/my/properties",
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search},
            total=inquiry_count,
            page=page,
            step=self._items_per_page
        )

        inquiries = PropertyInquiry.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'inquiries': inquiries,
            'page_name': 'property',
            'pager': pager,
            'default_url': '/my/properties',
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'sortby': sortby,
            'search': search,
            'search_in': search_in,
        })

        return request.render("estate.portal_my_properties", values)

    @http.route(['/my/property/<int:inquiry_id>'], type='http', auth='user', website=True)
    def portal_property_inquiry(self, inquiry_id=None, **kwargs):
        inquiry = request.env['crm.lead'].sudo().browse(inquiry_id)

        if not inquiry.exists() or inquiry.partner_id.id != request.env.user.partner_id.id:
            return request.redirect('/my')

        if inquiry.type != 'lead' or 'Property Inquiry' not in inquiry.description:
            return request.redirect('/my')

        values = self._prepare_portal_layout_values()
        values.update({
            'inquiry': inquiry,
            'page_name': 'property',
        })

        return request.render("estate.portal_property_inquiry", values)

    @http.route(['/my/purchased-properties'], type='http', auth='user', website=True)
    def portal_my_purchased_properties(self, **kwargs):
        values = self._prepare_portal_layout_values()

        purchased_properties = request.env['estate.property'].search([
            ('buyer_id', '=', request.env.user.partner_id.id),
            ('state', '=', 'sold')
        ])

        values.update({
            'properties': purchased_properties,
            'page_name': 'purchased_properties',
        })

        return request.render("estate.portal_my_purchased_properties", values)

    @http.route(['/my/property/<int:property_id>/detail'], type='http', auth='user', website=True)
    def portal_property_detail(self, property_id=None, **kwargs):
        property_record = request.env['estate.property'].sudo().browse(property_id)

        if not property_record.exists():
            return request.redirect('/my')

        if property_record.buyer_id.id != request.env.user.partner_id.id and property_record.state != 'sold':
            inquiry_exists = request.env['crm.lead'].search_count([
                ('type', '=', 'lead'),
                ('description', 'ilike', f'Inquiry for property: {property_record.name}'),
                ('partner_id', '=', request.env.user.partner_id.id)
            ]) > 0

            if not inquiry_exists:
                return request.redirect('/my')

        values = self._prepare_portal_layout_values()
        values.update({
            'property': property_record,
            'page_name': 'property_detail',
        })

        return request.render("estate.portal_property_detail", values)
