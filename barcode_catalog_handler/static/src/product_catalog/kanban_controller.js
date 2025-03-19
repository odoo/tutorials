import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";
import { useService, useBus } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

import { ProductCatalogKanbanController } from "@product/product_catalog/kanban_controller";

patch(ProductCatalogKanbanController.prototype, {

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.barcode = useService("barcode");
        this.action = useService("action");
        this.orderId = this.props.context.order_id;
        this.orderResModel = this.props.context.product_catalog_order_model;

        useBus(this.barcode.bus, "barcode_scanned", (event) => this.handleBarcodeScan(event.detail.barcode));
    },

    /**
     * Handles barcode scanning.
     * Searches for the scanned product and updates the order line.
     * 
     * @param {string} barcode - The scanned barcode value.
     */
    async handleBarcodeScan(barcode) {

        const [product] = await this.orm.searchRead(
            "product.product",
            [
                ...this.model.root.domain,
                ["barcode", "=", barcode]
            ],
            ["id", "name", "barcode"]
        );

        const hasVendorFilter = JSON.stringify(this.model.root.domain).includes("seller_ids");

        if(!product){
            const message = hasVendorFilter 
                ? _t("Try removing the top filter to broaden your search.")
                : _t("Product not found with this barcode!");
            
            this.notification.add(message, { type: "danger" });
            return;
        }

        await this.orderLineHandler(product);
        this.model.load();
    },

    /**
     * Handles the order line update when a product is scanned.
     * - If the product exists in the order, increase the quantity.
     * - If not, add the product with quantity = 1.
     * 
     * @param {Object} product - The product object found via barcode scan.
     */
    async orderLineHandler(product) {

        let orderLineQty = this.orderResModel == "sale.order" ? "product_uom_qty" : "product_qty";

        const orderLines = await this.orm.searchRead(
            this.props.context.active_model,
            [
                ["order_id", "=", this.orderId],
                ["product_id", "=", product.id]
            ],
            ["id", orderLineQty]
        )

        let newQty = 1;

        if (orderLines.length === 1) {
            const orderLine = orderLines[0];
            newQty = orderLine[orderLineQty] + 1;

            this.notification.add(`${product.name}'s quantity updated to ${newQty}.`, { type: "success" });
        }
        else if (orderLines.length > 1) {
            this.notification.add(`Multiple order lines found for ${product.name}. Please review.`, { type: "warning" });
            return;
        }
        else {
            this.notification.add(`${product.name} added to the order with quantity ${newQty}.`, { type: "success" });
        }

        await rpc("/product/catalog/update_order_line_info", {
            order_id: this.orderId,
            product_id: product.id,
            quantity: newQty,
            res_model: this.orderResModel,
        });
    },

});
