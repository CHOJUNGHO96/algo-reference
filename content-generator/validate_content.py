"""
Content quality validation script.

Validates generated algorithm content for completeness, syntax, and quality.

Usage:
    python validate_content.py
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
import ast


class ContentValidator:
    """Validate generated algorithm content"""

    def __init__(self, content_dir: Path):
        self.content_dir = content_dir
        self.results = {
            "total_files": 0,
            "valid_files": 0,
            "issues": []
        }
        self.quality_metrics = {
            "completeness": [],
            "content_length": {},
            "code_syntax_valid": {"python": 0, "cpp": 0, "java": 0},
            "leetcode_refs": 0
        }

    def validate_python_syntax(self, code: str) -> Tuple[bool, str]:
        """Validate Python code syntax"""
        try:
            ast.parse(code)
            return True, ""
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"

    def validate_cpp_syntax(self, code: str) -> Tuple[bool, str]:
        """Basic C++ syntax validation (simplified)"""
        # Check for basic C++ structure
        has_braces = '{' in code and '}' in code
        has_semicolons = ';' in code
        has_includes_or_using = '#include' in code or 'using namespace' in code

        if not (has_braces and has_semicolons):
            return False, "Missing basic C++ structure (braces/semicolons)"

        return True, ""

    def validate_java_syntax(self, code: str) -> Tuple[bool, str]:
        """Basic Java syntax validation (simplified)"""
        # Check for basic Java structure
        has_class = 'class ' in code or 'public ' in code
        has_braces = '{' in code and '}' in code
        has_semicolons = ';' in code

        if not (has_class and has_braces and has_semicolons):
            return False, "Missing basic Java structure (class/braces/semicolons)"

        return True, ""

    def check_placeholder_text(self, text: str) -> List[str]:
        """Check for placeholder text"""
        placeholders = []
        placeholder_patterns = [
            r'\bTODO\b',
            r'\bFIXME\b',
            r'\bXXX\b',
            r'Lorem ipsum',
            r'\.\.\.',
            r'placeholder',
            r'to be implemented'
        ]

        for pattern in placeholder_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                placeholders.append(pattern)

        return placeholders

    def validate_leetcode_references(self, problem_types: List[Dict]) -> Tuple[int, List[str]]:
        """Validate LeetCode problem references"""
        valid_count = 0
        issues = []
        leetcode_pattern = re.compile(r'^LC \d+\. .+')

        for problem_type in problem_types:
            examples = problem_type.get("leetcode_examples", [])
            for example in examples:
                if leetcode_pattern.match(example):
                    valid_count += 1
                else:
                    issues.append(f"Invalid format: {example}")

        return valid_count, issues

    def calculate_completeness(self, content: Dict) -> float:
        """Calculate content completeness score (0-1)"""
        required_fields = [
            "title", "category", "difficulty", "concept_summary",
            "core_formulas", "thought_process", "application_conditions",
            "time_complexity", "space_complexity", "problem_types",
            "common_mistakes", "code_templates"
        ]

        filled_count = 0
        total_count = len(required_fields)

        for field in required_fields:
            value = content.get(field)
            if value:
                # Check if actually filled (not just empty string/list/dict)
                if isinstance(value, str) and len(value.strip()) > 0:
                    filled_count += 1
                elif isinstance(value, (list, dict)) and len(value) > 0:
                    filled_count += 1

        # Check code templates specifically
        code_templates = content.get("code_templates", {})
        if all(len(code.strip()) > 100 for code in code_templates.values()):
            # Give extra points for all 3 languages having substantial code
            filled_count += 1

        return filled_count / total_count

    def validate_file(self, file_path: Path) -> Dict:
        """Validate a single JSON file"""
        file_result = {
            "filename": file_path.name,
            "valid": True,
            "issues": [],
            "completeness": 0.0,
            "content_lengths": {}
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)

            # 1. Check completeness
            completeness = self.calculate_completeness(content)
            file_result["completeness"] = completeness
            self.quality_metrics["completeness"].append(completeness)

            if completeness < 0.9:
                file_result["issues"].append(f"Completeness only {completeness*100:.1f}%")
                file_result["valid"] = False

            # 2. Check 8-point structure
            concept_summary = content.get("concept_summary", "")
            thought_process = content.get("thought_process", "")
            common_mistakes = content.get("common_mistakes", "")

            file_result["content_lengths"] = {
                "concept_summary": len(concept_summary),
                "thought_process": len(thought_process),
                "common_mistakes": len(common_mistakes)
            }

            # 3. Check for placeholders
            all_text = json.dumps(content)
            placeholders = self.check_placeholder_text(all_text)
            if placeholders:
                file_result["issues"].append(f"Contains placeholders: {', '.join(placeholders)}")
                file_result["valid"] = False

            # 4. Validate code templates
            code_templates = content.get("code_templates", {})

            # Python
            python_code = code_templates.get("python", "")
            if python_code:
                valid, error = self.validate_python_syntax(python_code)
                if valid:
                    self.quality_metrics["code_syntax_valid"]["python"] += 1
                else:
                    file_result["issues"].append(f"Python syntax error: {error}")
                    file_result["valid"] = False

            # C++
            cpp_code = code_templates.get("cpp", "")
            if cpp_code:
                valid, error = self.validate_cpp_syntax(cpp_code)
                if valid:
                    self.quality_metrics["code_syntax_valid"]["cpp"] += 1
                else:
                    file_result["issues"].append(f"C++ syntax error: {error}")

            # Java
            java_code = code_templates.get("java", "")
            if java_code:
                valid, error = self.validate_java_syntax(java_code)
                if valid:
                    self.quality_metrics["code_syntax_valid"]["java"] += 1
                else:
                    file_result["issues"].append(f"Java syntax error: {error}")

            # 5. Validate LeetCode references
            problem_types = content.get("problem_types", [])
            valid_refs, ref_issues = self.validate_leetcode_references(problem_types)
            self.quality_metrics["leetcode_refs"] += valid_refs

            if ref_issues:
                file_result["issues"].append(f"LeetCode ref issues: {len(ref_issues)}")

        except json.JSONDecodeError as e:
            file_result["valid"] = False
            file_result["issues"].append(f"Invalid JSON: {str(e)}")

        except Exception as e:
            file_result["valid"] = False
            file_result["issues"].append(f"Validation error: {str(e)}")

        return file_result

    def run_validation(self) -> None:
        """Run validation on all files"""
        print("=" * 60)
        print("CONTENT QUALITY VALIDATION")
        print("=" * 60)

        if not self.content_dir.exists():
            print(f"\n[ERROR] Directory not found: {self.content_dir}")
            return

        # Find JSON files (exclude cost report)
        json_files = [f for f in self.content_dir.glob("*.json") if not f.name.startswith("cost_")]

        if not json_files:
            print(f"\n[ERROR] No JSON files found in: {self.content_dir}")
            return

        print(f"\n[INFO] Validating {len(json_files)} files...")

        for idx, json_file in enumerate(json_files, 1):
            print(f"\n[{idx}/{len(json_files)}] {json_file.name}")

            result = self.validate_file(json_file)
            self.results["total_files"] += 1

            if result["valid"]:
                self.results["valid_files"] += 1
                print(f"   [OK] VALID (completeness: {result['completeness']*100:.1f}%)")
            else:
                print(f"   [FAIL] ISSUES FOUND:")
                for issue in result["issues"]:
                    print(f"      - {issue}")
                self.results["issues"].append(result)

        # Generate quality report
        self.print_quality_report()

    def print_quality_report(self) -> None:
        """Print comprehensive quality report"""
        print("\n" + "=" * 60)
        print("QUALITY REPORT")
        print("=" * 60)

        # Summary
        print(f"\n[SUMMARY]")
        print(f"   Total files:  {self.results['total_files']}")
        print(f"   Valid:        {self.results['valid_files']}")
        print(f"   Issues:       {len(self.results['issues'])}")

        # Completeness
        if self.quality_metrics["completeness"]:
            avg_completeness = sum(self.quality_metrics["completeness"]) / len(self.quality_metrics["completeness"])
            print(f"\n[COMPLETENESS]")
            print(f"   Average: {avg_completeness*100:.1f}%")
            print(f"   Min:     {min(self.quality_metrics['completeness'])*100:.1f}%")
            print(f"   Max:     {max(self.quality_metrics['completeness'])*100:.1f}%")

        # Code syntax validation
        print(f"\n[CODE SYNTAX VALIDATION]")
        print(f"   Python: {self.quality_metrics['code_syntax_valid']['python']} valid")
        print(f"   C++:    {self.quality_metrics['code_syntax_valid']['cpp']} valid")
        print(f"   Java:   {self.quality_metrics['code_syntax_valid']['java']} valid")

        # LeetCode references
        print(f"\n[LEETCODE REFERENCES]")
        print(f"   Valid references: {self.quality_metrics['leetcode_refs']}")

        # Issues detail
        if self.results["issues"]:
            print(f"\n[ISSUES DETAIL]")
            for issue_result in self.results["issues"]:
                print(f"\n   File: {issue_result['filename']}")
                for issue in issue_result["issues"]:
                    print(f"      - {issue}")

        # Save report
        report_path = self.content_dir / "validation_report.json"
        report_data = {
            "summary": {
                "total_files": self.results['total_files'],
                "valid_files": self.results['valid_files'],
                "files_with_issues": len(self.results['issues'])
            },
            "quality_metrics": {
                "average_completeness": sum(self.quality_metrics["completeness"]) / max(len(self.quality_metrics["completeness"]), 1),
                "code_syntax_valid": self.quality_metrics["code_syntax_valid"],
                "total_leetcode_refs": self.quality_metrics["leetcode_refs"]
            },
            "issues": self.results["issues"]
        }

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)

        print(f"\n[SAVE] Validation report saved to: {report_path}")


def main():
    """Entry point"""
    script_dir = Path(__file__).parent
    content_dir = script_dir / "generated"

    validator = ContentValidator(content_dir)
    validator.run_validation()


if __name__ == "__main__":
    main()
