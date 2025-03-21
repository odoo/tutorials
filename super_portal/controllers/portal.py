from collections import OrderedDict
from markupsafe import Markup
from operator import itemgetter

from odoo import _, http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.osv.expression import OR, AND
from odoo.tools import groupby as groupbyelem


class CustomPortal(CustomerPortal):

    #-------------------------------------------------------------------------------#
    # Generalise filter based on super and sub branch
    #-------------------------------------------------------------------------------#
    def _get_searchbar_filters(self):
        partner = request.env.user.partner_id
        filters = OrderedDict({'all': {'label': _('All'), 'domain': []}})

        partner_ids = request.env['res.partner'].search([
            ('id', 'child_of', partner.id),
            ('is_company', '=', True)
        ])

        for p in partner_ids:
            filters[str(p.id)] = {
                'label': p.name,
                'domain': [('partner_id', '=', p.id)],
            }
        return filters

    #-------------------------------------------------------------------------------#
    # Add filters for super-branch and sub-branch in each section
    # (sales orders, your invoices, our orders, tickets)
    #-------------------------------------------------------------------------------#

    #-------------------------------------------------------------------------------#
    # 1. invoices & bills
    def _get_account_searchbar_filters(self):
        branch_filters = self._get_searchbar_filters()
        filters = OrderedDict({
            'all': {'label': _('All'), 'domain': []},
            'invoices': {'label': _('Invoices'),
                         'domain': [('move_type', 'in', ('out_invoice', 'out_refund', 'out_receipt'))]},
            'bills': {'label': _('Bills'),
                      'domain': [('move_type', 'in', ('in_invoice', 'in_refund', 'in_receipt'))]},
        })
        filters.update(branch_filters)
        return filters

    #-------------------------------------------------------------------------------#
    # 2. your orders
    def _get_sale_searchbar_filters(self):
        return self._get_searchbar_filters()

    def _prepare_sale_portal_rendering_values(
        self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, quotation_page=False, **kwargs
    ):
        SaleOrder = request.env['sale.order']

        if not sortby:
            sortby = 'date'

        partner = request.env.user.partner_id
        values = self._prepare_portal_layout_values()

        if quotation_page:
            url = "/my/quotes"
            domain = self._prepare_quotations_domain(partner)
        else:
            url = "/my/orders"
            domain = self._prepare_orders_domain(partner)

        searchbar_sortings = self._get_sale_searchbar_sortings()
        searchbar_filters = self._get_sale_searchbar_filters()
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        sort_order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        pager_values = portal_pager(
            url=url,
            total=SaleOrder.search_count(domain),
            page=page,
            step=self._items_per_page,
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby},
        )
        orders = SaleOrder.search(domain, order=sort_order, limit=self._items_per_page, offset=pager_values['offset'])

        values.update({
            'date': date_begin,
            'quotations': orders.sudo() if quotation_page else SaleOrder,
            'orders': orders.sudo() if not quotation_page else SaleOrder,
            'page_name': 'quote' if quotation_page else 'order',
            'pager': pager_values,
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': searchbar_filters,
            'filterby': filterby
        })

        return values

    #-------------------------------------------------------------------------------#
    # 3. our orders
    @http.route(
        ['/my/purchase', '/my/purchase/page/<int:page>'], type='http',
        auth="user", website=True
    )
    def portal_my_purchase_orders(
        self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw
    ):
        return self._render_portal(
            "purchase.portal_my_purchase_orders",
            page, date_begin, date_end, sortby, filterby,
            [],
            self._get_searchbar_filters(),
            'all',
            "/my/purchase",
            'my_purchases_history',
            'purchase',
            'orders'
        )

    #-------------------------------------------------------------------------------#
    # 4. tickets
    def _prepare_my_tickets_values(
        self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all',
        search=None, groupby='none', search_in='content'
    ):

        values = self._prepare_portal_layout_values()
        domain = self._prepare_helpdesk_tickets_domain()

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'reference': {'label': _('Reference'), 'order': 'id desc'},
            'name': {'label': _('Subject'), 'order': 'name'},
            'user': {'label': _('Assigned to'), 'order': 'user_id'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc'},
        }
        searchbar_filters = self._get_searchbar_filters()
        searchbar_inputs = {
            'content': {
                'input': 'content',
                'label': Markup(_('Search <span class="nolabel"> (in Content)</span>'))
            },
            'ticket_ref': {'input': 'ticket_ref', 'label': _('Search in Reference')},
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'user': {'input': 'user', 'label': _('Search in Assigned to')},
            'status': {'input': 'status', 'label': _('Search in Stage')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'stage': {'input': 'stage_id', 'label': _('Stage')},
            'user': {'input': 'user_id', 'label': _('Assigned to')},
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        if groupby in searchbar_groupby and groupby != 'none':
            order = f'{searchbar_groupby[groupby]["input"]}, {order}'

        if filterby in ['last_message_sup', 'last_message_cust']:
            discussion_subtype_id = request.env.ref('mail.mt_comment').id
            messages = request.env['mail.message'].search_read(
                [('model', '=', 'helpdesk.ticket'), ('subtype_id', '=', discussion_subtype_id)],
                fields=['res_id', 'author_id'], order='date desc'
            )

            last_author_dict = {}
            for message in messages:
                if message['res_id'] not in last_author_dict:
                    last_author_dict[message['res_id']] = message['author_id'][0]

            ticket_author_list = request.env['helpdesk.ticket'].search_read(fields=['id', 'partner_id'])
            ticket_author_dict = {
                ticket['id']: ticket['partner_id'][0] if ticket['partner_id'] else False
                for ticket in ticket_author_list
            }

            last_message_cust = []
            last_message_sup = []
            ticket_ids = set(last_author_dict.keys()) & set(ticket_author_dict.keys())
            for ticket_id in ticket_ids:
                if last_author_dict[ticket_id] == ticket_author_dict[ticket_id]:
                    last_message_cust.append(ticket_id)
                else:
                    last_message_sup.append(ticket_id)

            if filterby == 'last_message_cust':
                domain = AND([domain, [('id', 'in', last_message_cust)]])
            else:
                domain = AND([domain, [('id', 'in', last_message_sup)]])

        else:
            domain = AND([domain, searchbar_filters[filterby]['domain']])

        if date_begin and date_end:
            domain = AND([domain, [('create_date', '>', date_begin), ('create_date', '<=', date_end)]])

        # Search
        if search and search_in:
            search_domain = []
            if search_in == 'ticket_ref':
                search_domain = OR([search_domain, [('ticket_ref', 'ilike', search)]])
            elif search_in == 'content':
                search_domain = OR([
                    search_domain, ['|', ('name', 'ilike', search), ('description', 'ilike', search)]
                ])
            elif search_in == 'user':
                assignees = request.env['res.users'].sudo()._search([('name', 'ilike', search)])
                search_domain = OR([search_domain, [('user_id', 'in', assignees)]])
            elif search_in == 'message':
                discussion_subtype_id = request.env.ref('mail.mt_comment').id
                search_domain = OR([
                    search_domain, [('message_ids.body', 'ilike', search),
                                    ('message_ids.subtype_id', '=', discussion_subtype_id)]
                ])
            elif search_in == 'status':
                search_domain = OR([search_domain, [('stage_id', 'ilike', search)]])
            
            domain = AND([domain, search_domain])

        # Pager
        tickets_count = request.env['helpdesk.ticket'].search_count(domain)
        pager = portal_pager(
            url="/my/tickets",
            url_args={
                'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby,
                'search_in': search_in, 'search': search, 'groupby': groupby, 'filterby': filterby
            },
            total=tickets_count, page=page, step=self._items_per_page
        )

        tickets = request.env['helpdesk.ticket'].search(
            domain, order=order, limit=self._items_per_page, offset=pager['offset']
        )
        request.session['my_tickets_history'] = tickets.ids[:100]

        # Group tickets if needed
        if not tickets:
            grouped_tickets = []
        elif groupby != 'none':
            grouped_tickets = [
                request.env['helpdesk.ticket'].concat(*g)
                for k, g in groupbyelem(tickets, itemgetter(searchbar_groupby[groupby]['input']))
            ]
        else:
            grouped_tickets = [tickets]

        values.update({
            'date': date_begin,
            'grouped_tickets': grouped_tickets,
            'page_name': 'ticket',
            'default_url': '/my/tickets',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_filters': searchbar_filters,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
            'search_in': search_in,
            'search': search,
            'filterby': filterby,
        })
        return values
