import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.AuctionCountdown = publicWidget.Widget.extend({
    selector: ".auction_countdown", // The element where the countdown will be applied

    start: function () {
        this._super.apply(this, arguments);
        this.auctionEndTime = this.$el.data("auction-end");
        if (this.auctionEndTime) {
            this.startCountdown();
        }
    },

    startCountdown: function () {
        const self = this;
        const endTime = new Date(this.auctionEndTime).getTime();

        this.interval = setInterval(function () {
            const nowIst = new Date();
            const nowUtc = new Date(nowIst.getTime() - (5.5 * 60 * 60 * 1000));
            const now = nowUtc.getTime();
            const distance = endTime - now;

            if (distance <= 0) {
                clearInterval(self.interval);
                self.$el.text("Auction Ended");
            } else {
                const days = String(Math.floor(distance / (1000 * 60 * 60 * 24))).padStart(2, "0");
                const hours = String(Math.floor((distance / (1000 * 60 * 60)) % 24)).padStart(2, "0");
                const minutes = String(Math.floor((distance / (1000 * 60)) % 60)).padStart(2, "0");
                const seconds = String(Math.floor((distance / 1000) % 60)).padStart(2, "0");
                self.$el.text(`Time Left: ${days}d ${hours}h ${minutes}m ${seconds}s`);
            }
        }, 1000);
    },

    destroy: function () {
        clearInterval(this.interval);
        this._super.apply(this, arguments);
    },
});
