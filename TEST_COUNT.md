# Test Case Count

This repository contains **24 test cases** across 8 test files.

## Test Distribution by File

### experiments/Experiment.py (2 test cases)
- `test_create_single_model_experiment__defaults_check_defaults`
- `test_create_provider_experiment__customprompting__init_all`

### experiments/ModelConfiguration.py (5 test cases)
- `test_TwoStaticKeys_Concat`
- `test_key__text_value__hash_text_as_key`
- `test_alias__has_custom__return_custom`
- `test_alias__no_custom__return_key_as_alias`
- `test_MultipleConfigs_ReturnKeysByAlphabeticOrder`

### prompting/Prompt.py (2 test cases)
- `test_Key_TextValue_HashTextAsKey`
- `test_key_Prompt_TextReference_UseIdAsKey`

### prompting/PromptingBase.py (2 test cases)
- `test_apply_decorators__no_decorators_donothing`
- `test_apply_decorators__multiple_decorators__apply`

### tests/integration_tests.py (2 test cases)
- `test_api_run_all_get_functions`
- `test_ExperimentHost_AtomicDataset_RunExperiment`

### utility/FormatHelper.py (1 test case)
- `test_ShortenCode_SmallCodeWith50TrimSize_DoNotTouch`

### utility/Paths.py (5 test cases)
- `test_FindProjectRoot_NestedSrcPath_ReturnParent`
- `test_FindProjectRoot_SrcFilePath_ReturnParent`
- `test_FindProjectRoot_SrcFolderPath_ReturnParent`
- `test_FindProjectRoot_ProjectFolderPath_ReturnParent`
- `test_FindProjectRoot_NoProjectPath_RaiseError`

### utility/StringHelper.py (5 test cases)
- `test_Coelesce_PassNones`
- `test_Coelesce_ChooseFirstStr`
- `test_Coelesce_PassEmpties`
- `test_IsNullOrWhiteSpace_DetectSingleWhitespace`
- `test_IsNullOrWhiteSpace_DetectMultiplesWhitespaces`

## Summary

| Category | Count |
|----------|-------|
| **Total Test Cases** | **24** |
| Test Files | 8 |
| Unit Tests | 22 |
| Integration Tests | 2 |

## How to Count Tests

You can count the test cases in this repository using the provided utility script:

```bash
python count_tests.py
```

This script will scan all Python files in the `src` directory and count test methods (methods starting with `test_` in classes inheriting from `unittest.TestCase`).
