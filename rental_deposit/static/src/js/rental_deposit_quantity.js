import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.WebsiteSale.include({
    _onChangeCombination(ev, $parent, combination) {
        let qtyDisplay = this.$el.find("#add_qty");
        let depositAmount = qtyDisplay.data("deposit");
        let totalDeposit = combination.add_qty * depositAmount;
        qtyDisplay.text(totalDeposit.toFixed(2));
    },
});
