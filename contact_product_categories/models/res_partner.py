# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    # -----------------------
    # Company-only fields
    # -----------------------
    product_category_ids = fields.Many2many(
        comodel_name="product.category",
        relation="res_partner_product_category_rel",
        column1="partner_id",
        column2="categ_id",
        string="Product Categories",
    )

    capacity_tons = fields.Float(
        string="Capacity (tons)",
        digits=(16, 2),
    )

    partner_status_id = fields.Many2one(
        "res.partner.status",
        string="Company Status",
    )

    # -----------------------
    # UI helpers
    # -----------------------
    product_tmpl_count = fields.Integer(
        compute="_compute_product_tmpl_count"
    )

    is_company_lock_to_person = fields.Boolean(
        compute="_compute_is_company_lock_to_person",
        store=False,
    )

    # -----------------------
    # WRITE GUARD
    # -----------------------
    def write(self, vals):
        if (
            "is_company" in vals
            and vals["is_company"] is False
            and not self.env.context.get("allow_company_to_person")
        ):
            for partner in self:
                if partner.is_company:
                    raise UserError(_(
                        "To convert a company to an individual, use the "
                        "'Convert to Individual' button."
                    ))
        return super().write(vals)

    # -----------------------
    # COMPUTES
    # -----------------------
    @api.depends("product_category_ids")
    def _compute_product_tmpl_count(self):
        Product = self.env["product.template"]
        for partner in self:
            if not partner.product_category_ids:
                partner.product_tmpl_count = 0
                continue
            partner.product_tmpl_count = Product.search_count([
                ("all_categ_ids", "child_of", partner.product_category_ids.ids)
            ])

    def _compute_is_company_lock_to_person(self):
        for partner in self:
            partner.is_company_lock_to_person = bool(partner.is_company)

    # -----------------------
    # CONSTRAINTS (wizard-aware)
    # -----------------------
    @api.constrains("is_company", "capacity_tons")
    def _check_capacity_company_only(self):
        if self.env.context.get("allow_company_to_person"):
            return

        for partner in self:
            if not partner.is_company and (partner.capacity_tons or 0.0) > 0:
                raise ValidationError(
                    _("Capacity can be set only for companies.")
                )

    @api.constrains("is_company", "partner_status_id")
    def _check_status_company_only(self):
        if self.env.context.get("allow_company_to_person"):
            return

        for partner in self:
            if not partner.is_company and partner.partner_status_id:
                raise ValidationError(
                    _("Company Status can be set only for companies.")
                )

    @api.constrains("is_company", "product_category_ids")
    def _check_categories_company_only(self):
        if self.env.context.get("allow_company_to_person"):
            return

        for partner in self:
            if not partner.is_company and partner.product_category_ids:
                raise ValidationError(
                    _("Product Categories can be set only for companies.")
                )

    # -----------------------
    # ACTIONS
    # -----------------------
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