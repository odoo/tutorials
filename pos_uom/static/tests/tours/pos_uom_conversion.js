import * as Dialog from "@point_of_sale/../tests/tours/utils/dialog_util";
import * as Chrome from "@point_of_sale/../tests/tours/utils/chrome_util";
import { registry } from "@web/core/registry";
import * as Utils from "@point_of_sale/../tests/tours/utils/common";
import { waitForLoading } from "@point_of_sale/../tests/tours/utils/common";
import * as ProductScreen from "@point_of_sale/../tests/tours/utils/product_screen_util";

registry.category("web_tour.tours").add("pos_uom_conversion", {
    steps: () =>
        [
            waitForLoading(),
            Chrome.startPoS(),
            Dialog.confirm("Open Register"),
            ProductScreen.clickDisplayedProduct("Apple", "1.0"),
            Utils.selectButton("Add Quantity"),
            {
                "trigger": ".o_input",
                "content": "enter input",
                "run": "edit 6"
            },
            {
                "trigger": ".o-default-button:nth-child(1)",
                "content": "click confirm",
                "run": "click"
            },
            ProductScreen.selectedOrderlineHas("Apple", "0.5"),
            ProductScreen.closePos(),
        ].flat(),
});
