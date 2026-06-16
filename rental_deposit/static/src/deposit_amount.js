import { Component, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class DepositAmount extends Component {
    setup() {
        onMounted(() => {
            const depositEl = document.querySelector('#deposit_amount_val');
            const qtyInput = document.querySelector('input[name="add_qty"]');

            if (!depositEl || !qtyInput) return;

            const baseAmount = parseFloat(depositEl.dataset.baseAmount) || 0;

            const calculateTotal = () => {
                const quantity = parseFloat(qtyInput.value) || 1;
                depositEl.textContent = (baseAmount * quantity).toFixed(2);
            };

            qtyInput.addEventListener('input', calculateTotal);
            qtyInput.addEventListener('change', calculateTotal);

            calculateTotal();
        });
    }
}

registry.category("public_components").add("deposit_amount", DepositAmount);
