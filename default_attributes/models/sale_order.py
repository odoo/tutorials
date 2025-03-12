from odoo.http import request, route
from odoo.addons.sale.controllers.product_configurator import (
    SaleProductConfiguratorController,
)


class DefaultAttributeProductConfiguratorController(SaleProductConfiguratorController):
    @route("/sale/product_configurator/get_values", type="json", auth="user")
    def sale_product_configurator_get_values(
        self,
        product_template_id,
        quantity,
        currency_id,
        so_date,
        ptav_ids=None,
        **kwargs,
    ):
        """
        Override product configurator to set default attribute values based on Global Info.
        """
        product_template = request.env["product.template"].browse(product_template_id)

        if product_template:
            filtered_ptav_ids = (
                request.env["sale.order.global.info"]
                .search([("category_name", "=", product_template.categ_id.name)])
                .mapped("attribute_value_id")
            )
        else:
            filtered_ptav_ids = ptav_ids

        # Find the corresponding product.template.attribute.value records
        default_ptav_ids = (
            request.env["product.template.attribute.value"]
            .search(
                [
                    (
                        "product_attribute_value_id",
                        "in",
                        [val.id for val in filtered_ptav_ids],
                    ),
                    (
                        "attribute_line_id",
                        "in",
                        product_template.attribute_line_ids.ids,
                    ),
                ]
            )
            .ids
        )

        # Call the original method, but pass default attributes
        response = super().sale_product_configurator_get_values(
            product_template_id,
            quantity,
            currency_id,
            so_date,
            ptav_ids=default_ptav_ids,  # Use default attributes
            **kwargs,
        )
        return response
