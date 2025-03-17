import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";
import { ProductCatalogLastOrderOrderLine } from "./order_line/order_line";
import { patch } from "@web/core/utils/patch";

patch(ProductCatalogKanbanRecord.prototype, {
    setup() {
        super.setup();
    },

    get orderLineComponent() {
        if (this.env.orderResModel === "sale.order") {
            return ProductCatalogLastOrderOrderLine;
        }
        return super.orderLineComponent;
    },
});
