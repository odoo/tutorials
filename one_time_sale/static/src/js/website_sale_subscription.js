import { WebsiteSale } from "@website_sale/js/website_sale";
import publicWidget from "@web/legacy/js/public/public_widget";

WebsiteSale.include({
    _updateRootProduct($form) {
        this._super(...arguments);

        if (this._isSubscriptionPurchase($form)) {
            const selectedPlan = $form.find("select.plan_select:visible").val()
            this.rootProduct.plan_id = selectedPlan ? parseInt(selectedPlan) : undefined;
        }
    },

    _handleAdd($form) {
        this._super(...arguments);
        $form.find(this._isSubscriptionPurchase($form) ? ".one-time-purchase" : ".regular-delivery-purchase").hide();
    },

    _isSubscriptionPurchase($form) {
        return $form.find("#regular_delivery").prop("checked");
    }
});

publicWidget.registry.WebsiteSaleSubscription = publicWidget.Widget.extend({
    selector: ".oe_website_sale",

    start() {
        this._bindEvents();
        this._updateDisplayPrice(this.$("select.plan_select option:selected"));
        return this._super(...arguments);
    },

    _bindEvents() {
        this.$("select.plan_select").on("change", this._onSubscriptionPlanChange.bind(this));
    },

    _onSubscriptionPlanChange(event) {
        this._updateDisplayPrice($(event.target).find("option:selected"));
    },

    _updateDisplayPrice(selectedOption) {
        const selectedPrice = parseFloat(selectedOption.data("selected-price")) || 0;
        const discountText = selectedOption.data("discount") || "0%";

        $(".selected_price").text(selectedPrice.toFixed(2));
        $(".discount").text(discountText).toggle(discountText !== "0%");
        $(".oe_sale_price").toggle(discountText !== "0%");
    }
});
