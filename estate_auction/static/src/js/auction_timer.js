import publicWidget from "@web/legacy/js/public/public_widget";


publicWidget.registry.AuctionTimer = publicWidget.Widget.extend({
    selector: "#auction-timer",
    
    start: function () {
        this._updateTimer();
        this.timer = setInterval(this._updateTimer.bind(this), 1000);
    },

    _updateTimer: function () {
        let auctionTimer = this.$el;
        let auctionEndTime = auctionTimer.data("auction-end-time");

        if(!auctionEndTime) {
            auctionTimer.text("Auction Ended");
            return;
        }
        
        let utcEndTime = new Date(auctionEndTime);
        let localEndTime = new Date(utcEndTime.getTime() - (utcEndTime.getTimezoneOffset() * 1000 * 60 ));

        let now = new Date().getTime();
        let timeLeft = localEndTime - now;

        if(timeLeft > 0) {
            let days = Math.floor(timeLeft / (1000*60*60*24));
            let hours = Math.floor((timeLeft / (1000*60*60)) % 24);
            let minutes = Math.floor((timeLeft / (1000 * 60)) % 60);
            let seconds = Math.floor((timeLeft / 1000) % 60);

            auctionTimer.text(
                String(days).padStart(2, '0') + "d " +
                String(hours).padStart(2, '0') + "h " +
                String(minutes).padStart(2, '0') + "m " +
                String(seconds).padStart(2, '0') + "s"
            );
        }
        else {
            auctionTimer.text("Auction Ended");
            clearInterval(this.timer);
        }
    }
});
