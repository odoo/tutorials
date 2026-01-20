import * as ProductScreen from "@point_of_sale/../tests/tours/utils/product_screen_util";
import * as Dialog from "@point_of_sale/../tests/tours/utils/dialog_util";
import * as Chrome from "@point_of_sale/../tests/tours/utils/chrome_util";
import { registry } from "@web/core/registry";
import * as ProductScreen2 from "@point_of_sale_second_uom/../tests/tours/utils/product_screen_util";
import * as Order from "@point_of_sale/../tests/tours/utils/generic_components/order_widget_util";


registry.category("web_tour.tours").add("SecondUomTour", {
    steps: () =>
        [
            Chrome.startPoS(),
            Dialog.confirm("Open Register"),
            ProductScreen.addOrderline("Test Product"),
            ProductScreen2.clickAddQuantity(),
            ProductScreen2.fillInputArea(".pos-second", "6"),
            Dialog.confirm(),
            Order.hasLine({quantity:"0.5"}),
        ].flat(),
});
