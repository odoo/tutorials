import * as ProductScreen from "@point_of_sale/../tests/tours/utils/product_screen_util";
import * as ProductScreenEmp from "./utils/product_screen_util";
import * as PaymentScreen from "@point_of_sale/../tests/tours/utils/payment_screen_util";
import * as ReceiptScreen from "@point_of_sale/../tests/tours/utils/receipt_screen_util";
import * as Dialog from "@point_of_sale/../tests/tours/utils/dialog_util";
import * as Chrome from "@point_of_sale/../tests/tours/utils/chrome_util";
import { registry } from "@web/core/registry";

registry.category("web_tour.tours").add("PosAddEmployeeToOrderline", {
    checkDelay: 50,
    steps: () =>
        [
            Chrome.startPoS(),
            Dialog.confirm("Open Register"),

            ProductScreen.addOrderline("Desk Pad", "5.0"),
            ProductScreen.addOrderline("Monitor Stand", "3.0"),
            ProductScreen.addOrderline("Whiteboard Pen", "2.0"),

            ProductScreen.clickOrderline("Desk Pad", "5.0"),
            ProductScreenEmp.clickEmployeeButton(),
            ProductScreenEmp.clickEmployee('Employee Test 3'),

            ProductScreen.clickOrderline("Whiteboard Pen", "2.0"),
            ProductScreenEmp.clickEmployeeButton(),
            ProductScreenEmp.clickEmployee('Employee Test 2'),

            ProductScreen.clickPayButton(),
            PaymentScreen.clickPaymentMethod("Cash"),
            PaymentScreen.clickValidate(),
            ReceiptScreen.isShown(),
        ].flat(),
});

registry.category("web_tour.tours").add("PosEmployeeAllFieldsDisplayed", {
    checkDelay: 50,
    steps: () =>
        [
            Chrome.startPoS(),
            Dialog.confirm("Open Register"),
            ProductScreen.addOrderline("Desk Pad", "2.0"),
            ProductScreenEmp.clickEmployeeButton(),
            ProductScreenEmp.checkContactValues(
                "Employee Test 5",
                "9898989005",
                "employee5@example.com"
            ),
            ProductScreenEmp.searchEmployeeValue("Test"),
            ProductScreenEmp.searchEmployeeValue("afa@exa"),
            ProductScreenEmp.searchEmployeeValue("9898"),
        ].flat(),
});
