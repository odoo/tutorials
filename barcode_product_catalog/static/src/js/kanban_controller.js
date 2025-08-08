/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductCatalogKanbanController } from "@product/product_catalog/kanban_controller";
import { ManualBarcodeScanner } from "@stock_barcode/components/manual_barcode";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";
import { onMounted, onWillUnmount } from "@odoo/owl";

patch(ProductCatalogKanbanController.prototype, {
    setup() {
        super.setup();

        this.orm = useService("orm");
        this.barcodeService = useService("barcode");
        this.notification = useService("notification");
        this.dialogService = useService("dialog");

        this.orderId = this.props.context.order_id ;
        // console.log("orderId",this.orderId);
        this.orderModel = this.props.context.product_catalog_order_model;
        // console.log("orderModel",this.orderModel);

        this._onBarcodeScanned = this._onBarcodeScanned.bind(this);
        this._setupBarcodeScanner();

        onWillUnmount(() => {
            this.barcodeService.bus.removeEventListener("barcode_scanned", this._onBarcodeScanned);
        });
        onMounted(() => {
            if (document.activeElement instanceof HTMLElement) {
                document.activeElement.blur();
            }
        });
    },

    _setupBarcodeScanner() {
        // console.log("Listening for barcode scans...");
        this.barcodeService.bus.addEventListener("barcode_scanned", this._onBarcodeScanned);
    },

    _onBarcodeScanned(event) {
        event.preventDefault();
        event.stopPropagation();

        const barcode = event.detail.barcode;
        // console.log("Barcode scanned:", barcode);
        this._processBarcode(barcode);
    },

    openManualBarcodeDialog() {
        return new Promise((resolve, reject) => {
            this.dialogService.add(ManualBarcodeScanner, {
                facingMode: "environment",
                onResult: (barcode) => {
                    console.log("Manually entered barcode:", barcode);
                    // this._processBarcode(barcode);
                    resolve(barcode);
                },
                onError: reject,
            });
        }).catch(error => {
            console.error("Manual barcode dialog error:", error);
        });
    },

    async _findProductByBarcode(barcode) {
        const products = await this.orm.searchRead(
            "product.product",
            [["barcode", "=", barcode]],
            ["id", "name"],
            { limit: 1 }
        );
        return products[0] || null;
    },

    async _processBarcode(barcode) {
        try {
            const product = await this._findProductByBarcode(barcode);

            if (!product) {
                this.notification.add("No product found matching the scanned barcode.", { type: "warning" });
                return;
            }

            const { lineModel, qtyField } = this.getOrderLineInfo();
            if (!lineModel) {
                this.notification.add("Unsupported order type for barcode scanning.", { type: "warning" });
                console.warn("Unsupported order type:", this.orderModel);
                return;
            }

            const lines = await this.orm.searchRead(
                lineModel,
                [["order_id", "=", this.orderId], ["product_id", "=", product.id]],
                ["id", qtyField]
            );

            const currentQty = lines.length ? lines[0][qtyField] : 0;
            const newQty = currentQty + 1;

            await this._updateOrderLine(product.id, newQty);

            this.notification.add(`1 ${product.name} added to the order.`, { type: "success" });

            this.model.load();

        } catch (error) {
            console.error("Error processing barcode:", error);
            this.notification.add("Error processing barcode.", { type: "danger" });
        }
    },

    async _updateOrderLine(productId, quantity) {
        await rpc("/product/catalog/update_order_line_info", {
            res_model: this.orderModel,
            order_id: this.orderId,
            product_id: productId,
            quantity,
        });
    },

    getOrderLineInfo() {
        const map = {
            "sale.order": { lineModel: "sale.order.line", qtyField: "product_uom_qty" },
            "purchase.order": { lineModel: "purchase.order.line", qtyField: "product_qty" },
        };
        return map[this.orderModel] || { lineModel: null, qtyField: null };
    },
});
