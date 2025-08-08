from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route


class WebsiteSaleInherit(WebsiteSale):
    @route("/shop/vat/address", type="json", auth="public", website=True)
    def get_address(self, vat=None):
        if not vat:
            return {"error": "Please enter VAT number"}
        address_values = request.env["res.partner"].sudo().enrich_by_gst(vat)
        if not address_values:
            return {"error": "Please enter valid VAT number"}
        return address_values

    @route(
        "/shop/billing_address/submit",
        type="json",
        auth="public",
        website=True,
    )
    def shop_billing_address_submit(self, address=None, name=None, partner_id=None):
        order_sudo = request.website.sale_get_order()
        if partner_id:
            partner_sudo = request.env["res.partner"].browse(int(partner_id))
            partner_sudo.write({"name": name})
            return True
        partner_sudo = request.env["res.partner"].sudo().create({
            'name': name,
            'company_type': 'company',
            'parent_id': False,
            'street': address.get('street'),
            'street2': address.get('street2'),
            'city': address.get('city'),
            'state_id': address.get('state_id', {}).get('id', False),
            'country_id': address.get('country_id', {}).get('id', False),
            'zip': address.get('zip'),
            'vat': address.get('vat'),
            'email': address.get("email") or order_sudo.partner_id.email,
            'phone': address.get("phone") or order_sudo.partner_id.phone,
        })
        order_sudo._update_address(partner_sudo.id, {"partner_invoice_id"})
        order_sudo.partner_id.write({"type": "delivery", "parent_id": partner_sudo})
        return True
