import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@pos_self_order/app/components/product_card/product_card";
import { ProductDetailsPopup } from "./product_details_popup";

patch(ProductCard.prototype, {
    async selectProduct(qty){
        const product = this.props.product;
        if (this.selfOrder.ordering) {
            this.dialog.add(ProductDetailsPopup, {
                product: product,
                addOrderToCart: (qty) => {
                    super.selectProduct();
                },
                close: () => {
                    this.dialog.close();
                }
            });
        } else {
            super.selectProduct(qty);
        }
    }
});
