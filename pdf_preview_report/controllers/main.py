# -*- coding: utf-8 -*-
import json
import datetime
from odoo import http, fields
from odoo.http import request, route
from odoo.tools import format_datetime

class AccountReportPreviewController(http.Controller):

    @route('/account_reports/preview/<int:report_id>', type='http', auth='user', methods=['GET'])
    def preview_report(self, report_id, options=None, **kwargs):
        """Render the exact same QWeb HTML that wkhtmltopdf would receive for PDF export."""
        uid = request.env.uid
        options = json.loads(options) if options else {}

        allowed_company_ids = request.env['account.report'].get_report_company_ids(options)
        if not allowed_company_ids:
            company_str = request.cookies.get('cids', str(request.env.user.company_id.id))
            allowed_company_ids = [int(str_id) for str_id in company_str.split('-')]

        report = request.env['account.report'].with_user(uid).with_context(
            allowed_company_ids=allowed_company_ids,
        ).browse(report_id)

        base_url = (
            request.env['ir.config_parameter'].sudo().get_str('report.url')
            or request.env['ir.config_parameter'].sudo().get_str('web.base.url')
        )

        print_options = report.get_options(previous_options={**options, 'export_mode': 'print'})

        custom_handler_model = report._get_custom_handler_model()
        handler = request.env[custom_handler_model] if (
            custom_handler_model and hasattr(request.env[custom_handler_model], '_get_pdf_export_html')
        ) else report

        html_content = handler._get_pdf_export_html(
            print_options,
            report._filter_out_folded_children(report._get_lines(print_options)),
            additional_context={'base_url': base_url},
        )

        is_landscape = len(print_options.get('columns', [])) > 5 or print_options.get('horizontal_split') or print_options.get('force_landscape_printing')
        target_width = 990 if is_landscape else 765
        target_height = 765 if is_landscape else 990
        target_zoom = 1.0
        is_landscape_js = "true" if is_landscape else "false"

        # Timezone-aware date and time formatting matching Odoo's report layout
        local_dt = fields.Datetime.context_timestamp(request.env.user, fields.Datetime.now())
        current_time = local_dt.strftime('%Y-%m-%d %H:%M')
        company_name = request.env.company.name
        company_name_js = company_name.replace("'", "\\'")
        current_time_js = current_time

        style_inject = f"""
<style>
    body {{
        background-color: #525659 !important;
        margin: 0 !important;
        padding: 20px 0 !important;
    }}
    .o_content {{
        zoom: {target_zoom};
        width: {target_width}px;
        background-color: #ffffff !important;
        color: #212529 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35) !important;
        padding: 20px !important;
        margin: 0 auto !important;
        box-sizing: border-box !important;
        border: 1px solid #d3d3d3 !important;
        position: relative !important;
        font-family: "Times New Roman", Times, Georgia, serif !important;
    }}
    .o_content .o_table, .o_content .o_table * {{
        font-family: 'Verdana', sans-serif !important;
    }}
    .o_table {{
        width: 100% !important;
    }}
    .o_preview_repeated_header {{
        white-space: nowrap !important;
    }}
    .o_preview_header_row_last {{
        border-bottom: 2px solid #dee2e6 !important;
    }}
    .o_preview_repeated_header th, .o_preview_repeated_header td {{
        border-style: none !important;
        font-weight: bold !important;
    }}
    .o_preview_header_row_not_last th:not(:first-child), .o_preview_header_row_not_last td:not(:first-child) {{
        background-color: #e7e9ed !important;
        text-align: center !important;
    }}
</style>
"""
        script_inject = f"""
<script>
    (function() {{
        function handleEvents() {{
            const content = document.querySelector(".o_content");
            if (content) {{
                // 1. Reset zoom and styling to natural unzoomed state to measure widths
                content.style.zoom = "1";
                content.style.width = "auto";
                content.style.height = "auto";
                document.querySelectorAll(".o_preview_page_spacer, .o_preview_page_break, .o_preview_footer, .o_preview_repeated_header").forEach(el => el.remove());
                
                // Force synchronous layout reflow
                content.offsetHeight;
                
                // 2. Measure natural table/content width
                const table = document.querySelector(".o_table");
                const naturalTableWidth = table ? table.scrollWidth : 0;
                
                const isLandscape = {is_landscape_js};
                const baseTargetWidth = isLandscape ? 990 : 765;
                
                // The page sheet width is the maximum of the base US Letter width and the table width (plus padding)
                const padding = 80;
                const pageWidth = Math.max(baseTargetWidth, naturalTableWidth + padding);
                
                // Calculate targetHeight based on US Letter aspect ratio (792/612 = 1.2941)
                const targetHeight = isLandscape 
                    ? Math.round(pageWidth * 612 / 792) 
                    : Math.round(pageWidth * 792 / 612);
                
                // Set the fixed width on the page sheet container
                content.style.width = pageWidth + "px";
                
                // 3. Find table rows and insert spacers at page boundaries (at unzoomed coordinates)
                if (table) {{
                    const rows = Array.from(table.querySelectorAll("tbody tr"));
                    const thead = table.querySelector("thead");
                    const headerRows = thead ? Array.from(thead.querySelectorAll("tr")) : [];
                    let currentBoundary = targetHeight;
                    
                    for (let i = 0; i < rows.length; i++) {{
                        const row = rows[i];
                        if (row.classList.contains("o_preview_page_spacer") || row.classList.contains("o_preview_repeated_header")) continue;
                        
                        const contentRect = content.getBoundingClientRect();
                        const rowRect = row.getBoundingClientRect();
                        const rowTop = rowRect.top - contentRect.top;
                        const rowBottom = rowRect.bottom - contentRect.top;
                        
                        // If the row bottom crosses into the bottom page margin / footer zone (80px before boundary)
                        if (rowBottom > currentBoundary - 80) {{
                            const pushDistance = (currentBoundary + 50) - rowTop;
                            if (pushDistance > 0) {{
                                const spacer = document.createElement("tr");
                                spacer.className = "o_preview_page_spacer";
                                spacer.innerHTML = `<td colspan="100" style="height: ${{pushDistance}}px; padding: 0 !important; border: none !important; background: transparent !important;"></td>`;
                                row.parentNode.insertBefore(spacer, row);
                                
                                // Insert cloned header rows right after the spacer
                                headerRows.forEach((headerRow, index) => {{
                                     const clonedRow = headerRow.cloneNode(true);
                                     clonedRow.classList.add("o_preview_repeated_header");
                                     if (index === headerRows.length - 1) {{
                                         clonedRow.classList.add("o_preview_header_row_last");
                                     }} else {{
                                         clonedRow.classList.add("o_preview_header_row_not_last");
                                     }}
                                     row.parentNode.insertBefore(clonedRow, row);
                                 }});
                                
                                // Force layout update
                                content.offsetHeight;
                            }}
                            currentBoundary += targetHeight;
                        }}
                    }}
                }}
                
                // 4. Calculate total pages
                const naturalHeight = content.scrollHeight;
                const pagesCount = Math.max(1, Math.ceil(naturalHeight / targetHeight));
                content.style.height = (pagesCount * targetHeight) + "px";
                
                // 5. Draw dynamic page footers and page break lines
                const currentTime = "{current_time_js}";
                const companyName = "{company_name_js}";
                
                for (let i = 1; i <= pagesCount; i++) {{
                    // Add footer absolutely positioned at the bottom of page i
                    const footerEl = document.createElement("div");
                    footerEl.className = "o_preview_footer";
                    footerEl.style.cssText = "font-family: sans-serif;position: absolute; left: 40px; right: 40px; height: 30px; line-height: 30px; padding-top: 10px; font-size: 11px; color: #6c757d; z-index: 1000;";
                    footerEl.style.top = (i * targetHeight - 50) + "px";
                    
                    footerEl.innerHTML = `
                        <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
                            <div style="text-align: left; width: 33.33%;">${{currentTime}}</div>
                            <div style="text-align: center; width: 33.33%; font-weight: bold;">${{companyName}}</div>
                            <div style="text-align: right; width: 33.33%;">${{i}} / ${{pagesCount}}</div>
                        </div>
                    `;
                    content.appendChild(footerEl);
                    
                    // Add physical page gap separation (except for the last page)
                    if (i < pagesCount) {{
                        const breakEl = document.createElement("div");
                        breakEl.className = "o_preview_page_break";
                        breakEl.style.cssText = "position: absolute; left: -1px; right: -1px; height: 24px; background-color: #525659; border-top: 1px solid #d3d3d3; border-bottom: 1px solid #d3d3d3; box-shadow: inset 0 3px 5px rgba(0,0,0,0.15), inset 0 -3px 5px rgba(0,0,0,0.15); z-index: 1000;";
                        breakEl.style.top = (i * targetHeight - 12) + "px";
                        content.appendChild(breakEl);
                    }}
                }}
                
                // 6. Calculate fit zoom based on iframe viewport width
                const iframeWidth = window.innerWidth || document.documentElement.clientWidth;
                const baseZoom = isLandscape ? 0.75 : 0.95;
                const fitZoom = Math.min(baseZoom, (iframeWidth - 40) / pageWidth);
                
                const userZoom = window.pdfPreviewZoom || 1.0;
                content.style.zoom = fitZoom * userZoom;
            }}
        }}

        window.handleEvents = handleEvents;
        window.addEventListener("load", handleEvents);
        window.addEventListener("resize", handleEvents);
        if (document.readyState === "complete" || document.readyState === "interactive") {{
            handleEvents();
        }} else {{
            document.addEventListener("DOMContentLoaded", handleEvents);
        }}
    }})();
</script>
"""
        if isinstance(html_content, bytes):
            html_content = html_content.decode('utf-8')
        else:
            html_content = str(html_content)

        # Inject styles in head
        head_close_idx = html_content.find('</head>')
        if head_close_idx != -1:
            html_content = html_content[:head_close_idx] + style_inject + html_content[head_close_idx:]

        # Inject adjustZoom scripts in body
        body_close_idx = html_content.find('</body>')
        if body_close_idx != -1:
            html_content = html_content[:body_close_idx] + script_inject + html_content[body_close_idx:]

        return request.make_response(html_content, headers=[
            ('Content-Type', 'text/html; charset=utf-8'),
        ])
