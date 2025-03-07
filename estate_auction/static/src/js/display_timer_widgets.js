import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.auctionCountdownWidget = publicWidget.Widget.extend({
    selector: '[data-auction_end_time]',
    start() {
        this.auctionEndTime = this.$el.data("auction_end_time");
        if (!this.auctionEndTime) {
            console.warn("No auction_end_time found");
            return;
        }
        this.endTime = new Date(this.auctionEndTime.replace(" ", "T")+"Z").getTime();
        this.timer = setInterval(this.updateCountdown.bind(this), 1000);
        this.updateCountdown();
    },

    updateCountdown() {
        // Get the current time in UTC
        const now = Date.now(); // UTC timestamp (milliseconds)
        // Calculate remaining time
        const timeLeft = this.endTime - now;

        // If auction time has expired
        if (timeLeft <= 0) {
            this.$el.text("Auction Ended");
            clearInterval(this.timer); // Stop the timer
            return;
        }

        // Calculate remaining days, hours, minutes, seconds
        const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

        // Display countdown in "Xd Xh Xm Xs" format
        this.$el.text(`${days}d ${hours}h ${minutes}m ${seconds}s`);
    },
});

export default publicWidget.registry.auctionCountdownWidget;
