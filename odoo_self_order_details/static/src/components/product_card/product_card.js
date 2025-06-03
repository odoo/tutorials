// Part of Odoo. See LICENSE file for full copyright and licensing details.

import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@pos_self_order/app/components/product_card/product_card";

patch(ProductCard.prototype, {
    async selectProduct(qty = 1) {
        const product = this.props.product;

        if (!product.self_order_available || !this.isAvailable) {
            return;
        }

        if (product.isCombo()) {
            const selectedCombos = [];
            let showComboSelectionPage = false;
            for (const combo of product.combo_ids) {
                const { combo_item_ids } = combo;
                if (combo_item_ids.length > 1 || combo_item_ids[0]?.product_id.isConfigurable()) {
                    showComboSelectionPage = true;
                    break;
                }
                selectedCombos.push({
                    combo_item_id: this.selfOrder.models["product.combo.item"].get(
                        combo_item_ids[0].id
                    ),
                    configuration: {
                        attribute_custom_values: [],
                        attribute_value_ids: [],
                        price_extra: 0,
                    },
                });
            }

            if (showComboSelectionPage) {
                this.router.navigate("combo_selection", { id: product.id });
            } else {
                this.flyToCart();
                this.selfOrder.editedLine?.delete();
                this.selfOrder.addToCart(product, 1, "", {}, {}, selectedCombos);
            }
        } else {
            this.router.navigate("product", { id: product.id });
        }
    }
});

