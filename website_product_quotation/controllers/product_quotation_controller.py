from odoo import http
from odoo.http import Controller, request


class ProductQuotationController(Controller):
    @http.route("/product_quotation", type="http", auth="public", website=True)
    def show_page(self):
        product_names = [
            "Product A",
            "Product B",
            "Product C",
            "Product D",
            "Product E",
            "Product F",
            "Product G",
            "Product H",
        ]

        products = (
            request.env["product.template"]
            .sudo()
            .search([("name", "in", product_names)], limit=8)
        )

        product_data = []
        website = request.website

        for product in products:
            extra_images = (
                request.env["product.image"]
                .sudo()
                .search([("product_tmpl_id", "=", product.id)])
            )

            extra_image_data = [
                {
                    "url": website.image_url(img, "image_1024"),
                    "name": img.name if img.name else "Untitled Image",
                }
                for img in extra_images
            ]

            product_data.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "image_url": website.image_url(product, "image_1024"),
                    "extra_images": extra_image_data,
                    "size": product.attribute_line_ids.filtered(
                        lambda l: l.attribute_id.name == "SizeW"
                    ).mapped("value_ids.name"),
                    "color": product.attribute_line_ids.filtered(
                        lambda l: l.attribute_id.name == "Color"
                    ).mapped("value_ids.name"),
                    "fabric": product.attribute_line_ids.filtered(
                        lambda l: l.attribute_id.name == "Fabric"
                    ).mapped("value_ids.name"),
                    "print": product.attribute_line_ids.filtered(
                        lambda l: l.attribute_id.name == "Print"
                    ).mapped("value_ids.name"),
                    "url": f"/shop/product/{product.id}",
                }
            )

        return request.render(
            "website_product_quotation.product_quote_template",
            {"products": product_data},
        )
