import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(ProductScreen.prototype, {
    onRemoveClick() {
        if (this.currentOrder.get_selected_orderline()) {
            this.currentOrder.removeOrderline(this.currentOrder.get_selected_orderline());
        }
    }
});