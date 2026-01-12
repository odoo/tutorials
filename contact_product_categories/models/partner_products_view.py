from odoo import fields, models, tools


def _addon_name():
    parts = __name__.split(".")
    if len(parts) >= 3 and parts[0] == "odoo" and parts[1] == "addons":
        return parts[2]
    return parts[0]


MODULE = _addon_name()


class PartnerProductsView(models.Model):
    _name = "partner.products.view"
    _description = "Partner Products (Grouped by Partner Categories)"
    _auto = False
    _rec_name = "product_tmpl_id"
    _order = "partner_id, company_category_id, product_tmpl_id"

    partner_id = fields.Many2one("res.partner", readonly=True)
    company_category_id = fields.Many2one("product.category", string="Business", readonly=True)
    product_tmpl_id = fields.Many2one("product.template", string="Product", readonly=True)

    # Optional convenience fields (nice in list view)
    product_name = fields.Char(related="product_tmpl_id.name", readonly=True)
    dosage_per_ton = fields.Float(related="product_tmpl_id.dosage_per_ton", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)

        rel_path = f"{MODULE}/sql/partner_products_view.sql"
        with tools.file_open(rel_path, "rb") as f:
            view_body = f.read().decode("utf-8").strip().rstrip(";")

        self.env.cr.execute(f"CREATE OR REPLACE VIEW {self._table} AS ({view_body})")

