import { useRef, useEffect } from "@odoo/owl";

export function useAutofocus(name) {
	const elementRef = useRef(name);
	useEffect(
		() => {
			if (elementRef.el) elementRef.el.focus();
		},
		() => []
	);
}
