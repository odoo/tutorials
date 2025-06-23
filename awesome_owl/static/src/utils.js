import { useRef, onMounted } from "@odoo/owl";

// Hook to auto-focus an element when mounted
export function useAutofocus(refName) {
    const ref = useRef(refName);
    onMounted(() => {
        ref.el.focus();
    });
}
