import { patch } from "@web/core/utils/patch";
import { rpc } from "@web/core/network/rpc";
import { useService, useBus } from "@web/core/utils/hooks";
import { ProductCatalogKanbanController } from "@product/product_catalog/kanban_controller";

patch(ProductCatalogKanbanController.prototype, {
    setup(){
        super.setup();
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.barcodeService = useService("barcode");
        console.log(this.props.context)
        useBus(this.barcodeService.bus, 'barcode_scanned', (ev) => this._onBarcodeScannedHandler(ev.detail.barcode));
    },
    
    async _onBarcodeScannedHandler(barcode) {
        console.log(barcode)
        const [product] = await this.orm.searchRead(
            "product.product",
            [["barcode", "=", barcode]],
            ["id", "display_name", "barcode"],
            { limit: 1 }
        )
        if (!product) {
            this.notification.add("No product found with barcode: " + barcode,
                { type: 'danger' }
            );
            return;
        }
        console.log(product)

        const orderLines = await this.orm.searchRead(
            this.props.context.active_model, 
            [["order_id", "=", this.props.context.order_id], ["product_id", "=", product.id]],
            ["id", "product_uom_qty"]
        );
        console.log(orderLines)

        if (orderLines.length) {
            const orderLine = orderLines[0];
            const newQty = orderLine.product_uom_qty + 1;

            await rpc("/product/catalog/update_order_line_info", {
                order_id: this.props.context.order_id,
                product_id: product.id,
                quantity: newQty, 
                res_model: this.props.context.product_catalog_order_model,
            });
        } else {
            await rpc("/product/catalog/update_order_line_info", {
                order_id: this.props.context.order_id,
                product_id: product.id,
                quantity: 1,
                res_model: this.props.context.product_catalog_order_model,
            });
        }
        
        this.model.load();
    }
})
