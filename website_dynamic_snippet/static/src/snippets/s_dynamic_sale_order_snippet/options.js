import options from "@web_editor/js/editor/snippets.options";

options.registry.DynamicSnippetOptions = options.Class.extend({
    confirmOrderOnly(previewMode, widgetValue) {
        this.$target[0].dataset.confirmOrderOnly = widgetValue;
    },

    setLayout(previewMode, widgetValue) {
        this.$target[0].setAttribute("data-set-layout", widgetValue);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    _computeWidgetState(methodName, params) {
        if (methodName === "confirmOrderOnly") {
            return this.$target[0].dataset.confirmOrderOnly;
        }
        if (methodName === "setLayout") {
            return this.$target[0].getAttribute("data-set-layout");
        }
        return this._super(...arguments);
    },
});
