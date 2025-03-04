import { SalespersonOrderWidget } from "../../../generic_components/order_widget/order_widget";
import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";

export class SalespersonOrderSummary extends OrderSummary {
    static components = {
        ...OrderSummary.components,
        OrderWidget: SalespersonOrderWidget,
    };
}
