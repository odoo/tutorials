import * as ProductScreen from "@point_of_sale/../tests/tours/utils/product_screen_util";
import * as Numpad from "@point_of_sale/../tests/tours/utils/numpad_util";
import * as Chrome from "@point_of_sale/../tests/tours/utils/chrome_util";
import * as Dialog from "@point_of_sale/../tests/tours/utils/dialog_util";
import { inLeftSide } from "@point_of_sale/../tests/tours/utils/common";
import { registry } from "@web/core/registry";


registry.category("web_tour.tours").add("OrderWidgetMinPricePopUp", {
    checkDelay: 50,
    steps: () =>
        [
            Chrome.startPoS(),
            ProductScreen.clickDisplayedProduct("Acoustic Bloc Screens (Wood)", true, "1.0", "80.0"),
            inLeftSide([
                ...ProductScreen.selectedOrderlineHasDirect("Acoustic Bloc Screens (Wood)", "1.0"),
                Numpad.click("Price"),
                Numpad.click("4"),
                Numpad.click("5"),
            ]),
            Dialog.is("Price Restriction"),
            Dialog.confirm(),
            inLeftSide([
                ...ProductScreen.selectedOrderlineHasDirect("Acoustic Bloc Screens (Wood)", "1.0"),
                Numpad.click("Price"),
                Numpad.click("6"),
                Numpad.click("0"),
            ]),
            Chrome.clickMenuOption("Close Register"),
        ].flat(),
});
