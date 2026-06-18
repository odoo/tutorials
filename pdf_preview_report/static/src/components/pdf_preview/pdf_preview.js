/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { Component, onMounted, onWillDestroy, useRef } from "@odoo/owl";
import { proxy } from "@odoo/owl";
import { AccountReportController } from "@account_reports/components/account_report/controller";

export class PdfPreviewDialog extends Component {
    static template = "pdf_preview_report.PdfPreviewDialog";
    static components = { Dialog };
    static props = {
        previewUrl: { type: String },
        onExportPdf: { type: Function },
        close: { type: Function },
    };

    setup() {
        this.state = proxy({
            loading: true,
            zoom: 1.0,
        });
        this.iframeRef = useRef("previewIframe");
        this._pollInterval = null;
        this.savedScrollTop = 0;
        this.savedScrollLeft = 0;
        this.savedScrollTopWindow = 0;
        this.savedScrollLeftWindow = 0;

        onMounted(() => {
            const frame = this.iframeRef.el;
            if (frame) {
                frame.addEventListener("load", () => {
                    this.state.loading = false;
                    this.updateIframeZoom();
                    try {
                        const contentWindow = frame.contentWindow;
                        if (contentWindow && contentWindow.document) {
                            const doc = contentWindow.document;
                            const oContent = doc.querySelector(".o_content");
                            if (oContent) {
                                oContent.scrollTop = this.savedScrollTop;
                                oContent.scrollLeft = this.savedScrollLeft;
                            }
                            contentWindow.scrollTo(this.savedScrollLeftWindow, this.savedScrollTopWindow);
                        }
                    } catch (e) {
                        // ignore
                    }
                });
            }

            // 1-second poller that reloads the iframe content smoothly via AJAX
            this._pollInterval = setInterval(async () => {
                const frame = this.iframeRef.el;
                if (frame && frame.contentWindow && frame.contentWindow.document) {
                    try {
                        const url = frame.src;
                        const response = await fetch(url);
                        if (!response.ok) return;
                        const html = await response.text();

                        const parser = new DOMParser();
                        const newDoc = parser.parseFromString(html, "text/html");

                        const currentDoc = frame.contentWindow.document;

                        // 1. Save scroll positions
                        const oContentCurrent = currentDoc.querySelector(".o_content");
                        const scrollTop = oContentCurrent ? oContentCurrent.scrollTop : 0;
                        const scrollLeft = oContentCurrent ? oContentCurrent.scrollLeft : 0;
                        const scrollTopWindow = frame.contentWindow.scrollY || currentDoc.documentElement.scrollTop || currentDoc.body.scrollTop || 0;
                        const scrollLeftWindow = frame.contentWindow.scrollX || currentDoc.documentElement.scrollLeft || currentDoc.body.scrollLeft || 0;

                        this.savedScrollTop = scrollTop;
                        this.savedScrollLeft = scrollLeft;
                        this.savedScrollTopWindow = scrollTopWindow;
                        this.savedScrollLeftWindow = scrollLeftWindow;

                        // Temporarily lock body height/width to prevent scroll clamping
                        const originalMinHeight = currentDoc.body.style.minHeight;
                        const originalMinWidth = currentDoc.body.style.minWidth;
                        const scrollHeight = currentDoc.documentElement.scrollHeight || currentDoc.body.scrollHeight;
                        const scrollWidth = currentDoc.documentElement.scrollWidth || currentDoc.body.scrollWidth;
                        currentDoc.body.style.minHeight = scrollHeight + "px";
                        currentDoc.body.style.minWidth = scrollWidth + "px";

                        // 2. Update styles/links in head
                        currentDoc.head.innerHTML = newDoc.head.innerHTML;

                        // 3. Update body content
                        currentDoc.body.innerHTML = newDoc.body.innerHTML;

                        // 4. Re-execute scripts to run adjustZoom script
                        const scripts = currentDoc.querySelectorAll("script");
                        scripts.forEach(oldScript => {
                            const newScript = currentDoc.createElement("script");
                            if (oldScript.src) {
                                newScript.src = oldScript.src;
                            } else {
                                newScript.textContent = oldScript.textContent;
                            }
                            oldScript.parentNode.replaceChild(newScript, oldScript);
                        });

                        // Re-apply zoom state onto the iframe window context
                        this.updateIframeZoom();

                        // 5. Restore scroll positions
                        const oContentNew = currentDoc.querySelector(".o_content");
                        if (oContentNew) {
                            oContentNew.scrollTop = scrollTop;
                            oContentNew.scrollLeft = scrollLeft;
                        }
                        frame.contentWindow.scrollTo(scrollLeftWindow, scrollTopWindow);

                        // Restore original min-height and min-width styles
                        currentDoc.body.style.minHeight = originalMinHeight;
                        currentDoc.body.style.minWidth = originalMinWidth;
                    } catch (e) {
                        frame.src = frame.src;
                    }
                }
            }, 1000);
        });

        onWillDestroy(() => {
            if (this._pollInterval) {
                clearInterval(this._pollInterval);
                this._pollInterval = null;
            }
        });
    }

    get zoomPercent() {
        return Math.round(this.state.zoom * 100);
    }

    updateIframeZoom() {
        const frame = this.iframeRef.el;
        if (frame && frame.contentWindow) {
            frame.contentWindow.pdfPreviewZoom = this.state.zoom;
            if (typeof frame.contentWindow.handleEvents === "function") {
                frame.contentWindow.handleEvents();
            }
        }
    }

    onZoomIn() {
        this.state.zoom = Math.min(3.0, this.state.zoom + 0.1);
        this.updateIframeZoom();
    }

    onZoomOut() {
        this.state.zoom = Math.max(0.5, this.state.zoom - 0.1);
        this.updateIframeZoom();
    }

    onZoomReset() {
        this.state.zoom = 1.0;
        this.updateIframeZoom();
    }

    onClose() {
        this.props.close();
    }

    async onExportPdf() {
        this.props.close();
        await this.props.onExportPdf();
    }
}

// Monkey-patch AccountReportController to intercept PDF export
const _originalButtonAction = AccountReportController.prototype.buttonAction;
AccountReportController.prototype.buttonAction = function (ev, button) {
    if (
        button.action_param === "export_to_pdf"
        && this.options
        && this.options.preview_before_export
    ) {
        if (ev) {
            ev.preventDefault();
            ev.stopPropagation();
        }

        const options = this.cachedFilterOptions;
        const reportId = options.report_id;
        const optionsJson = encodeURIComponent(JSON.stringify(options));
        const previewUrl = `/account_reports/preview/${reportId}?options=${optionsJson}`;

        this.dialog.add(PdfPreviewDialog, {
            previewUrl,
            onExportPdf: async () => {
                await this.reportAction(null, button.action, button.action_param, true);
            },
        });
        return;
    }
    return _originalButtonAction.call(this, ev, button);
};
