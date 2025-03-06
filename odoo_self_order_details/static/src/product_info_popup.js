import { Component } from "@odoo/owl";

export class CustomProductInfoPopup extends Component {
    static template = "odoo_self_order_details.ProductInfoPopup";
    static props = ["addToCart"];

    orderProduct() {
        this.props.addToCart(1);
        this.props.close();
    }
}
