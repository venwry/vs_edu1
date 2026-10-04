/* Shared date geometry. Plotting envelopes never overwrite canonical story dates. */
(()=>{'use strict';
const DAY=86400000;
function boundary(value,end=false){
 const m=/^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$/.exec(value||'');
 if(!m)return null;
 const y=+m[1],month=+(m[2]||1)-1,day=+(m[3]||1);
 if(!end)return Date.UTC(y,month,day);
 return m[3]?Date.UTC(y,month,day)+DAY:m[2]?Date.UTC(y,month+1,1):Date.UTC(y+1,0,1);
}
function point(ms){const y=new Date(ms).getUTCFullYear();return y+(ms-Date.UTC(y,0,1))/(Date.UTC(y+1,0,1)-Date.UTC(y,0,1));}
const iso=ms=>new Date(ms).toISOString().slice(0,10);
function processSpan(process,story){
 const phases=story.phases.filter(p=>process.phase_refs.includes(p.id));
 const explicit=boundary(process.period.start)!==null&&boundary(process.period.end,true)!==null;
 let start=explicit?boundary(process.period.start):Math.min(...phases.map(p=>boundary(p.period.start)));
 const end=explicit?boundary(process.period.end,true):Math.max(...phases.map(p=>boundary(p.period.end,true)));
 let basis=explicit?'Recorded interval; partial dates cover their stated calendar years or months.':'Approximate display envelope from the associated phase boundaries; actual start and end are unspecified.';
 return {start,end,startDate:iso(start),endDate:iso(end-DAY),approximate:!explicit||process.date_basis==='provisional',basis:process.date_basis==='provisional'?'Provisional academic calendar interval; see date precision notes.':basis};
}
function tracks(items){const ends=[];return items.slice().sort((a,b)=>a.span.start-b.span.start||a.span.end-b.span.end).map(item=>{let track=ends.findIndex(end=>end<=item.span.start);if(track<0)track=ends.length;ends[track]=item.span.end;return {...item,track};});}
window.AtlasTimeline={boundary,point,iso,processSpan,tracks};
})();

