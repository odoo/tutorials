import { Component,useState,useExternalListener,markup } from "@odoo/owl";

export class ProductPopDetails extends Component {
    static template = "odoo_self_order_details.ProductPopDetails";
    static props = ["product", "addToCart", "close"];

    setup() {
        this.self_order_description = markup(this.props.product.self_order_description || '');
        useExternalListener(window, "click", this.props.close);
        this.state = useState({
            qty: 1,
        });
    }

    addToCartAndClose() {
        this.props.addToCart(this.state.qty);
        this.props.close();
    }
}
