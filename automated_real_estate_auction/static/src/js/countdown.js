import publicWidget from "@web/legacy/js/public/public_widget"

publicWidget.registry.AuctionTimer = publicWidget.Widget.extend({
    selector: '#remaining_auction_time',
    start: function () {
        let countdownDate;

        let auctionEndTime = document.getElementById("auction_end_time").innerText;
        countdownDate = new Date(auctionEndTime).getTime();

        let x = setInterval(function () {
            let now = new Date().getTime();
            let distance = countdownDate - now;

            let days = Math.floor(distance / (1000 * 60 * 60 * 24));
            let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((distance % (1000 * 60)) / 1000);

            if (distance) document.getElementById("remaining_auction_time").innerHTML =
                days + " : " + hours + " : " + minutes + " : " + seconds + " ";
            if (distance < 0) {
                clearInterval(x);
                document.getElementById("remaining_auction_time").innerHTML = "Auction Time Ended";
            }
        }, 1000);
    },
});
