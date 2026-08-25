import { useRef, onMounted } from "@odoo/owl";

/**
 * Custom hook to autofocus an element on mounted
 * 
 * @param {String} ref name that will be used for the element
 * @returns the reference created for the element
 */
export function useAutoFocus(ref) {
    const inputRef = useRef(ref)

    onMounted(() => {
        inputRef.el?.focus();
    })

    return inputRef;
}
