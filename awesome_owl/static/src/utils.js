import { onMounted, useRef } from '@odoo/owl'

export function useAutoFocus(refName) {
    const inputRef = useRef(refName);

    onMounted(() => {
        inputRef.el.focus();
    });
}
