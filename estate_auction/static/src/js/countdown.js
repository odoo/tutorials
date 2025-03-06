/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CountdownTimer = publicWidget.Widget.extend({
    selector: '#countdown',
    start: function () {
        let countdownDate;

        let auctionEndTime = document.getElementById("auction_end_time").innerText;
        countdownDate = new Date(new Date(auctionEndTime).getTime() - new Date(auctionEndTime).getTimezoneOffset() * 60000).getTime();

        let x = setInterval(function () {
            let now = new Date().getTime();
            let distance = countdownDate - now;

            let days = Math.floor(distance / (1000 * 60 * 60 * 24));
            let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((distance % (1000 * 60)) / 1000);

            if (distance) document.getElementById("countdown").innerHTML =
                days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

            if (distance < 0) {
                clearInterval(x);
                document.getElementById("countdown").innerHTML = "Auction Time Ended";
            }
        }, 1000);
    },
});
