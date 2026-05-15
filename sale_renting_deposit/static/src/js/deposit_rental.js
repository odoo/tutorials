document.addEventListener('change', function (ev) {
    const input = ev.target;
    if (!input.matches('.js_main_product input[name="add_qty"]')) {
        return;
    }
    const productEl = input.closest('.js_product');
    const depositEl = productEl?.querySelector('.o_deposit_wrapper');
    if (!depositEl) {
        return;
    }
    const depositUnit = parseFloat(depositEl.dataset.depositUnit) || 0;
    const quantity = parseFloat(input.value) || 0;
    const total = (depositUnit * quantity).toFixed(2);
    const target = depositEl.querySelector('.o_deposit_amount_value');
    if (target) {
        target.textContent = total;
    }
});
