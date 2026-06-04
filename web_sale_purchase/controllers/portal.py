from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from collections import OrderedDict


class SellerPortal(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        values["portal_vendor_category_enable"] = True

        if "purchase_count" in counters:
            partner = request.env.user.partner_id
            purchase_count = request.env["purchase.order"].search_count(
                [("partner_id", "=", partner.id)]
            )
            values["purchase_count"] = purchase_count

        return values

    def _get_purchase_searchbar_sortings(self):
        return {
            "date": {"label": "Newest", "order": "date_order desc, id desc"},
            "name": {"label": "Name", "order": "name asc, id asc"},
            "amount_total": {
                "label": "Total",
                "order": "amount_total desc, id desc",
            },
        }

    def _render_purchase_portal(
        self,
        template,
        page,
        url,
        date_begin,
        date_end,
        sortby,
        filterby,
        domain,
        searchbar_filters,
        default_filter,
        history,
        page_name,
        key,
    ):
        values = self._prepare_portal_layout_values()
        PurchaseOrder = request.env["purchase.order"]

        searchbar_sortings = self._get_purchase_searchbar_sortings()

        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        if not filterby:
            filterby = default_filter
        domain += searchbar_filters[filterby]["domain"]

        purchase_order_count = PurchaseOrder.search_count(domain)

        pager = portal_pager(
            url=url,
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
            },
            page=page,
            step=self._items_per_page,
            total=purchase_order_count,
        )

        orders = PurchaseOrder.search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )

        request.session[history] = orders.ids[:100]

        values.update(
            {
                "date": date_begin,
                key: orders,
                "page_name": page_name,
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
                "searchbar_filters": OrderedDict(sorted(searchbar_filters.items())),
                "filterby": filterby,
                "default_url": url,
            }
        )

        return request.render(template, values)

    @http.route(
        ["/my/purchase", "/my/purchase/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_purchase_orders(
        self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw
    ):
        partner = request.env.user.partner_id

        domain = [("partner_id", "=", partner.id)]

        searchbar_filters = {"all": {"label": "All", "domain": []}}

        return self._render_purchase_portal(
            template="web_sale_purchase.purchase_order_portal",
            page=page,
            url="/my/purchase",
            date_begin=date_begin,
            date_end=date_end,
            sortby=sortby,
            filterby=filterby,
            domain=domain,
            searchbar_filters=searchbar_filters,
            default_filter="all",
            history="my_purchase_history",
            page_name="purchase",
            key="orders",
        )
