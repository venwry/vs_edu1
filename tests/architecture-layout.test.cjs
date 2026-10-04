const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const context={window:{}};vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(__dirname,'../architecture-explorer.js'),'utf8'),context);
const rects=[{id:'a',x:20,y:20,w:160,h:110},{id:'middle',x:260,y:20,w:160,h:110},{id:'b',x:500,y:20,w:160,h:110},{id:'lower',x:260,y:200,w:160,h:110}];
for(const [a,b] of [['a','b'],['a','lower'],['middle','b'],['b','a']]){
 const route=context.window.routeArchitecture(rects,a,b);assert(route.length>1);
 for(let i=1;i<route.length;i++){const p=route[i-1],q=route[i];assert(p[0]===q[0]||p[1]===q[1]);for(const r of rects){const crosses=p[0]===q[0]?p[0]>=r.x&&p[0]<=r.x+r.w&&Math.max(p[1],q[1])>r.y&&Math.min(p[1],q[1])<r.y+r.h:p[1]>=r.y&&p[1]<=r.y+r.h&&Math.max(p[0],q[0])>r.x&&Math.min(p[0],q[0])<r.x+r.w;assert(!crosses,'Connector intersects '+r.id);}}
}
console.log('PASS: orthogonal connectors avoid intervening blocks and block borders.');
