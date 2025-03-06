import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteSale.include({
    _onChangeCombination(ev, $parent, combination) {
        if (combination && combination.amount !== undefined) {
            const $amount = $parent.find("#total_amount");
            const quantity = parseFloat($parent.find("input[name='add_qty']").val()) || 1;
            $amount.text(this._priceToStr(combination.amount * quantity));
        }
    },
});
