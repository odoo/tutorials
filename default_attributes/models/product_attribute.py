from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange("categ_id")
    def _compute_default_attribut_category(self):
        if self.categ_id:
            self.attribute_line_ids = [(5, 0, 0)]  # exisiting record ne clear karav

            attributes = []

            for attr in self.categ_id.attribute_ids:
                attribute_vals = attr.value_ids

                print(attribute_vals)

                attributes.append(
                    (
                        0,
                        0,
                        {
                            "attribute_id": attr.id,
                            "value_ids": [(6, 0, attribute_vals.ids)],
                        },
                    )
                )

                print(attributes)

            self.attribute_line_ids = attributes
