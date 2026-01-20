import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.notification = useService("notification");
    },

    async _createReferralGiftCard() {
        const partner = this.currentOrder?.get_partner();
        if (!partner?.referred_by) return;

        const orderAmount = this.currentOrder.get_total_with_tax();
        const giftCardAmount = (orderAmount * 0.10).toFixed(2);
        try {
            await this.orm.call("loyalty.card", "create_referral_gift_card", [partner.id, this.currentOrder.get_total_with_tax(), this.currentOrder.id], {});
            this.notification.add(
                `Referral gift card of $${giftCardAmount} created for ${partner.referred_by.name}`,
                { type: "success" }
            );
        } catch (error) {
            this.notification.add("Failed to create referral gift card. Please try again.", { type: "danger", timeout: 5000 });
        }
    },

    async _finalizeValidation() {
        await super._finalizeValidation();
        if (this.currentOrder?.is_paid()) await this._createReferralGiftCard();
    },
});
