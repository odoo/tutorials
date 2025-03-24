import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.AuctionTimer = publicWidget.Widget.extend({
    selector: '#remaining_auction_time',
    start: function () {
        let auctionEndTimeElement = document.getElementById("auction_end_time");
        let auctionEndTime = auctionEndTimeElement.innerText.trim();
        let countdownDate = Date.parse(auctionEndTime);

        let x = setInterval(function () {
            let now = new Date().getTime();
            let distance = countdownDate - now;

            if (distance > 0) {
                let days = Math.floor(distance / (1000 * 60 * 60 * 24));
                let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                let seconds = Math.floor((distance % (1000 * 60)) / 1000);
                document.getElementById("remaining_auction_time").innerHTML =
                    `${days.toString().padStart(2, '0')} : ${hours.toString().padStart(2, '0')} : ${minutes.toString().padStart(2, '0')} : ${seconds.toString().padStart(2, '0')}`;
            } else {
                clearInterval(x);
                document.getElementById("remaining_auction_time").innerHTML = "Auction Time Ended";
            }
        }, 1000);
    },
});
