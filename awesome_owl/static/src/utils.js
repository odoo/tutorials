import {onMounted, useRef} from "@odoo/owl";

export function useAutoFocus(name) {
    const input = useRef(name);

    onMounted(() => {
        input.el.focus();
    });
}
