import { finalizePresentation } from 'file:///C:/Users/HOME/.codex/plugins/cache/openai-primary-runtime/presentations/26.1022.11436/skills/presentations/container_tools/artifact_tool_utils.mjs';
process.env.RUNTIME_NODE_MODULES='C:/Users/HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const root='E:/Projects/DBMS OOPS/presentations';
const skill='C:/Users/HOME/.codex/plugins/cache/openai-primary-runtime/presentations/26.1022.11436/skills/presentations';
const owners=[3,4,7,8,9,10,12,16];
console.log(await finalizePresentation({workspaceDir:root,candidatePath:root+'/.build/candidate.pptx',finalPath:root+'/output/FoodBridge_OOP_DBMS.pptx',pythonExecutable:'C:/Users/HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...owners.flatMap(n=>['--require-native-table-slide',String(n)])],requiredNativeTableOwnerSlides:owners,fontPolicy:{basis:'design',families:['Aptos']},verifyArtifactToolImport:true,receiptPath:root+'/.build/validation.json'}));

