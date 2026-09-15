import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';

const root=process.cwd();
const out=path.join(root,'outputs/CONACIC2026');
const build=path.join(root,'tmp/conacic2026');
const skill=process.env.CONACIC_PRESENTATIONS_SKILL;
const python=process.env.CONACIC_RUNTIME_PYTHON;
if(!skill||!python)throw new Error('Set CONACIC_PRESENTATIONS_SKILL and CONACIC_RUNTIME_PYTHON');
const template=path.join(out,'plantillas_oficiales/CONACIC2024_PLANTILLA_PARA_PONENCIAS_SIMULTANEAS.pptx');
const p=await PresentationFile.importPptx(await FileBlob.load(template));
const content=JSON.parse(await fs.readFile(path.join(out,'CRONOMETRAJE.json'),'utf8'));
// Actual imported blank layout. Existing five source slides remain in use.
while(p.slides.items.length<10)p.slides.add({layoutId:'/ppt/slideLayouts/slideLayout7.xml'});
const white='#FFFFFF', navy='#0A2B4B', green='#00AD50';
const font='Gill Sans MT'; // Major and minor Latin font in the official theme.
function rect(sl,x,y,w,h,fill){return sl.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:'none',width:0}})}
function text(sl,t,x,y,w,h,size=26,color=navy,bold=false){
 const sh=sl.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=t;sh.text.style={typeface:font,fontSize:size,color,bold,autoFit:'none',verticalAlignment:'middle'};
 return sh;
}
function bulletLines(sl,lines,x,y,w,size=27,step=70){lines.forEach((v,i)=>text(sl,v,x,y+step*i,w,step-10,size));}
async function picture(sl,name,x,y,w,h){sl.images.add({blob:await fs.readFile(path.join(root,'outputs/figures',name)),contentType:'image/png',alt:name.replaceAll('_',' '),fit:'contain',position:{left:x,top:y,width:w,height:h}})}
for(let i=0;i<10;i++){
 const sl=p.slides.items[i],s=content.slides[i];
 if(i===0){
  rect(sl,140,164,1060,460,navy);
  text(sl,s.title,170,186,1000,210,34,white,true);
  text(sl,'Edwin Santiago Paz Bedoya\nNathalia Orozco Morales',170,410,980,72,28,white);
  text(sl,'UNIMINUTO Virtual – Bogotá, Colombia',170,495,970,38,23,white);
  text(sl,'edwin.paz@uniminuto.edu\nnathalia.orozco@uniminuto.edu',170,540,950,58,19,white);
 }else{
  rect(sl,90,148,1115,65,navy);
  text(sl,s.title,106,153,1080,53,34,white,true);
  rect(sl,90,224,1115,418,white);
 }
 text(sl,`CONACIC 2026 · Paper 17 · DRAFT · ${i+1}/10`,165,660,1030,30,17,white);
 sl.speakerNotes.textFrame.setText(`${s.speech}\n\nTiempo planificado: ${s.start}–${s.end} s. Señalar: ${s.point}\nFuentes: ${s.source}\nEstado: DRAFT. Pendiente de similitud, IA y revisión final.`);
}
let sl=p.slides.items[1];
text(sl,'Objetivo',120,246,350,42,28,navy,true);
text(sl,'Estimar el PROMEDIO_GLOBAL de la siguiente aplicación\na partir del historial público de cada programa',120,302,1045,100,31);
rect(sl,120,426,1030,3,green);
text(sl,'Unidad de análisis',120,450,440,42,26,navy,true);
text(sl,'Institución · programa · prueba · año',120,500,1000,46,30);
text(sl,'Alcance: predicción agregada y apoyo a revisión académica',120,578,1020,35,23);

