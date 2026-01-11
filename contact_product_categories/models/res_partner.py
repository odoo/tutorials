from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    product_category_ids = fields.Many2many(
        comodel_name="product.category",
        relation="res_partner_product_category_rel",
        column1="partner_id",
        column2="categ_id",
        string="Product Categories",
        help="Internal product categories associated with this contact.",
    )

    product_tmpl_count = fields.Integer(
        string="Products",
        compute="_compute_product_tmpl_count",
    )

    capacity_tons = fields.Float(
        string="Capacity (tons)",
        help="Production capacity of this company in tons.",
        digits=(16, 2),
    )

    partner_status_id = fields.Many2one(
        "res.partner.status",
        string="Company Status",
        help="Company status (e.g., Existing Customer, Potential Customer).",
    )



    @api.depends("product_category_ids")
    def _compute_product_tmpl_count(self):
        ProductTmpl = self.env["product.template"]
        for partner in self:
            if not partner.product_category_ids:
                partner.product_tmpl_count = 0
                continue
            partner.product_tmpl_count = ProductTmpl.search_count(
                [("all_categ_ids", "child_of", partner.product_category_ids.ids)]
            )

    @api.constrains("is_company", "product_category_ids", "capacity_tons")
    def _check_company_only_fields(self):
        for partner in self:
            if not partner.is_company:
                if partner.capacity_tons:
                    raise ValidationError(_("Capacity can be set only for companies."))
                if partner.product_category_ids:
                    raise ValidationError(_("Only companies can have product categories."))
                if partner.partner_status_id:
                    raise ValidationError(_("Only companies can have statuses."))
            if partner.capacity_tons < 0:
                raise ValidationError(_("Capacity cannot be negative."))



    @api.onchange("is_company")
    def _onchange_is_company_clear_company_only_fields(self):
        for partner in self:
            if not partner.is_company:
                # Clear company-only fields for friendly UX
                if partner.capacity_tons:
                    partner.capacity_tons = 0.0
                if partner.product_category_ids:
                    partner.product_category_ids = [(5, 0, 0)]
                if partner.partner_status_id:
                    partner.partner_status_id = False
                return {
                    "warning": {
                        "title": _("Company fields cleared"),
                        "message": _("Capacity, Product Categories and Status are available only for companies."),
                    }
                }

    def _products_domain_for_partner_categories(self):
        self.ensure_one()
        if not self.product_category_ids:
            return [("id", "=", 0)]
        # Use all_categ_ids so products match main OR extra categories
        return [("all_categ_ids", "child_of", self.product_category_ids.ids)]

    def action_view_products_in_categories(self):
        """
        Smart button action: open product templates filtered by partner's categories.
        """
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Products",
            "res_model": "product.template",
            "view_mode": "list,form",
            "domain": self._products_domain_for_partner_categories(),
            "context": {
                # optional: can set defaults/search filters here if you want
                # "search_default_sale_ok": 1,
                "group_by": ["all_categ_ids"],
            },
        }