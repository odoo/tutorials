import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.AuctionCountdown = publicWidget.Widget.extend({
    selector: "#auction_countdown", 

    start: function () {
        this._super.apply(this, arguments);
        this.auctionEndTime = this.$el.data("auction-end");
        if (this.auctionEndTime) {
            console.log("Auction Countdown Started!");
            this.startCountdown();
        }
    },

    startCountdown: function () {
        const self = this;
        const endTime = new Date(this.auctionEndTime).getTime();

        this.interval = setInterval(function () {
            const now = new Date().getTime();
            const distance = endTime - now;

            if (distance <= 0) {
                clearInterval(self.interval);
                self.$el.text("Auction Ended");
            } else {
                const days = String(Math.floor(distance / (1000 * 60 * 60 * 24))).padStart(2, "0");
                const hours = String(Math.floor((distance / (1000 * 60 * 60)) % 24)).padStart(2, "0");
                const minutes = String(Math.floor((distance / (1000 * 60)) % 60)).padStart(2, "0");
                const seconds = String(Math.floor((distance / 1000) % 60)).padStart(2, "0");
                self.$el.text(`${days}d ${hours}h ${minutes}m ${seconds}s`);
            }
        }, 1000);
    },

    destroy: function () {
        clearInterval(this.interval);
        this._super.apply(this, arguments);
    },
});
