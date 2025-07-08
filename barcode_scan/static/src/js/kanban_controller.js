import { patch } from "@web/core/utils/patch";
import { rpc } from "@web/core/network/rpc";
import { useService, useBus } from "@web/core/utils/hooks";
import { ProductCatalogKanbanController } from "@product/product_catalog/kanban_controller";

patch(ProductCatalogKanbanController.prototype, {
    setup(){
        super.setup();
        this.orm = useService("orm");
        this.barcodeService = useService("barcode");
        useBus(this.barcodeService.bus, "barcode_scanned", (ev) => this.onBarcodeScannedHandler(ev.detail.barcode));
        this.resModel = this.props.context.product_catalog_order_model;
        this.notification = useService("notification");
    },

    async onBarcodeScannedHandler(barcode) {
        const [product] = await this.orm.searchRead(
            "product.product",
            [["barcode", "=", barcode]],
            ["id"],
            { limit: 1 }
        );
        if (!product) {
            this.notification.add(("No product found with barcode: ") + barcode, { type: "danger" });
            return;
        }

        let productQuantity;
        if (this.resModel == "sale.order") {
            productQuantity = "product_uom_qty";
        } else if (this.resModel == "purchase.order") {
            productQuantity = "product_qty";
        } else {
            console.error("Model not found");
            return;
        }

        const orderLines = await this.orm.searchRead(
            this.props.context.active_model,
            [["order_id", "=", this.props.context.order_id],
            ["product_id", "=", product.id]],
            ["id", productQuantity, "product_id"]
        );

        const existingQty = orderLines[0]?.[productQuantity] || 0;
        const finallyQuantity = existingQty + 1;
        await rpc("/product/catalog/update_order_line_info", {
            order_id: this.props.context.order_id,
            product_id: product.id,
            quantity: finallyQuantity,
            res_model: this.resModel,
        });

        this.model.load();
    }
});
