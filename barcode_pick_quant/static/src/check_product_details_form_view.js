/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService } from "@web/core/utils/hooks";

export class CheckProductDetailsController extends FormController {
    setup() {
        super.setup(...arguments);
        this.notification = useService("notification");
        this.dialogService = useService("dialog");
    }

    /**
     * @override
     * Validates product details before executing the action button.
     */
    async beforeExecuteActionButton(clickParams) {
        if (clickParams.special === "save") {
            try {
                const { location_id: locationData, qty_done: qtyDone = 0, available_quantity } = this.model.root.data;
                const locationName = locationData?.[1] || "the selected location";

                if (available_quantity > qtyDone) {
                    return super.beforeExecuteActionButton(clickParams);
                }

                const confirmed = await this.showConfirmationDialog(locationName);
                if (confirmed) {
                    return super.beforeExecuteActionButton(clickParams);
                }
                return false; // Prevent execution if the user cancels
            } catch (error) {
                console.error("Error in beforeExecuteActionButton:", error);
            }
        }

        return super.beforeExecuteActionButton(clickParams);
    }

    async showConfirmationDialog(locationName) {
        return new Promise((resolve) => {
            this.dialogService.add(ConfirmationDialog, {
                body: `Oops! It seems that this product is not located at ${locationName}. Do you confirm you picked it there?`,
                confirmLabel: "Confirm",
                cancelLabel: "Discard",
                confirm: () => resolve(true),
                cancel: () => resolve(false),
            });
        });
    }
}

export const CheckProductDetails = {
    ...formView,
    Controller: CheckProductDetailsController,
};

registry.category("views").add("check_product_details", CheckProductDetails);
