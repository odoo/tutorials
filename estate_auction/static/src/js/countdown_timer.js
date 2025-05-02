import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.AuctionCountdownTimer = publicWidget.Widget.extend({
    selector: '#countdown_timer',
    start: function () {
        const countdown = document.getElementById('countdown_timer');
        const displaySpan = document.getElementById('auction_end_time');
        const endTimeStr = countdown.getAttribute('data-end-time');

        if (!endTimeStr) {
            countdown.textContent = 'End time not specified.';
            return;
        }

        const endTime = new Date(endTimeStr + 'Z').getTime();
        if (isNaN(endTime)) {
            countdown.textContent = 'Invalid end time format.';
            displaySpan.textContent = 'Invalid date';
            return;
        }

        this.interval = setInterval(function () {
            const now = new Date().getTime();
            const difference = endTime - now;

            if (difference <= 0) {
                clearInterval(self.interval);
                countdown.textContent = 'Auction Ended';
                document.getElementById('offer_modal_button').hidden = true;
                return;
            }

            const days = Math.floor(difference / 86400000);
            const hrs = Math.floor((difference % 86400000) / 3600000);
            const mins = Math.floor((difference % 3600000) / 60000);
            const secs = Math.floor((difference % 60000) / 1000);

            countdown.textContent = (
                (days > 0 ? days + 'd ' : '') +
                (hrs < 10 ? '0' : '') + hrs + 'h ' +
                (mins < 10 ? '0' : '') + mins + 'm ' +
                (secs < 10 ? '0' : '') + secs + 's'
            );
        }, 1000);
    },

    destroy: function () {
        clearInterval(this.interval);
    }
});
