/** Adaptación quirúrgica del paquete original: no recompone ni rasteriza slides.
 * Uso desde la raíz del worktree con RUNTIME_NODE_MODULES y ENSIU_PYTHON.
 * Artifact Tool inspecciona entrada/salida; el parche OOXML preserva gráficos,
 * tablas y coordenadas, evitando una conversión global de la plantilla.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';

const modules=process.env.RUNTIME_NODE_MODULES;
if(!modules) throw new Error('Defina RUNTIME_NODE_MODULES con las dependencias de Codex.');
const require=createRequire(path.join(modules,'package.json'));
const JSZip=require('jszip');
const {FileBlob,PresentationFile}=await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const root=process.cwd();
const source=path.join(root,'outputs/CONACIC2026/PRESENTACION_CONACIC2026_FINAL.pptx');
const build=path.join(root,'build/ensiu2026');
const candidate=path.join(build,'candidate.pptx');
const official=path.join(root,'docs/ENSIU2026/fuentes_oficiales');
await fs.mkdir(build,{recursive:true});
const data=await fs.readFile(source);
if(createHash('sha256').update(data).digest('hex') !== JSON.parse(await fs.readFile(path.join(root,'outputs/ENSIU2026/fuentes_final/ORIGINALES_SHA256.json'),'utf8'))['outputs/CONACIC2026/PRESENTACION_CONACIC2026_FINAL.pptx']) throw new Error('La base cambió desde la auditoría.');
const imported=await PresentationFile.importPptx(await FileBlob.load(source));
if(imported.slides.items.length!==10) throw new Error('Se esperan diez diapositivas.');
await fs.writeFile(path.join(build,'before.ndjson'),(await imported.inspect({kind:'slide,layout,chart,table',maxChars:40000})).ndjson);
const zip=await JSZip.loadAsync(data);
const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const emu=n=>Math.round(n*914400);
const replaceShape=(xml,index,operation)=>{
 let n=0;
 return xml.replace(/<p:(sp|pic|graphicFrame)\b[\s\S]*?<\/p:\1>/g,m=>n++===index?operation(m):m);
};
function setText(shape,lines,{size=1725,bold=false,color='0B2D49'}={}){
 const paras=lines.map(t=>`<a:p><a:pPr marL="0" indent="0"/><a:r><a:rPr lang="es-CO" sz="${size}" b="${bold?1:0}"><a:solidFill><a:srgbClr val="${color}"/></a:solidFill><a:latin typeface="Gill Sans MT"/></a:rPr><a:t>${escape(t)}</a:t></a:r><a:endParaRPr lang="es-CO" sz="${size}"/></a:p>`).join('');
 return shape.replace(/(<p:txBody>[\s\S]*?<a:lstStyle\s*\/>)[\s\S]*?(<\/p:txBody>)/,`$1${paras}$2`);
}
function place(shape,x,y,w,h){
 return shape.replace(/<a:xfrm>[\s\S]*?<\/a:xfrm>/,`<a:xfrm><a:off x="${emu(x)}" y="${emu(y)}"/><a:ext cx="${emu(w)}" cy="${emu(h)}"/></a:xfrm>`);
}
const picture=(id,name,rid,x,y,w,h)=>`<p:pic><p:nvPicPr><p:cNvPr id="${id}" name="${name}" descr="${name}, archivo oficial UNIMINUTO"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="${rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="${emu(x)}" y="${emu(y)}"/><a:ext cx="${emu(w)}" cy="${emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>`;

// Las tres marcas anteriores son objetos independientes del fondo genérico.
let master=await zip.file('ppt/slideMasters/slideMaster1.xml').async('string');
master=master.replace(/<p:pic>[\s\S]*?<\/p:pic>/g,m=>/r:embed="rId1[456]"/.test(m)?'':m);
master=master.replace(/<p:sp>[\s\S]*?<\/p:sp>/g,m=>{
 const text=[...m.matchAll(/<a:t>([\s\S]*?)<\/a:t>/g)].map(x=>x[1]).join('');
 return text==='SIMULTÁNEA'?m.replace(/<p:txBody>[\s\S]*?<\/p:txBody>/,'<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody>'):m;
});
master=master.replace('</p:spTree>',picture(900,'Logo ENSIU 2026','rIdEnsiu',7.25,0.35,2.8,2.8*107/418)+picture(901,'Logo UNIMINUTO','rIdUniminuto',10.35,0.43,2.25,2.25*71/263)+'</p:spTree>');
zip.file('ppt/slideMasters/slideMaster1.xml',master);
let rels=await zip.file('ppt/slideMasters/_rels/slideMaster1.xml.rels').async('string');
rels=rels.replace(/<Relationship\b[^>]*\bId="rId1[456]"[^>]*\/>/g,'').replace('</Relationships>','<Relationship Id="rIdEnsiu" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/logo_ensiu.jpg"/><Relationship Id="rIdUniminuto" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/logo_uniminuto.png"/></Relationships>');
zip.file('ppt/slideMasters/_rels/slideMaster1.xml.rels',rels);
for(const f of ['image2.emf','image3.png','image4.png'])zip.remove(`ppt/media/${f}`);
zip.file('ppt/media/logo_ensiu.jpg',await fs.readFile(path.join(official,'Logo-Ensiu-2026-web.jpg')));
zip.file('ppt/media/logo_uniminuto.png',await fs.readFile(path.join(official,'logo-uniminuto.png')));
let types=await zip.file('[Content_Types].xml').async('string');
types=types.replace(/<Default Extension="emf"[^>]*\/>/,'');
if(!types.includes('Extension="jpg"'))types=types.replace('</Types>','<Default Extension="jpg" ContentType="image/jpeg"/></Types>');
zip.file('[Content_Types].xml',types);

for(let i=1;i<=10;i++){
 const f=`ppt/slides/slide${i}.xml`;
 let xml=(await zip.file(f).async('string')).replaceAll('CONACIC 2026','ENSIU 2026');
 if(i===1){
  xml=replaceShape(xml,3,s=>setText(s,['Anticipar para Incluir:','Inteligencia Artificial al Servicio de la Equidad Educativa'],{size:2550,bold:true,color:'FFFFFF'}));
  xml=replaceShape(xml,6,s=>setText(place(s,1.77,5.63,10.1,0.72),['Misión 4 — Inteligencia Artificial para la equidad','Edwin: Especialización en Inteligencia Artificial · Código 1071010'],{size:1500,color:'FFFFFF'}));
 }
 if(i===2){
  xml=replaceShape(xml,9,s=>setText(place(s,1.25,6.12,10.7,0.38),['Datos para la equidad: información pública con lectura territorial.'],{size:1650}));
 }
 if(i===10){
  xml=replaceShape(xml,10,s=>setText(place(s,1.2917,6.08,10.84,0.58),['Trabajo futuro: validación walk-forward, mejores datos y evaluación institucional','con enfoque de equidad territorial.'],{size:1500}));
 }
 zip.file(f,xml);
}

const script=await fs.readFile(path.join(root,'outputs/ENSIU2026/GUION_PONENCIA_ENSIU2026_FINAL.md'),'utf8');
const sections=[...script.matchAll(/### (\d+)\. ([^\n]+)\n\n\*\*Texto oral\*\*\n\n([\s\S]*?)\n\n\*\*Apoyo:/g)];
if(sections.length!==10)throw new Error('Faltan secciones del guion.');
const evidence=[
 'Comunicación de ponencia ENSIU 2026, título, autoría y alineación institucional. Logos originales: https://www.uniminuto.edu/ensiu, consultada el 28/09/2026.',
 'Comunicación de ponencia ENSIU 2026, apartados S y T y alineación institucional.',
 'Reportes públicos ICFES 2020–2024; gráfico y libro incrustado originales del proyecto. Unidad: institución, programa, prueba y año.',
 'Auditoría metodológica archivada del proyecto. No se atribuye carácter completamente temporal a la validación interna.',
 'outputs/reports/decision_modelo_final.txt; outputs/reports/decision_transformer.txt. Comparación limitada a configuraciones evaluadas.',
 'outputs/metrics/baseline_metrics.csv; outputs/figures/lgbm_predicho_vs_real.png.',
 'outputs/metrics/baseline_metrics.csv; outputs/reports/decision_transformer.txt. Se conserva la tabla científica original, incluido MAE no disponible para Transformer.',
 'outputs/figures/lgbm_shap_beeswarm.png. SHAP es una explicación predictiva, no causal.',
 'Izquierda: outputs/figures/lgbm_error_por_nbc.png. Derecha: cifras aproximadas departamentales del resultado científico archivado; outputs/metrics/metricas_lgbm_por_depto.csv. Análisis descriptivo.',
 'Resultados archivados del proyecto y comunicación de ponencia ENSIU 2026. Validación e impacto institucional pendientes.'
];
for(const [_,num,title,body] of sections){
 const f=`ppt/notesSlides/notesSlide${num}.xml`;
 let xml=await zip.file(f).async('string');
 xml=xml.replace(/<p:sp>[\s\S]*?<\/p:sp>/g,m=>m.includes('type="body"')?setText(m,[`${num}. ${title}`,...body.split('\n\n'),`Fuentes: ${evidence[Number(num)-1]}`],{size:1200}):m);
 zip.file(f,xml);
}
// Metadatos y miniatura: retirar referencias o previsualizaciones antiguas.
for(const f of Object.keys(zip.files)){
 if(f.startsWith('docProps/thumbnail'))zip.remove(f);
 if(f.endsWith('.xml')||f.endsWith('.rels')){
  let xml=await zip.file(f).async('string');
  if(f==='_rels/.rels')xml=xml.replace(/<Relationship\b[^>]*Type="[^"]*thumbnail"[^>]*\/>/g,'');
  if(f==='[Content_Types].xml')xml=xml.replace(/<Override\b[^>]*PartName="\/docProps\/thumbnail[^>]*\/>/g,'');
  if(f==='docProps/core.xml'){
   xml=xml.replace(/<dc:title>[\s\S]*?<\/dc:title>/,'<dc:title>Anticipar para Incluir: Inteligencia Artificial al Servicio de la Equidad Educativa</dc:title>');
   xml=xml.replace(/<dc:creator>[\s\S]*?<\/dc:creator>/,'<dc:creator>Edwin Santiago Paz Bedoya; Nathalia Orozco Morales</dc:creator>');
  }
  xml=xml.replaceAll('CONACIC','ENSIU').replaceAll('CONAC','ENSIU').replaceAll('UADY','UNIMINUTO').replaceAll('SIMULTÁNEA','').replaceAll('SIMULTANEA','');
  zip.file(f,xml);
 }
}
await fs.writeFile(candidate,await zip.generateAsync({type:'nodebuffer',compression:'DEFLATE'}));
const check=await PresentationFile.importPptx(await FileBlob.load(candidate));
await fs.writeFile(path.join(build,'after.ndjson'),(await check.inspect({kind:'slide,layout,chart,table',maxChars:40000})).ndjson);
console.log(JSON.stringify({candidate,slides:check.slides.items.length,changedContent:[1,2,10],visualOnly:[3,4,5,6,7,8,9]}));
