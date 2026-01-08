import { Component, onMounted, markup } from "@odoo/owl";

export class ProductDetailsPopup extends Component{
    static template = "odoo_self_order_details.ProductDetailsPopup";
    static props = ["product", "addOrderToCart", "close"];

    setup(){
        this.self_order_description = markup(this.props.product.self_order_description || '');
        this.popupTimeout = false;

        onMounted(() => {
            window.addEventListener("click", (event) => {
                this.popupTimeout && clearTimeout(this.popupTimeout);
                this.setPopupTimeout();
            });
            this.setPopupTimeout();
        });
    }

    addToOrder(){
        this.props.addOrderToCart(1);
        this.props.close();
    }

    setPopupTimeout(){
        this.popupTimeout = setTimeout(() => {
            this.props.close();
        }, 1000 * 60);
    }
}
