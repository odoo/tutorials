document.addEventListener('change', function (event) {
    const input = event.target;
    if (!input.matches('input[name="add_qty"]')) {
        return;
    }
    const productEl = input.closest('.js_product');
    const depositEl = productEl?.querySelector('.deposit_div');
    if (!depositEl) {
        return;
    }
    const unit_deposit_price = parseFloat(depositEl.dataset.depositUnit) || 0;
    const quantity = parseFloat(input.value) || 0;
    const total = (unit_deposit_price * quantity).toFixed(2);
    const target = depositEl.querySelector('.deposit_value');
    if (target) {
        target.textContent = total;
    }
});
