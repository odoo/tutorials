/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { registry } from "@web/core/registry";

/**
 * We patch the form controller behavior through the "views" registry (safe for Odoo 19)
 * by patching the base "FormController" prototype.
 */
import { FormController } from "@web/views/form/form_controller";

patch(FormController.prototype, {
    /**
     * Intercept form changes. When company_type is changed from company -> person,
     * we stop the normal flow and open confirmation dialog.
     */
    async onFieldChanged(record, changes, options = {}) {
        // Call parent for everything except our special case.
        const isResPartner = record?.resModel === "res.partner";
        const hasCompanyTypeChange = changes && Object.prototype.hasOwnProperty.call(changes, "company_type");

        if (!isResPartner || !hasCompanyTypeChange) {
            return super.onFieldChanged(record, changes, options);
        }

        const oldValue = record.data.company_type;
        const newValue = changes.company_type;

        // Allow person -> company without extra checks
        if (oldValue === "person" && newValue === "company") {
            return super.onFieldChanged(record, changes, options);
        }

        // If company -> person: confirm and use wizard
        if (oldValue === "company" && newValue === "person") {
            // Revert UI immediately to avoid saving wrong value if user cancels
            // (We don't apply the change yet.)
            // NOTE: calling super with revert prevents the toggle staying on "person".
            await super.onFieldChanged(record, { company_type: "company" }, options);

            // Open confirmation dialog (Odoo-native)
            this.env.services.dialog.add(ConfirmationDialog, {
                title: _t("Convert to Individual"),
                body: _t(
                    "You are converting this contact to an Individual.\n\n" +
                    "Company-only fields will be cleared:\n" +
                    "• Capacity (tons)\n" +
                    "• Product Categories\n" +
                    "• Company Status\n\n" +
                    "Do you want to continue?"
                ),
                confirm: async () => {
                    // Trigger your wizard action (ensure this XMLID exists!)
                    await this.env.services.action.doAction(
                        "contact_product_categories.action_partner_convert_wizard",
                        { additionalContext: { active_id: record.resId } }
                    );
                },
                cancel: () => {
                    // nothing to do; we already reverted to "company"
                },
            });

            return;
        }

        // Fallback: default behavior
        return super.onFieldChanged(record, changes, options);
    },
});
