/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';

const MouseFollower = publicWidget.Widget.extend({
    selector: '#wrapwrap',
    events: { 'mousemove': '_onMouseMove' },

    _onMouseMove: function(ev) {
        this.mouseX = ev.clientX;
        this.mouseY = ev.clientY;

        setInterval(() => {
            this.xp += this.mouseX - this.xp;
            this.yp += this.mouseY - this.yp;

            this.follower.setAttribute('style', `top: ${this.yp}px; left: ${this.xp}px;`);
        }, 400);
    },
    start: function() {
        // Initialize starting position
        this.xp = 0;
        this.yp = 0;

        // Create the Follower
        this.follower = document.createElement('div');
        this.follower.setAttribute('class', 'x_mouse_follower o_not_editable position-fixed rounded-circle bg-o-color-1 opacity-50 translate-middle pe-none');
        this.el.querySelector('#top + main').append(this.follower);

        return this._super(...arguments);
    },

    destroy: function() {
        this.el.querySelector('.x_mouse_follower').remove();

        return this._super(...arguments);
    }
});

publicWidget.registry.MouseFollower = MouseFollower;
export default MouseFollower;
