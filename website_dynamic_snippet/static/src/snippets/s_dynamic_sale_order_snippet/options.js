import options from "@web_editor/js/editor/snippets.options";

options.registry.DynamicSnippetOptions = options.Class.extend({
    confirmOrderOnly(previewMode, widgetValue, params) {
        const confirmOrderOnly = widgetValue;
        this.$target[0].attr("data-confirm-order-only", widgetValue);
    },

    setLayout(previewMode, widgetValue, params) {
        const snippetList = this.$target[0].querySelector(".list_sale_order");
        const snippetCard = this.$target[0].querySelector(".card_sale_order");
        if (widgetValue && widgetValue === "list") {
            snippetList.classList.remove("d-none");
            snippetCard.classList.add("d-none");
        } else if (widgetValue && widgetValue === "grid") {
            snippetList.classList.add("d-none");
            snippetCard.classList.remove("d-none");
        } else {
            snippetList.classList.remove("d-none");
            snippetCard.classList.add("d-none");
        }
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    _computeWidgetState(methodName, widgetName, params, widgetValue) {
        if (methodName === "confirmOrderOnly") {
            return this.$target[0].dataset.isConfirmOrder === 'true' || this.$target[0].dataset.isConfirmOrder === true;
        }
        if (methodName === "setLayout") {
            return this.$target[0].querySelector(".list_sale_order").classList.contains('d-none') ? "grid" : "list";
        }
        return this._super(...arguments);
    },
});
