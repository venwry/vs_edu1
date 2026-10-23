/* Shared catalogue membership for Navigator and domain-page deduplication. */
(function(root){
const sections=['base_parts','devices','computers','software_products','platform_editions','external_partner_products','offered_bundles','proposed_bundles','commercial_offerings'];
const pages=['operating-systems','business-software','bpi','software-development','flexibus','video-system','networking','academy','peripherals'];
const ids=catalog=>new Set(sections.flatMap(k=>(catalog[k]||[]).map(r=>r.id)));
root.CatalogNavigation={sections,pages,ids,url:id=>'bom-navigator.html?element='+encodeURIComponent(id)};
})(typeof window==='undefined'?globalThis:window);
