import { SalespersonControlButtons } from "./control_buttons/control_buttons";
import { SalespersonOrderSummary } from "./order_summary/order_summary";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { registry } from "@web/core/registry";

export class CustomProductScreen extends ProductScreen {
    static components = {
        ...ProductScreen.components,
        ControlButtons: SalespersonControlButtons,
        OrderSummary: SalespersonOrderSummary
    };
}

registry.category("pos_screens").add("ProductScreen", CustomProductScreen, { force: true });
