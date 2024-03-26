/** @odoo-module **/
import { onMounted, useRef } from "@odoo/owl";

export function useAutoFocus(ref) {
	let to_focus = useRef(ref);
	onMounted( () => {
		to_focus.el.focus();
	});
	return ;
}

