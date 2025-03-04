import { OrderWidget } from "@point_of_sale/app/generic_components/order_widget/order_widget";

export class SalespersonOrderWidget extends OrderWidget {
    static props = {
        ...OrderWidget.props,
        sales_person: { type: String, optional: true },
    };
}
