/** @odoo-module **/

import options from '@web_editor/js/editor/snippets.options';

options.registry.HelpdeskTickets = options.Class.extend({
    
    selectDataAttribute(previewMode, widgetValue, params) {
        this.$target[0].setAttribute("data-helpdesk-team-id", widgetValue) || '';
    },

    selectLayout(previewMode, widgetValue, params) {

        this.$target[0].setAttribute("data-layout", widgetValue);
    },
    //----------------------------------------------------------------------
    // Private methods
    //----------------------------------------------------------------------
    
    /**
     * @override
    */

    _computeWidgetState(methodName, params) {
        if (methodName === 'selectDataAttribute') {
                return this.$target[0].getAttribute("data-helpdesk-team-id") || '';
            }

        if (methodName === 'selectLayout') {
                return this.$target[0].getAttribute("data-layout");
        }
            return this._super(...arguments);
        },

});

