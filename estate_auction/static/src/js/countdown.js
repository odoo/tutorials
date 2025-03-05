odoo.define('estate_auction.countdown', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var moment = require('moment'); // Import moment
    var odoo = window.odoo; // Declare odoo

    publicWidget.registry.CountdownTimer = publicWidget.Widget.extend({
        selector: '.countdown-timer',
        
        start: function () {
            var self = this;
            var endTimeStr = this.$el.data('end-time');
            
            if (!endTimeStr) {
                this.$el.html('<span class="text-danger">End time not set</span>');
                return;
            }
            
            // Parse the end time
            var endTime = moment(endTimeStr);
            
            // Update the countdown every second
            this.interval = setInterval(function() {
                self._updateCountdown(endTime);
            }, 1000);
            
            // Initial update
            this._updateCountdown(endTime);
            
            return this._super.apply(this, arguments);
        },
        
        destroy: function () {
            if (this.interval) {
                clearInterval(this.interval);
            }
            this._super.apply(this, arguments);
        },
        
        _updateCountdown: function (endTime) {
            var now = moment();
            var diff = endTime.diff(now);
            
            if (diff <= 0) {
                // Auction has ended
                this.$el.html('<span class="badge bg-danger p-2">Auction Ended</span>');
                clearInterval(this.interval);
                return;
            }
            
            // Calculate remaining time
            var duration = moment.duration(diff);
            var days = Math.floor(duration.asDays());
            var hours = duration.hours();
            var minutes = duration.minutes();
            var seconds = duration.seconds();
            
            // Format the display
            var html = '<div class="d-flex justify-content-center">';
            
            if (days > 0) {
                html += '<div class="text-center mx-2"><span class="display-6">' + days + '</span><br><small>Days</small></div>';
            }
            
            html += '<div class="text-center mx-2"><span class="display-6">' + this._padZero(hours) + '</span><br><small>Hours</small></div>';
            html += '<div class="text-center mx-2"><span class="display-6">' + this._padZero(minutes) + '</span><br><small>Minutes</small></div>';
            html += '<div class="text-center mx-2"><span class="display-6">' + this._padZero(seconds) + '</span><br><small>Seconds</small></div>';
            html += '</div>';
            
            this.$el.html(html);
        },
        
        _padZero: function (num) {
            return (num < 10 ? '0' : '') + num;
        }
    });
});
