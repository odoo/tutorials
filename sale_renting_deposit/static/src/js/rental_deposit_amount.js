/** @odoo-module  **/

import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.WebsiteSale.include({
    _onChangeCombination(ev, $parent, combination) {
        const res = this._super.apply(this, arguments);
        const $total_deposit_amount = $parent.find("#total_deposit_amount");
        $total_deposit_amount.text(this._priceToStr(combination.total_deposit_amount));
        return res;
    },
});
