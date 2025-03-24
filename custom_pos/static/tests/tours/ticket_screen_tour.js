import * as ProductScreen from "@point_of_sale/../tests/tours/utils/product_screen_util";
import * as ReceiptScreen from "@point_of_sale/../tests/tours/utils/receipt_screen_util";
import * as PaymentScreen from "@point_of_sale/../tests/tours/utils/payment_screen_util";
import * as TicketScreen from "@point_of_sale/../tests/tours/utils/ticket_screen_util";
import * as Chrome from "@point_of_sale/../tests/tours/utils/chrome_util";
import * as Dialog from "@point_of_sale/../tests/tours/utils/dialog_util";
import { registry } from "@web/core/registry";


registry.category("web_tour.tours").add("TicketScreenBarcodeSearch", {
    checkDelay: 50,
    steps: () =>
        [
            Chrome.startPoS(),
            Dialog.confirm("Open Register"),
            ProductScreen.clickDisplayedProduct("Acoustic Bloc Screens (Wood)", true, "1.0", "80.0"),
            ProductScreen.clickPayButton(),
            PaymentScreen.clickPaymentMethod("Cash"),
            PaymentScreen.clickValidate(),
            ReceiptScreen.receiptIsThere(),
            ReceiptScreen.clickNextOrder(),
            Chrome.clickMenuOption("Orders"),
            TicketScreen.selectFilter("Paid"),
            TicketScreen.search("Product Barcode", "6016478556530"),
            {
                content: "Wait for search result to update for a valid barcode",
                trigger: ".order-row",
                run: function() {
                    const visibleOrders = document.querySelectorAll(".order-row");
                    if (visibleOrders.length !== 1) {
                        throw new Error(`Test failed: Expected 1 order, but found ${visibleOrders.length}`);
                    }
                }
            },     
            TicketScreen.search("Product Barcode", "invalid_barcode"),
            {
                content: "Wait for search results to update for an invalid barcode",
                trigger: ".orders",
                run: function() {
                    const visibleOrders = document.querySelectorAll(".order-row");
                    if (visibleOrders.length > 0) {
                        throw new Error(`Test failed: Found ${visibleOrders.length} orders for an invalid barcode`);
                    }
                }
            },
            Chrome.clickMenuOption("Close Register"),
        ].flat(),
});
