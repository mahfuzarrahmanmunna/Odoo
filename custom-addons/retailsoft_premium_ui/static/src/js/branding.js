/** @odoo-module **/
const brandIcon = '/retailsoft_premium_ui/static/src/img/system.svg';
function brandText(value) { return value.replace(/\bOdoo\b/gi, 'System'); }
function applyBrand() {
    if (document.title !== brandText(document.title)) document.title = brandText(document.title);
    let links = document.querySelectorAll('link[rel~="icon"], link[rel="shortcut icon"]');
    if (!links.length) { const link = document.createElement('link'); link.rel = 'icon'; document.head.append(link); links = [link]; }
    for (const link of links) if (link.getAttribute('href') !== brandIcon) link.setAttribute('href', brandIcon);
    // Only known chrome and branding surfaces; never rewrite business records or inputs.
    const selectors = '.o_main_navbar, .o_user_menu .dropdown-menu, .o_menu_systray .dropdown-menu, .oe_login_form, .o_database_list, .o_footer_copyright, .o_settings_container .o_setting_box';
    for (const node of document.querySelectorAll(selectors)) {
        const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
        while (walker.nextNode()) {
            const t = walker.currentNode;
            if (t.parentElement?.closest('script,style,textarea,input,[contenteditable],pre,code')) continue;
            if (/copyright|licen[cs]e|©/i.test(t.nodeValue)) continue;
            const value = brandText(t.nodeValue);
            if (value !== t.nodeValue) t.nodeValue = value;
        }
    }
    for (const a of document.querySelectorAll('a[href*="odoo.com"]')) {
        if (/^\s*Powered by Odoo\s*$/i.test(a.textContent)) a.textContent = 'Powered by System';
    }
    for (const img of document.querySelectorAll('.oe_login_form img, .o_database_list img, .o_main_navbar img, .card img')) {
        if (/\/web\/static\/img\/odoo_logo[^/]*\.(svg|png)/i.test(img.getAttribute('src') || '')) { img.src = brandIcon; img.alt = 'System'; }
    }
}
let pending = false;
function schedule() { if (!pending) { pending = true; requestAnimationFrame(() => { pending = false; applyBrand(); }); } }
function start() { applyBrand(); new MutationObserver(schedule).observe(document.documentElement,{childList:true,subtree:true,characterData:true}); }
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded',start,{once:true}); else start();
