import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@pos_self_order/app/components/product_card/product_card";

patch(ProductCard.prototype, {
  async selectProduct(qty = 1) {
    const product = this.props.product;

    if (!product.self_order_available || !this.isAvailable) {
      return;
    }

    if (product.isCombo()) {
      await super.selectProduct(qty);
    } else {
      this.router.navigate("product", { id: product.id });
    }
  },
});
