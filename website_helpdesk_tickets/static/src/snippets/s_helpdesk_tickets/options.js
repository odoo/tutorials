/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";

options.registry.HelpdeskTickets = options.Class.extend({

  //----------------------------------------------------------------------
  // Private methods
  //----------------------------------------------------------------------

  /**
   * @override
   */
  _computeWidgetState(methodName, params) {
      if (methodName === "setHelpdeskTeamId") {
          return this.$target[0].dataset.helpdeskTeamId || "";
        }
      if (methodName === "setLayout") {
        return this.$target[0].dataset.layout || "card";
      }
        return this._super(...arguments);
    },
});
