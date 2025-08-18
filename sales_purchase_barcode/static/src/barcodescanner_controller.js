import { patch } from "@web/core/utils/patch";
import { ProductCatalogKanbanController } from "@product/product_catalog/kanban_controller";
import { rpc } from "@web/core/network/rpc";
import { useService, useBus } from "@web/core/utils/hooks";

patch(ProductCatalogKanbanController.prototype, {
    /**
     * @override
     */
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.barcodeService = useService('barcode');
        useBus(this.barcodeService.bus, 'barcode_scanned', (ev) => this._processBarcode(ev.detail.barcode));
    },

    /**
     * Processes the scanned barcode to find the corresponding product and update the order.
     *
     * @param {string} scannedBarcode The barcode string to process.
     */
    async _processBarcode(scannedBarcode) {
        // An order must be selected to add products.
        if (!this.orderId) {
            this.notification.add("Please select an order first.", { type: "warning" });
            return;
        }

        try {
            // Search for a product with the scanned barcode.
            const products = await this.orm.searchRead(
                "product.product",
                [["barcode", "=", scannedBarcode]],
                ["id", "name"]
            );

            if (!products.length) {
                this.notification.add("No product found for this barcode.", { type: "warning" });
                return;
            }

            const product = products[0];

            let orderLineModel, quantityField;
            // Determine the correct model and field names based on the order type.
            if (this.orderResModel === "sale.order") {
                orderLineModel = "sale.order.line";
                quantityField = "product_uom_qty";
            } else if (this.orderResModel === "purchase.order") {
                orderLineModel = "purchase.order.line";
                quantityField = "product_qty";
            } else {
                // Log an error if the order model is not supported.
                console.error("Unsupported order model for barcode scanning:", this.orderResModel);
                this.notification.add("Barcode scanning is not supported for this document type.", { type: "danger" });
                return;
            }

            // Check if there is an existing order line for this product.
            const existingOrderLines = await this.orm.searchRead(
                orderLineModel,
                [["order_id", "=", this.orderId], ["product_id", "=", product.id]],
                ["id", quantityField]
            );

            // If a line exists, increment its quantity; otherwise, set quantity to 1.
            const updatedQuantity = existingOrderLines.length ? existingOrderLines[0][quantityField] + 1 : 1;

            // Call the backend to create or update the order line.
            await rpc("/product/catalog/update_order_line_info", {
                res_model: this.orderResModel,
                order_id: this.orderId,
                product_id: product.id,
                quantity: updatedQuantity,
            });

            // Notify the user of the successful addition.
            this.notification.add(
                `Added ${product.name} (Qty: ${updatedQuantity})`,
                { type: "success" }
            );

            // Reload the view to show the updated order line information.
            this.model.load();

        } catch (error) {
            console.error("Error processing barcode scan:", error);
            this.notification.add("An error occurred while processing the barcode.", { type: "danger" });
        }
    },
});
