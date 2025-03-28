/** @odoo-module */

import { patch } from '@web/core/utils/patch';
import { ProductCard } from '@pos_self_order/app/components/product_card/product_card';
import { ProductDetailScreen } from '@odoo_self_order_details/product_detail_screen/product_detail_screen';

patch(ProductCard.prototype, {
        selectProduct(qty = 1) {
        const product = this.props.product;

        if (!product.self_order_available || !this.isAvailable) {
            return;
        }
        
        if (product.isCombo()) {
            this.router.navigate('combo_selection', { id: product.id });
        } else if (product.isConfigurable()) {
            this.router.navigate('product', { id: product.id });
        }  else {
            this.dialog.add(ProductDetailScreen, {
                product: product,
                addToCart: (qty) => {
                    this.flyToCart();
                    this.scaleUpPrice();
                    
                    const isProductInCart = this.selfOrder.currentOrder.lines.find(
                        (line) => line.product_id === product.id
                    );
                    
                    if (isProductInCart) {
                        isProductInCart.qty += qty;
                    } else {
                        this.selfOrder.addToCart(product, qty);
                    }
                },
                close: () => this.dialog.close(),
            });
        }
    }
});
