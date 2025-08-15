# Stream Processor Testing Suite

This directory contains comprehensive testing tools for validating MongoDB Atlas Stream Processing JSON configurations before deployment.

## Test Files

### `test_processors.py`
Comprehensive unit test suite using Python's `unittest` framework.

**Features:**
- JSON syntax validation
- Required schema validation 
- Pipeline stage validation
- Connection reference validation
- Naming convention checks
- Best practices linting
- Warning detection for missing DLQ, timestamps, etc.

### `test_runner.py`
Quick validation script with user-friendly output.

**Features:**
- Simple pass/fail validation
- Warning detection
- Clear error reporting
- Fast execution

## Usage

### Quick Testing (Recommended)

Use the integrated `sp test` command for the best experience:

```bash
# Test all processors (returns JSON)
./sp test

# Test specific processor (returns JSON)
./sp test -p solar_simple_processor

# Show help
./sp test --help
```

**Output Format**: The `sp test` command returns structured JSON output by default for consistency with other `sp` commands, making it suitable for automation and programmatic use.

### Direct Script Usage

You can also run the test scripts directly:

```bash
# Quick JSON validation
python3 tests/test_runner.py

# Test specific processor (JSON output)
python3 tests/test_runner.py -p processor_name

# Comprehensive unit tests (traditional test output)
python3 tests/test_processors.py
python3 tests/test_processors.py -v
```

## Validation Checks

### **Critical Errors (Must Fix)**
- Invalid JSON syntax
- Missing required `pipeline` field
- Empty pipeline
- Missing `$source` stage as first stage
- Invalid pipeline stage operators
- Malformed `$merge` or `$emit` stages

### **Warnings (Should Review)**
- Unknown connection references
- Missing output stages (`$merge`, `$emit`)
- No DLQ configuration
- Processor name doesn't match filename

> **Note**: The validation supports current MongoDB Atlas Stream Processing stages including `$emit` for streaming platforms and `$merge` for database collections. Atlas Stream Processing automatically adds `_ts` timestamp fields to all incoming data. Additional output stages may be supported in future versions of MongoDB Atlas Stream Processing.

### **Best Practices (Recommendations)**
- Use lowercase_underscore naming convention
- Include error handling (DLQ)
- Add meaningful field names
- Optionally add processing timestamps for debugging (in addition to automatic `_ts`)

## Integration with Development Workflow

### Pre-Deployment Validation
```bash
# Always test before creating processors
./sp test

# If tests pass, then deploy
./sp create processors
```

### Continuous Integration
Add to your CI/CD pipeline:
```bash
#!/bin/bash
cd tools/
./sp test
if [ $? -eq 0 ]; then
    echo "All processors are valid"
    ./sp create processors
else
    echo "Processor validation failed"
    exit 1
fi
```

### Development Loop
```bash
# 1. Edit processor JSON
vim processors/my_processor.json

# 2. Test specific processor
./sp test -p my_processor

# 3. Fix issues and test again
./sp test -p my_processor --verbose

# 4. Deploy when ready
./sp create processors -p my_processor
```

## Example Output

### Successful Validation
```
Processor Validation Results
==================================================
Total files: 3
Valid: 3
Invalid: 0
```

### With Warnings (Verbose Mode)
```
Processor Validation Results
==================================================
Total files: 3
Valid: 3
Invalid: 0

Warnings:
  No warnings found.
```
```
Processor Validation Results
==================================================
Total files: 3
Valid: 3
Invalid: 0

Warnings:
  • solar_simple_processor.json
    - WARNING: No DLQ configuration
    - WARNING: Consider adding timestamp fields
```

### Validation Errors
```
Processor Validation Results
==================================================
Total files: 3
Valid: 2
Invalid: 1

Files with errors:
  • bad_processor.json
    - ERROR: Missing required 'pipeline' field
```
```
Processor Validation Results
==================================================
Total files: 3
Valid: 2
Invalid: 1

Files with errors:
  • broken_processor.json
    - ERROR: Invalid JSON: Expecting ',' delimiter: line 5 column 1
    - ERROR: Missing required 'pipeline' field
```

## Extending the Tests

### Adding New Validation Rules

1. **Edit `test_processors.py`** for comprehensive unit tests
2. **Edit `test_runner.py`** for quick validation checks

### Example: Adding Custom Validation
```python
def test_custom_validation(self):
    """Test custom business logic"""
    for proc_file in self.processor_files:
        with self.subTest(file=proc_file.name):
            # Your custom validation logic here
            pass
```

## 🔍 **Common Issues and Solutions**

### Issue: "Unknown connection 'my_connection'"
**Solution:** Add the connection to `connections/connections.json`

### Issue: "Missing required 'pipeline' field"
**Solution:** Ensure your JSON has a top-level `pipeline` array

### Issue: "First pipeline stage must be '$source'"
**Solution:** Start your pipeline with a `$source` stage

### Issue: "Invalid JSON syntax"
**Solution:** Use a JSON validator or linter to fix syntax errors

## 📚 **Related Documentation**

- [MongoDB Atlas Stream Processing Pipeline Stages](https://www.mongodb.com/docs/atlas/atlas-stream-processing/pipeline-stages/)
- [SP Command Reference](../tools/README.md)
- [Pipeline Patterns](../docs/PIPELINE_PATTERNS.md)
- [Development Workflow](../docs/DEVELOPMENT_WORKFLOW.md)

---

**Always test your processors before deployment to catch configuration errors early!**
