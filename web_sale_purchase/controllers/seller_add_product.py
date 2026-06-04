import base64
from odoo import http
from odoo.http import request, route


class SellerAddProduct(http.Controller):
    @route(route="/shop/add_product", type="http", website=True, author="user")
    def seller_add_product(self, **kw):
        current_user = request.env.user.partner_id

        if not current_user.is_seller:
            return request.redirect("/")

        return request.render("web_sale_purchase.seller_add_product_template")

    @route(
        route="/shop/create_product",
        type="http",
        website=True,
        author="user",
        methods=["POST"],
    )
    def seller_create_product(self, **kw):
        current_user = request.env.user.partner_id

        if not current_user.is_seller:
            return request.redirect("/")

        product_info = {
            "name": kw.get("name"),
            "list_price": float(kw.get("list_price")),
            "description": kw.get("description"),
            "seller_id": current_user.id,
            "website_published": kw.get("website_published"),
        }

        uploaded_file = request.httprequest.files.get("image_1920")
        if uploaded_file and uploaded_file.filename:
            file_binary = uploaded_file.read()
            product_info["image_1920"] = base64.b64encode(file_binary)

        request.env["product.template"].sudo().create(product_info)
        return request.redirect("my/marketplace/dashboard")