sl=p.slides.items[2];
text(sl,'127.716 filas procesadas',120,243,1000,45,32,navy,true);
const ch=sl.charts.add('bar',{position:{left:120,top:310,width:645,height:285},categories:['2020','2021','2022','2023','2024'],series:[{name:'Filas del panel',values:[19135,24233,27722,27864,28762],fill:'#24719B'}],barOptions:{direction:'column',grouping:'clustered'},hasLegend:false,dataLabels:{showValue:true,position:'outEnd'}});
const {applyPresentationChartFont,finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
applyPresentationChartFont(ch,{fontFamily:font});
text(sl,'Reportes ICFES 2020–2024',800,312,365,65,26,navy,true);
text(sl,'Datos agregados\n\nEstadísticas reorganizadas\nen columnas\n\nHistorial por entidad',800,384,370,220,24);

sl=p.slides.items[3];
rect(sl,125,255,650,91,navy);rect(sl,792,255,364,91,green);
text(sl,'Entrenamiento 2020–2023\n98.954 filas',143,264,608,72,27,white,true);
text(sl,'Prueba 2024\n28.762 filas',810,264,330,72,27,white,true);
bulletLines(sl,['Excluir puntajes y medidas del mismo ciclo','Construir rezagos con observaciones anteriores','Calcular tendencias sin incluir el resultado actual'],125,376,1030,27,60);
text(sl,'Pendiente de revisión: las divisiones internas mezclan años',125,581,1030,38,23,'#95401C',true);

sl=p.slides.items[4];
const models=[['Ridge y Lasso','Referencias lineales con regularización'],['LightGBM','50 ensayos Optuna · 188 árboles finales'],['Transformer encoder','2 capas · 4 cabezas · secuencias por entidad']];
models.forEach((v,i)=>{text(sl,v[0],123,250+i*103,1020,42,29,navy,true);text(sl,v[1],123,294+i*103,1020,38,25);});
text(sl,'Comparación limitada a las configuraciones e información disponibles',123,592,1045,32,21);

sl=p.slides.items[5];
await picture(sl,'lgbm_predicho_vs_real.png',105,235,640,393);
text(sl,'RMSE  9,3293',780,265,395,48,34,navy,true);
text(sl,'MAE    6,2109',780,335,395,48,34,navy,true);
text(sl,'R²        0,7062',780,405,395,48,34,navy,true);
text(sl,'Evaluación externa en 2024\n28.762 observaciones',780,503,400,90,25);

sl=p.slides.items[6];
const values=[['Modelo','RMSE','MAE','R²'],['Ridge','10,2294','7,2967','0,6467'],['Lasso','10,0722','7,0622','0,6575'],['LightGBM','9,3293','6,2109','0,7062'],['Transformer','16,8588','n/d','0,0405']];
const table=sl.tables.add({rows:5,columns:4,left:120,top:254,width:1050,height:275,columnWidths:[360,230,230,230],values});
for(let r=0;r<5;r++)for(let c=0;c<4;c++){const cell=table.getCell(r,c);cell.fill=r===0?navy:(r===3?'#D8EFE3':(r%2?'#F2F5F7':white));cell.text.style={typeface:font,fontSize:27,color:r===0?white:navy,bold:r===0||r===3};}
table.borders.assign({style:'solid',fill:'#D9E0E5',width:1});
text(sl,'LightGBM reduce 7,4 % el RMSE frente a Lasso',125,552,1040,43,29,navy,true);
text(sl,'Resultados aceptados. Un año de prueba; sin intervalos formales.',125,598,1040,30,20);

sl=p.slides.items[7];
await picture(sl,'lgbm_shap_beeswarm.png',105,231,625,405);
text(sl,'Mayor influencia del historial',758,263,425,75,28,navy,true);
text(sl,'1. Rezago global más reciente\n\n2. Segundo rezago global\n\n3. Rezago de la prueba',758,363,430,189,24);
text(sl,'Asociación predictiva\nsin interpretación causal',758,560,410,59,23);

sl=p.slides.items[8];
await picture(sl,'lgbm_error_por_nbc.png',105,233,620,395);
text(sl,'RMSE por departamento',750,249,440,42,27,navy,true);
text(sl,'Sucre          13,29  (n = 366)\nChocó          12,03  (n = 243)\nPutumayo   11,18  (n = 54)',750,310,450,130,24);
text(sl,'Cinco años de datos\nUn único año de prueba\nSin covariables socioeconómicas',750,470,440,140,24);

sl=p.slides.items[9];
text(sl,'Resultado',124,251,990,43,28,navy,true);
text(sl,'LightGBM: RMSE 9,33 y R² 0,706 en 2024',124,300,1030,48,31);
text(sl,'Alcance',124,371,1030,40,28,navy,true);
text(sl,'Historial útil, datos agregados y evidencia de un solo corte',124,417,1030,50,27);
text(sl,'Trabajo futuro',124,484,1030,40,28,navy,true);
text(sl,'Varios cortes temporales, revisión de variables y validación institucional',124,532,1030,76,27);

await fs.mkdir(build,{recursive:true});
const candidate=path.join(build,'presentation_candidate.pptx');
await(await PresentationFile.exportPptx(p)).save(candidate);
await fs.writeFile(path.join(build,'deck-inspect.ndjson'),(await p.inspect({kind:'slide,textbox,chart,table',maxChars:60000})).ndjson);
const result=await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:process.env.CONACIC_FINAL_PPTX || path.join(out,'PRESENTACION_CONACIC2026.pptx'),pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit','--require-native-table-slide','7'],fontPolicy:{basis:"reference",families:["Gill Sans MT"],referencePath:template,referenceSha256:createHash("sha256").update(await fs.readFile(template)).digest("hex")},requiredNativeTableOwnerSlides:[7],requiredNativeChartOwnerSlides:[3],materializeLiteralChartWorkbooks:true,explicitTotalSlideCount:10,verifyArtifactToolImport:true,receiptPath:process.env.CONACIC_RECEIPT || path.join(build,'presentation_validation.json')});
console.log(JSON.stringify(result));
