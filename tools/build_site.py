"""Build common navigation, content placement and legacy redirects from site config.
Run after catalogue assembly and after any financial HTML builder.
"""
from pathlib import Path
import json,re,html
ROOT=Path(__file__).resolve().parents[1]
def build():
 site=json.loads((ROOT/'generated/catalogs/site-pages.json').read_text());pages={p['id']:p for p in site['pages']};esc=html.escape
 labels={'timeline':'Timeline','ecosystem':'3rd Party','operating-systems':'OS','business-software':'Business','software-development':'Dev','video-system':'Video','peripherals':'Peripherals','aurelia':'Aurelia','artemis':'Artemis','athena':'Athena','bpi':'BPI','flexibus':'FlexiBUS','networking':'Network','academy':'Academy','pricing':'Pricing','sales':'Sales','industrial-investment':'Investment','roi':'ROI','market-share':'Share'}
 header='<header class="atlas-header"><nav aria-label="Main navigation">'+''.join('<section><h2>'+esc(group['title'])+'</h2>'+''.join('<a href="'+pages[i]['path']+'">'+esc(labels.get(i,pages[i]['title']))+'</a>' for i in group['page_refs'])+'</section>' for group in site['navigation_sections'])+'</nav></header>'
 (ROOT/'site/navigation.html').write_text(header+'\n')
 for path in list(ROOT.glob('*.html'))+list((ROOT/'tools').glob('*template.html')):
  if path.name in site['redirects']:continue
  text=path.read_text();
  if not re.search(r'<body\b',text):
   text=re.sub(r'(<html[^>]*>)',r'\1<head>',text,count=1);text=text.replace('</style>','</style></head><body>',1);text=text.replace('</html>','</body></html>')
  text=re.sub(r'<!-- shared-navigation -->.*?<!-- /shared-navigation -->','',text,flags=re.S)
  text=re.sub(r'<nav\b(?![^>]*id=)[^>]*>.*?</nav>','',text,count=1,flags=re.S) if path.name in ['ecosystem.html','roi.html','industrial_investment_1974_1981.html','market-share.html'] or 'template' in path.name else text
  text=re.sub(r'<div class="site-nav project-nav"[^>]*>.*?</div>','',text,flags=re.S)
  if 'site-shell.css' not in text:text=text.replace('</head>','<link rel="stylesheet" href="site-shell.css"><script defer src="site-shell.js"></script></head>')
  text=re.sub(r'(<body\b[^>]*>)',lambda m:m[1]+'<!-- shared-navigation -->'+header+'<!-- /shared-navigation -->',text,count=1)
  text=re.sub(r'<!-- relocated-content -->.*?<!-- /relocated-content -->','',text,flags=re.S)
  page=next((p for p in site['pages'] if p['path']==path.name),None)
  if page:
   content=''
   for fragment in sorted((ROOT/'site/content').glob('*-'+page['id']+'.html')):
    if page['id']=='timeline':
     event='event.ncc82_graphics_mouse' if fragment.name.startswith('ncc') else 'event.autodesk_comdex'
     content+=f'<template id="campaign-{event}">'+fragment.read_text()+'</template>'
    else:content+='<section class="relocated-section">'+fragment.read_text()+'</section>'
   text=text.replace('</body>','<!-- relocated-content --><div id="site-details" class="site-details" data-page="'+page['id']+'">'+content+'</div><!-- /relocated-content --></body>')
  # Retain specific anchors; redirects are only for incoming old URLs.
  text=re.sub(r'href="([^"#?]+\.html)(#[^"]*)?"',lambda m:'href="'+(site['redirects'][m[1]].split('#')[0]+(m[2] or ('#'+site['redirects'][m[1]].split('#')[1] if '#' in site['redirects'][m[1]] else '')) if m[1] in site['redirects'] else m[1]+(m[2] or ''))+'"',text)
  path.write_text(text)
 deep_links={ref:pages[pg]['path']+'#'+ref for ref,pg in site['record_page_links'].items()}
 deep_links['november-prices']='pricing.html#november-prices'
 for source,target in site['redirects'].items():
  (ROOT/source).write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page moved · Logix / AION</title><link rel="stylesheet" href="site-shell.css"><script defer src="site-shell.js"></script></head><body>'+header+'<main class="site-details"><h1>Page moved</h1><p><a id="redirect-target" href="'+target+'">Continue to the reorganised page</a></p></main><script>const routes='+json.dumps(deep_links)+';const target=new URL(routes[decodeURIComponent(location.hash.slice(1))]||document.getElementById("redirect-target").href,location.href);if(location.hash)target.hash=location.hash;if(location.pathname.endsWith("comdex-1982.html")&&location.hash==="#november-prices"){target.pathname=target.pathname.replace("timeline.html","pricing.html");}target.search=location.search;location.replace(target.href);</script></body></html>\n')
 return len(pages)
if __name__=='__main__':print('Built navigation and content for',build(),'primary pages')
