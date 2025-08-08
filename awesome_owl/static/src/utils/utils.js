import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(input) {
    const inputRef = useRef(input);

    onMounted(() => {
        if (inputRef.el) {
            inputRef.el.focus();
        }
    });

    return { inputRef };
}
