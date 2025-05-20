import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.AuctionCountdown = publicWidget.Widget.extend({
    selector: "#auction-countdown",

    start() {
        this._startCountdown();
    },

    _startCountdown: function () {
        let timerElement = this.$el;
        let endTime = new Date(timerElement.data("end-time")).getTime();

        function updateCountdown() {
            let now = new Date().getTime();
            let timeLeft = endTime - now;

            if (timeLeft > 0) {
                let days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
                let hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                let minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
                let seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

                timerElement.text(`${days}d ${hours}h ${minutes}m ${seconds}s`);
            } else {
                clearInterval(timerInterval);
            }
        }

        let timerInterval = setInterval(updateCountdown, 1000);
        updateCountdown();
    },
});
