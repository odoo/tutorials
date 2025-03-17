from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    vendor_status_id = fields.Many2one(
        "vendor.status",
        string="Vendor Status",
        help="Shows the Product Status for this Partner",
    )
    vendor_status_sequence = fields.Integer(
        related="vendor_status_id.sequence", store=True
    )
    vendor_product_category_ids = fields.Many2many(
        "product.category",
        "res_partner_product_category_rel",
        "partner_id",
        "category_id",
        string="Vendor Product Categories",
    )
    sedex_registered = fields.Selection(
        [("yes", "Yes"), ("no", "No")], string="Sedex Registered"
    )
    sedex_no = fields.Char(string="Sedex Number")
    ethical_audit = fields.Selection(
        [("yes", "Yes"), ("no", "No")], string="Ethical Audit Conducted?"
    )
    gfsi_certified = fields.Selection(
        [("yes", "Yes"), ("no", "No")], string="GFSI Certified"
    )
    gfsi_grade_id = fields.Many2one("gfsi.grade", string="GFSI Grade")
    gfsi_scheme_id = fields.Many2one("gfsi.scheme", string="GFSI Scheme")
    fsc_certified = fields.Selection(
        [("yes", "Yes"), ("no", "No")], string="FSC Certified"
    )
    pefc_certified = fields.Selection(
        [("yes", "Yes"), ("no", "No")], string="PEFC Certified"
    )
    certification_id = fields.Many2many("gfsi.certificate", string="Certification")

    @api.constrains(
        "sedex_registered",
        "sedex_no",
        "gfsi_certified",
        "gfsi_grade_id",
        "gfsi_scheme_id",
    )
    def _check_compliance_mandatories(self):
        for rec in self:
            if rec.sedex_registered == "yes" and not rec.sedex_no:
                raise ValidationError(
                    "Sedex Number is required when Sedex Registered is 'Yes'."
                )
            if rec.gfsi_certified == "yes":
                if not rec.gfsi_grade_id:
                    raise ValidationError(
                        "GFSI Grade is required when GFSI Certification is 'Yes'."
                    )
                if not rec.gfsi_scheme_id:
                    raise ValidationError(
                        "GFSI Scheme is required when GFSI Certification is 'Yes'."
                    )

    @api.onchange("vendor_status_id")
    def _onchange_vendor_status_id(self):
        if self.vendor_status_id:
            previous_status = self._origin.vendor_status_id
            user = self.env.user
            if (
                previous_status
                and self.vendor_status_id.sequence < previous_status.sequence
            ):
                raise ValidationError(
                    "Status changes cannot be made to a lower hierarchy!"
                )
            allowed_users = self.vendor_status_id.status_change_user_ids
            if allowed_users and user not in allowed_users:
                raise ValidationError(
                    "You are not allowed to change this Vendor Status!"
                )
