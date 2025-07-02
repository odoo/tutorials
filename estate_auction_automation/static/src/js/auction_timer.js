import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.AuctionTimer = publicWidget.Widget.extend({
    selector: "#auction_timer",
    
    start: function () {
        let auctionTimerElement = this.$el[0];
        let endTimeUTCString = auctionTimerElement.getAttribute("data-end-time");

        if (!endTimeUTCString) {
            return;
        }

        let endTimeUTC = new Date(endTimeUTCString.replace(" ", "T") + "Z").getTime();
        let offerButton = document.getElementById("create_offer_button");

        function updateCountdown() {
            let nowUTC = new Date().getTime();
            let timeRemaining = endTimeUTC - nowUTC;

            if (timeRemaining <= 0) {
                auctionTimerElement.innerText = "Auction Ended";
                clearInterval(countdownInterval);

                if (offerButton) {
                    offerButton.style.display = "none";
                }                
                return;
            }

            let days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
            let hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

            auctionTimerElement.innerText = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        }

        let countdownInterval = setInterval(updateCountdown, 1000);
        updateCountdown();
    }
});
