import publicWidget from "@web/legacy/js/public/public_widget";


publicWidget.registry.WebsiteSale.include({
    _onChangeCombination(ev, $parent, combination) {
        const res = this._super.apply(this, arguments);
        this._updateDepositAmount($parent, combination);
        return res;
    },

    _updateDepositAmount($parent, combination) {
        const depositAmount = combination.deposit_amount ? parseFloat(combination.deposit_amount) : 0;
        const $depositSpan = $parent.find("#deposit_amount");
        const $quantityInput = $parent.find("input[name='add_qty']");

        if (!$depositSpan.length || !$quantityInput.length) {
            console.warn("Deposit span or quantity input not found!");
            return;
        }

        const baseDeposit = depositAmount || parseFloat($depositSpan.attr("data-deposit-amount")) || 0;

        const updateDeposit = () => {
            const quantity = parseFloat($quantityInput.val()) || 1;
            const totalDeposit = baseDeposit * quantity;
            $depositSpan.text(this._priceToStr(totalDeposit));
        };
        $quantityInput.off("change keyup").on("change keyup", updateDeposit);
        updateDeposit();
    },
});
