/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CountdownTimer = publicWidget.Widget.extend({
    selector: '.countdown-timer',

    start: function () {
        const self = this;
        const endTimeStr = this.$el.data('end-time');

        if (!endTimeStr) {
            this.$el.html('<span class="text-danger">End time not set</span>');
            return this._super.apply(this, arguments);
        }

        const endTime = new Date(endTimeStr).getTime();

        this.interval = setInterval(function () {
            self._updateCountdown(endTime);
        }, 1000);

        this._updateCountdown(endTime);

        return this._super.apply(this, arguments);
    },

    destroy: function () {
        if (this.interval) {
            clearInterval(this.interval);
        }
        return this._super.apply(this, arguments);
    },

    _updateCountdown: function (endTime) {
        const now = Date.now();
        const diff = endTime - now;

        if (diff <= 0) {
            this.$el.html('<span class="badge bg-danger p-2">Auction Ended</span>');
            clearInterval(this.interval);
            return;
        }

        let seconds = Math.floor(diff / 1000);
        let minutes = Math.floor(seconds / 60);
        let hours = Math.floor(minutes / 60);
        let days = Math.floor(hours / 24);

        hours %= 24;
        minutes %= 60;
        seconds %= 60;

        let html = '<div class="d-flex justify-content-center">';

        if (days > 0) {
            html += `<div class="text-center mx-2"><span class="display-6">${days}</span><br><small>Days</small></div>`;
        }

        html += `<div class="text-center mx-2"><span class="display-6">${this._padZero(hours)}</span><br><small>Hours</small></div>`;
        html += `<div class="text-center mx-2"><span class="display-6">${this._padZero(minutes)}</span><br><small>Minutes</small></div>`;
        html += `<div class="text-center mx-2"><span class="display-6">${this._padZero(seconds)}</span><br><small>Seconds</small></div>`;
        html += '</div>';

        this.$el.html(html);
    },

    _padZero: function (num) {
        return (num < 10 ? '0' : '') + num;
    },
});

export default publicWidget.registry.CountdownTimer;
