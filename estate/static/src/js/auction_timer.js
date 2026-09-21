import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.AuctionTimer = publicWidget.Widget.extend({
    selector: ".js_auction_timer",
    start: function () {
        this._super.apply(this, arguments);
        this.endTimeStr = this.$el.data("auction-end");
        if (this.endTimeStr) {
            let formattedStr = String(this.endTimeStr).trim();
            if (!formattedStr.endsWith("Z") && !formattedStr.includes("Z")) {
                formattedStr = formattedStr.replace(" ", "T") + "Z";
            }
            this.targetDate = new Date(formattedStr).getTime();
            this._updateTimer();
            this.interval = setInterval(this._updateTimer.bind(this), 1000);
        }
    },
    _updateTimer: function () {
        const now = new Date().getTime();
        const diff = this.targetDate - now;

        if (diff <= 0) {
            this.$el.text("00:00:00:00");
            clearInterval(this.interval);
            return;
        }

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        const pad = (n) => String(n).padStart(2, '0');
        this.$el.text(`${pad(days)}:${pad(hours)}:${pad(minutes)}:${pad(seconds)}`);
    },
    destroy: function () {
        if (this.interval) {
            clearInterval(this.interval);
        }
        this._super.apply(this, arguments);
    }
});
