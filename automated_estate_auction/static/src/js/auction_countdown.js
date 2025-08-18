/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { deserializeDateTime } from "@web/core/l10n/dates";

const { DateTime } = luxon;

publicWidget.registry.EstateAuctionCountdown = publicWidget.Widget.extend({
    selector: ".o_estate_auction_countdown",

    start: function () {
        const _super = this._super.apply(this, arguments);
        const endTimeString = this.el.getAttribute("datetime");

        this.auctionEndTime = deserializeDateTime(endTimeString);
        this._updateCountdown();

        this.countdownInterval = setInterval(this._updateCountdown.bind(this), 1000);

        return _super;
    },

    _updateCountdown: function () {
        const now = DateTime.local();
        const remainingMillis = Math.max(0, this.auctionEndTime.diff(now).as("milliseconds"));

        let countdownText = "";

        if (remainingMillis > 0) {
            const hours = Math.floor(remainingMillis / (1000 * 60 * 60));
            const minutes = Math.floor((remainingMillis % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((remainingMillis % (1000 * 60)) / 1000);

            const formattedHours = String(hours).padStart(2, '0');
            const formattedMinutes = String(minutes).padStart(2, '0');
            const formattedSeconds = String(seconds).padStart(2, '0');

            countdownText = `${formattedHours}:${formattedMinutes}:${formattedSeconds}`;
            this.$el.html(`<i class="fa fa-clock-o me-1"></i> ${countdownText}`);
        } else {
            countdownText = "Auction Ended!";
            this.$el.text(countdownText);
            clearInterval(this.countdownInterval);
        }
    },
});
