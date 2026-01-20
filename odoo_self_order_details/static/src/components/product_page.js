import { patch } from "@web/core/utils/patch";
import { ProductPage } from "@pos_self_order/app/pages/product_page/product_page";
import { markup } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

// Patch the ProductPage to include self_order_description
patch(ProductPage.prototype, {
  async setup() {
    super.setup();

    const orm = useService("orm"); // or this.env.services.orm;

    const [rc] = await orm.read(
      "product.product",
      [this.props.product.id],
      ["self_order_description"]
    );
    
    if (rc?.self_order_description) {
      this.props.product.self_order_description = markup(
        rc.self_order_description
      );
    }
  },
});
