import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.AuctionTimer = publicWidget.Widget.extend({
    selector: "#auction_timer",
    
    start: function () {
        this._super.apply(this, arguments);
        this.startTimer();
    },

    startTimer: function () {
        let endTime = this.$el.data("end-time");

        if (!endTime) {
            console.error("Auction end time not set");
            return;
        }

        let countDownDate = new Date(endTime);
        let timerElement = this.$el;

        let x = setInterval(function () {
            let now = new Date();
            let utcNow = now.getTime() + now.getTimezoneOffset() * 60000;
            let distance = countDownDate - utcNow;

            if (distance < 0) {
                clearInterval(x);
                return;
            }

            let days = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60 * 24))
            let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((distance % (1000 * 60)) / 1000);

            timerElement.text(`${days}d ${hours}h ${minutes}m ${seconds}s`);
        }, 1000);
    }
});
