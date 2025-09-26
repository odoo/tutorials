import { WebsiteSale } from '@website_sale/js/website_sale';


const oldOnChangeCombination = WebsiteSale.prototype._onChangeCombination;

WebsiteSale.include({
    _onChangeCombination(ev, $parent, combination) {
        oldOnChangeCombination.call(this, ev, $parent, combination);
        
        
        if (combination && combination.amount !== undefined) {
            const $amount = $parent.find("#total_amount");
            const quantity = parseFloat($parent.find("input[name='add_qty']").val()) || 1;
            console.log("amount and quantity", $amount, quantity);
            $amount.text(this._priceToStr(combination.amount * quantity));
            console.log("combitnation", combination, $amount.text());
        }
    },
});