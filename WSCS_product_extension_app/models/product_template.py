from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_status_id = fields.Many2one("product.status", string="Product Status")
    customer_reference = fields.Char(string="Customer Reference")
    hs_code = fields.Char(string="HS Code")
    pallet_spec_ids = fields.One2many(
        "product.palletspec",
        "product_tmpl_id",
    )
    landed_cost = fields.Monetary(string="Landed Cost", currency_field="currency_id")
    margin_percent = fields.Float(
        string="Margin (%)", compute="_compute_margin", store=True
    )

    def write(self, vals):
        if "product_status_id" in vals:
            new_status = self.env["product.status"].browse(vals["product_status_id"])

            for record in self:
                current_status = record.product_status_id

                # Skip check if status didn't actually change
                if new_status.id == current_status.id:
                    continue

                # Special case: Allow switching between Active and Archived
                is_active_to_archived = (
                    current_status.name == "Active" and new_status.name == "Archived"
                )
                is_archived_to_active = (
                    current_status.name == "Archived" and new_status.name == "Active"
                )
                if is_active_to_archived or is_archived_to_active:
                    allowed_group = (
                        new_status.status_change_up_group_id
                        or new_status.status_change_down_group_id
                    )
                    if allowed_group:
                        xml_id = allowed_group.get_external_id().get(allowed_group.id)
                        if xml_id and not self.env.user.has_group(xml_id):
                            raise UserError(
                                (
                                    "You do not have the required group to move from '%s' to '%s'."
                                )
                                % (current_status.name, new_status.name)
                            )
                    continue

                if current_status and new_status.sequence < current_status.sequence:
                    raise UserError(
                        (
                            "You cannot downgrade product status from '%s' (sequence %s) "
                            "to '%s' (sequence %s)."
                        )
                        % (
                            current_status.name,
                            current_status.sequence,
                            new_status.name,
                            new_status.sequence,
                        )
                    )
                # Regular group check (status_change_up)
                required_group = new_status.status_change_up_group_id
                if required_group:
                    group_ext_id = required_group.get_external_id().get(
                        required_group.id
                    )
                    if group_ext_id and not self.env.user.has_group(group_ext_id):
                        raise UserError(
                            (
                                "You do not have permission to change product status to '%s'.\n"
                                "Required group: '%s'"
                            )
                            % (new_status.name, required_group.name)
                        )
        return super().write(vals)

    @api.depends("list_price", "standard_price", "landed_cost")
    def _compute_margin(self):
        for product in self:
            cost = product.standard_price + product.landed_cost
            if float_is_zero(product.list_price, precision_digits=2):
                product.margin_percent = 0.0
            else:
                margin = (product.list_price - cost) / product.list_price * 100
                product.margin_percent = margin
