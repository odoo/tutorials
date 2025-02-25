import publicWidget from '@web/legacy/js/public/public_widget';


publicWidget.registry.WebsiteSale.include({
    _onChangeCombination(ev, $parent, combination) {
        const res = this._super.apply(this, arguments);
        const $calculatedAmount = $parent.find("#calculated_amount");
        if ($calculatedAmount.length && combination.calculated_amount !== undefined) {
            $calculatedAmount.text(this._priceToStr(combination.calculated_amount));
        }
        return res;
    },
});
