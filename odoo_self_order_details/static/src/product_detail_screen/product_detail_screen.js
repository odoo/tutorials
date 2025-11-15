/** @odoo-module */

import { Component, useExternalListener, useState } from '@odoo/owl';

export class ProductDetailScreen extends Component {
    static template = 'odoo_self_order_details.ProductDetailScreen';
    static props = ['product', 'addToCart', 'close'];

    setup() {
        useExternalListener(window, 'click', this.props.close);
        this.state = useState({
            qty: 1,
        });
    }

    addToCartAndClose() {
        this.props.addToCart(this.state.qty);
        this.props.close();
    }
}
