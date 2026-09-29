import path from 'node:path';
import fs from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const skill='C:/Users/santi/.codex/plugins/cache/openai-primary-runtime/presentations/26.915.20218/skills/presentations';
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const root=process.cwd();
const ref=path.join(root,'outputs/CONACIC2026/PRESENTACION_CONACIC2026_FINAL.pptx');
const result=await finalizePresentation({
 workspaceDir:root,candidatePath:path.join(root,'build/ensiu2026/candidate.pptx'),
 finalPath:path.join(root,'outputs/ENSIU2026/PRESENTACION_ENSIU2026_FINAL.pptx'),
 pythonExecutable:'C:/Users/santi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit','--require-native-table-slide','7'],
 explicitTotalSlideCount:10,requiredNativeTableOwnerSlides:[7],requiredNativeChartOwnerSlides:[3],requiredEmbeddedWorkbookChartOwnerSlides:[3],
 fontPolicy:{basis:'reference',families:['Gill Sans MT'],referencePath:ref,referenceSha256:createHash('sha256').update(await fs.readFile(ref)).digest('hex')},
 verifyArtifactToolImport:true,receiptPath:path.join(root,'build/ensiu2026/final-validation.json')
});
console.log(JSON.stringify(result));
