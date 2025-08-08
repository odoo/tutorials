from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route


class WebsiteSaleInherit(WebsiteSale):
    @route("/shop/vat/address", type="json", auth="public", website=True)
    def get_address(self, vat=None):
        if not vat:
            return {"error": "Please enter VAT number"}
        address_values = request.env["res.partner"].sudo()._l10n_in_get_partner_vals_by_vat(vat)
        if not address_values:
            return {"error": "Please enter valid VAT number"}
        address_values["country"] = request.env["res.country"].browse(address_values["country_id"]).name
        return address_values

    @route(
        "/shop/checkout",
        type="http",
        methods=["GET"],
        auth="public",
        website=True,
        sitemap=False,
    )
    def shop_checkout(self, try_skip_step=None, **query_params):
        response = super().shop_checkout(try_skip_step=try_skip_step, **query_params)
        if response.qcontext.get("order"):
            if response.qcontext.get(
                "order"
            ).partner_invoice_id != response.qcontext.get("delivery_addresses"):
                response.qcontext["want_tax_credit"] = True
                response.qcontext["partner"] = response.qcontext.get(
                    "order"
                ).partner_invoice_id
        return response

    @route(
        "/shop/billing_address/submit",
        type="json",
        auth="public",
        website=True,
    )
    def shop_billing_address_submit(self, vat=None, name=None, partner_id=None):
        order_sudo = request.website.sale_get_order()
        if partner_id:
            partner_sudo, _ = self._prepare_address_update(order_sudo, partner_id=int(partner_id))
            partner_sudo.write({"name": name})
            return {"partner_id": partner_id}
        address_values = (
            request.env["res.partner"].sudo()._l10n_in_get_partner_vals_by_vat(vat)
        )
        if not address_values:
            return {"error": "Please enter valid VAT number"}
        address_values.update(
            {
                "type": "invoice",
                "name": name,
                "phone": order_sudo.partner_id.phone,
                "email": order_sudo.partner_id.email,
            }
        )
        partner_sudo = request.env["res.partner"].sudo().create(address_values)
        order_sudo._update_address(partner_sudo.id, {"partner_invoice_id"})
        order_sudo.partner_id.write(
            {"type": "delivery", "parent_id": partner_sudo}
        )
        return {"partner_sudo": partner_sudo}
    