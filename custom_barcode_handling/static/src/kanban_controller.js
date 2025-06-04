import { patch } from "@web/core/utils/patch";
import { rpc } from "@web/core/network/rpc";
import { useService, useBus } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";  
import { ProductCatalogKanbanController } from "@product/product_catalog/kanban_controller";

patch(ProductCatalogKanbanController.prototype, {
    setup(){
        super.setup();
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.barcodeService = useService("barcode");
        useBus(this.barcodeService.bus, "barcode_scanned", (ev) => this._onBarcodeScannedHandler(ev.detail.barcode));
        this.resModel = this.props.context.product_catalog_order_model;
    },
    
    async _onBarcodeScannedHandler(barcode) {
        const [product] = await this.orm.searchRead(
            "product.product",
            [["barcode", "=", barcode]],
            ["id"],
            { limit: 1 }
        );
        if (!product) {
            this.notification.add(_t("No product found with barcode: ") + barcode, { type: "danger" });
            return;
        }

        let quantityField;
        if (this.resModel === "sale.order") {
            quantityField = "product_uom_qty";
        } else if (this.resModel === "purchase.order") {
            quantityField = "product_qty";
        } else {
            console.error(_t("Unsupported order model:"), this.resModel);
            return;
        }

        const orderLines = await this.orm.searchRead(
            this.props.context.active_model, 
            [["order_id", "=", this.props.context.order_id], ["product_id", "=", product.id]],
            ["id", quantityField, "product_id"]
        );

        const existingQty = orderLines[0]?.[quantityField] || 0;
        const newQty = existingQty + 1;
        await rpc("/product/catalog/update_order_line_info", {
            order_id: this.props.context.order_id,
            product_id: product.id,
            quantity: newQty, 
            res_model: this.resModel,
        });
        
        this.model.load();
    }
});
