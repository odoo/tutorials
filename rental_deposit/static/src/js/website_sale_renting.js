import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.WebsiteSale.include({
    _onChangeCombination(ev, $parent, combination) {
        this._super.apply(this, arguments);
        $parent.find("#calculated_deposit").text(this._priceToStr(combination.deposit_total || 0));
    },
});
