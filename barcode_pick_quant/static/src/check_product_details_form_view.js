import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService } from "@web/core/utils/hooks";

export class CheckProductDetailsController extends FormController {
    setup() {
        super.setup(...arguments);
        this.notification = useService("notification");
    }

    /**
     * @override
     * Validates product details before executing the action button.
     */
    async beforeExecuteActionButton(clickParams) {
        if (clickParams.special !== "save") {
            return super.beforeExecuteActionButton(...arguments);
        }

        const productId = this.model.root.data.product_id?.[0];
        if (!productId) return super.beforeExecuteActionButton(...arguments);

        // Preserve the product data to prevent it from being reset
        const originalProductData = this.model.root.data.product_id;

        try {
            // Fetch product template ID from product
            const [productData] = await this.orm.searchRead(
                "product.product",
                [["id", "=", productId]],
                ["product_tmpl_id"],
                { limit: 1 }
            );

            if (!productData) return super.beforeExecuteActionButton(...arguments);

            const product_tmpl_id = productData.product_tmpl_id?.[0];

            // Fetch product type from template
            const [templateData] = await this.orm.searchRead(
                "product.template",
                [["id", "=", product_tmpl_id]],
                ["type"],
                { limit: 1 }
            );

            if (!templateData) return super.beforeExecuteActionButton(...arguments);

            const type = templateData.type;
            const locationId = this.model.root.data.location_id?.[0];
            const locationName = this.model.root.data.location_id?.[1] || "the selected location";

            // Fetch stock quantity and reserved quantity
            const [quantData] = await this.orm.searchRead(
                "stock.quant",
                [["product_tmpl_id", "=", product_tmpl_id], ["location_id", "=", locationId]],
                ["quantity", "reserved_quantity"],
                { limit: 1 }
            );

            const stockQty = quantData?.quantity ?? 0;
            const reservedQty = quantData?.reserved_quantity ?? 0;
            const qtyDone = this.model.root.data.qty_done ?? 0;

            // Validate stock availability
            if (stockQty - reservedQty > qtyDone && type === "consu") {
                return super.beforeExecuteActionButton(...arguments);
            }

            // Show confirmation dialog using a Promise
            return this.showConfirmationDialog(locationName)
                .then(async () => {
                    await super.beforeExecuteActionButton(...arguments);
                })

        } catch (error) {
            super.beforeExecuteActionButton(...arguments);
        }
    }

    /**
     * Shows a confirmation dialog and returns a Promise.
     * Resolves on "Confirm", rejects on "Discard".
     */
    showConfirmationDialog(locationName) {
        return new Promise((resolve, reject) => {
            this.dialogService.add(ConfirmationDialog, {
                body: `Oops! It seems that this product is not located at ${locationName}. Do you confirm you picked it there?`,
                confirmLabel: "Confirm",
                cancelLabel: "Discard",
                confirm: resolve,
                cancel: reject,
            });
        });
    }

    async afterExecuteActionButton(clickParams) {}
}

export const CheckProductDetails = {
    ...formView,
    Controller: CheckProductDetailsController,
};

registry.category("views").add("check_product_details", CheckProductDetails);
