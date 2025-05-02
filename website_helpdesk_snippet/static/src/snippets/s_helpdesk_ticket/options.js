/** @odoo-module **/

import options from '@web_editor/js/editor/snippets.options';

options.registry.HelpdeskTickets = options.Class.extend({
    
    setHelpdeskTeamId(previewMode, widgetValue, params) {
        const teamId = widgetValue 
        this.$target.attr('data-helpdesk-team-id', teamId? teamId : 'all');  

    },
    //----------------------------------------------------------------------
    // Private methods
    //----------------------------------------------------------------------
    
    /**
     * @override
    */
    _computeWidgetState(methodName, params) {
        if (methodName === 'setHelpdeskTeamId') {
                return this.$target[0].dataset.helpdeskTeamId || 'all';
            }
            return this._super(...arguments);
        },

});

