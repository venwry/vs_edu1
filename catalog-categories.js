/* Canonical category predicates shared by catalogue consumers. No legacy aliases. */
(function(root){
'use strict';
const memory=new Set(['memory_ic','memory_module','memory_expansion','memory_assembly','memory_controller_assembly','memory_identification_circuitry','memory_management_ic']);
const expansions=new Set(['memory_expansion','processor_expansion','video_expansion_card','network_interface_card','io_interface_expansion']);
const disks=new Set(['hard_disk_drive','external_floppy_drive','floppy_drive_mechanism']);
const category=(record,records={})=>record?.product_ref?records[record.product_ref]?.category:record?.category;
const isMemory=r=>memory.has(r?.category);
const isExpansion=r=>expansions.has(r?.category);
const isMonitor=r=>r?.category==='monitor';
const isVideoCard=r=>r?.category==='video_expansion_card';
const isDisk=r=>disks.has(r?.category);
const hardwareGroup=r=>isMemory(r)?'memory':isDisk(r)?'disks':isExpansion(r)?'expansion':'ports';
const api={category,isMemory,isExpansion,isMonitor,isVideoCard,isDisk,hardwareGroup};
root.CatalogCategories=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window==='undefined'?globalThis:window);
