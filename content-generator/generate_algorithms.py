"""
Algorithm content generation script.

Phase 1: Preparation and validation framework
Phase 2: AI-powered content generation (to be implemented)

Usage:
    python generate_algorithms.py --validate    # Validate catalog and prompts only
    python generate_algorithms.py --generate    # Generate content using AI (Phase 2)
    python generate_algorithms.py --algorithm "Two Pointer Technique"  # Generate single algorithm
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import sys
import os
import time
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

# Import validation schema
sys.path.append(str(Path(__file__).parent))
from schemas.content_schema import AlgorithmContent, validate_algorithm_content


class AlgorithmContentGenerator:
    """Main content generation orchestrator."""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.catalog_path = self.base_dir / "algorithm_catalog.json"
        self.prompt_template_path = self.base_dir / "prompts" / "algorithm_prompt.md"
        self.output_dir = self.base_dir / "generated"
        self.output_dir.mkdir(exist_ok=True)

        # Initialize Anthropic client
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None

        # Track API usage
        self.total_tokens = 0
        self.total_cost = 0.0
        self.retry_delay = 1.0  # Initial retry delay in seconds

    def load_catalog(self) -> Dict:
        """Load algorithm catalog from JSON."""
        if not self.catalog_path.exists():
            raise FileNotFoundError(f"Catalog not found: {self.catalog_path}")

        with open(self.catalog_path, 'r', encoding='utf-8') as f:
            catalog = json.load(f)

        print(f"[OK] Loaded {len(catalog['algorithms'])} algorithms from catalog")
        return catalog

    def load_prompt_template(self) -> str:
        """Load AI prompt template."""
        if not self.prompt_template_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {self.prompt_template_path}")

        with open(self.prompt_template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        print(f"[OK] Loaded prompt template ({len(template)} characters)")
        return template

    def validate_catalog_structure(self, catalog: Dict) -> bool:
        """Validate catalog has required fields."""
        required_fields = {'title', 'category', 'difficulty', 'priority', 'keywords'}

        for idx, algorithm in enumerate(catalog['algorithms']):
            missing_fields = required_fields - set(algorithm.keys())
            if missing_fields:
                print(f"[ERROR] Algorithm #{idx + 1} missing fields: {missing_fields}")
                return False

            # Validate difficulty
            if algorithm['difficulty'] not in ['Easy', 'Medium', 'Hard']:
                print(f"[ERROR] Algorithm #{idx + 1} has invalid difficulty: {algorithm['difficulty']}")
                return False

            # Validate keywords
            if not isinstance(algorithm['keywords'], list) or len(algorithm['keywords']) < 3:
                print(f"[ERROR] Algorithm #{idx + 1} has insufficient keywords")
                return False

        print(f"[OK] Catalog structure validation passed")
        return True

    def prepare_prompt(self, algorithm_info: Dict, template: str) -> str:
        """
        Prepare AI prompt by filling in template with algorithm details.

        Args:
            algorithm_info: Dictionary with title, category, difficulty, keywords
            template: Prompt template string

        Returns:
            Filled prompt ready for AI
        """
        prompt = template.replace("{title}", algorithm_info['title'])
        prompt = prompt.replace("{category}", algorithm_info['category'])
        prompt = prompt.replace("{difficulty}", algorithm_info['difficulty'])
        prompt = prompt.replace("{keywords}", ", ".join(algorithm_info['keywords']))

        return prompt

    def generate_algorithm_content(self, algorithm_info: Dict, prompt: str) -> Optional[Dict]:
        """
        Generate content for one algorithm using AI.

        Args:
            algorithm_info: Algorithm metadata from catalog
            prompt: Prepared prompt for AI

        Returns:
            Generated content dictionary or None if generation fails
        """
        print(f"\n[GENERATE] Generating content for: {algorithm_info['title']}")
        print(f"   Category: {algorithm_info['category']} | Difficulty: {algorithm_info['difficulty']}")

        if not self.client:
            print("[ERROR] Anthropic API client not initialized. Check ANTHROPIC_API_KEY in .env")
            return None

        # Retry logic with exponential backoff
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                # Call Claude API
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=6000,  # Enough for all 8 sections + code templates
                    temperature=0.7,  # Balance creativity and consistency
                    system="You are an expert algorithm educator creating reference content for coding interview preparation.",
                    messages=[{"role": "user", "content": prompt}]
                )

                # Extract content
                raw_content = response.content[0].text.strip()

                # Track token usage
                input_tokens = response.usage.input_tokens
                output_tokens = response.usage.output_tokens
                total_tokens = input_tokens + output_tokens

                # Calculate cost (Claude 3.5 Sonnet pricing: $3/MTok input, $15/MTok output)
                cost = (input_tokens / 1_000_000 * 3.0) + (output_tokens / 1_000_000 * 15.0)

                self.total_tokens += total_tokens
                self.total_cost += cost

                print(f"[API] Tokens: {total_tokens:,} | Cost: ${cost:.4f}")

                # Parse JSON response
                try:
                    # Handle potential markdown code blocks
                    if raw_content.startswith("```json"):
                        raw_content = raw_content.split("```json")[1].split("```")[0].strip()
                    elif raw_content.startswith("```"):
                        raw_content = raw_content.split("```")[1].split("```")[0].strip()

                    content = json.loads(raw_content)
                    return content

                except json.JSONDecodeError as e:
                    print(f"[ERROR] Failed to parse JSON response: {e}")
                    print(f"[DEBUG] Raw response (first 500 chars): {raw_content[:500]}")
                    return None

            except Exception as e:
                retry_count += 1
                error_msg = str(e)

                if "rate_limit" in error_msg.lower() or "overloaded" in error_msg.lower():
                    if retry_count < max_retries:
                        delay = self.retry_delay * (2 ** retry_count)  # Exponential backoff
                        print(f"[RETRY] Rate limit hit. Waiting {delay:.1f}s before retry {retry_count}/{max_retries}")
                        time.sleep(delay)
                        continue
                    else:
                        print(f"[ERROR] Max retries reached. Giving up.")
                        return None
                else:
                    print(f"[ERROR] API call failed: {error_msg}")
                    return None

        return None

    def validate_generated_content(self, content: Dict, algorithm_title: str) -> bool:
        """
        Validate generated content against Pydantic schema.

        Args:
            content: Generated algorithm content
            algorithm_title: Title for logging

        Returns:
            True if validation passes, False otherwise
        """
        is_valid, message = validate_algorithm_content(content)

        if is_valid:
            print(f"[OK] Validation passed for: {algorithm_title}")
        else:
            print(f"[ERROR] Validation failed for: {algorithm_title}")
            print(f"   Error: {message}")

        return is_valid

    def save_generated_content(self, content: Dict, filename: str) -> None:
        """
        Save generated content to JSON file.

        Args:
            content: Algorithm content dictionary
            filename: Output filename (e.g., "two_pointer_technique.json")
        """
        output_path = self.output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)

        print(f"[SAVE] Saved to: {output_path}")

    def run_validation_only(self) -> bool:
        """
        Run Phase 1 validation checks without generating content.

        Returns:
            True if all validations pass
        """
        print("=" * 60)
        print("Phase 1: Validation Mode")
        print("=" * 60)

        try:
            # Load catalog
            catalog = self.load_catalog()

            # Validate catalog structure
            if not self.validate_catalog_structure(catalog):
                return False

            # Load prompt template
            template = self.load_prompt_template()

            # Test prompt preparation for first algorithm
            first_algo = catalog['algorithms'][0]
            prepared_prompt = self.prepare_prompt(first_algo, template)
            print(f"\n[OK] Prompt preparation test successful")
            print(f"   Sample prompt length: {len(prepared_prompt)} characters")

            # Validate output directory exists
            if self.output_dir.exists():
                print(f"[OK] Output directory ready: {self.output_dir}")
            else:
                print(f"[ERROR] Output directory missing: {self.output_dir}")
                return False

            print("\n" + "=" * 60)
            print("[OK] All Phase 1 validations passed!")
            print("=" * 60)
            print("\n[SUMMARY] Summary:")
            print(f"   - {len(catalog['algorithms'])} algorithms ready for generation")
            print(f"   - Prompt template validated")
            print(f"   - Output directory prepared")
            print(f"   - Validation schema loaded")
            print("\n[READY] Ready for Phase 2: AI content generation")

            return True

        except Exception as e:
            print(f"\n[ERROR] Validation failed: {str(e)}")
            return False

    def run_generation(self, specific_algorithm: Optional[str] = None) -> None:
        """
        Run Phase 2 content generation.

        Args:
            specific_algorithm: If provided, generate only this algorithm
        """
        print("=" * 60)
        print("Phase 2: AI Content Generation")
        print("=" * 60)

        if not self.client:
            print("\n[ERROR] ANTHROPIC_API_KEY not found in environment variables")
            print("Please create .env file with: ANTHROPIC_API_KEY=your_key_here")
            return

        catalog = self.load_catalog()
        template = self.load_prompt_template()

        # Filter algorithms if specific one requested
        algorithms_to_generate = catalog['algorithms']
        if specific_algorithm:
            algorithms_to_generate = [
                algo for algo in catalog['algorithms']
                if algo['title'].lower() == specific_algorithm.lower()
            ]
            if not algorithms_to_generate:
                print(f"[ERROR] Algorithm not found: {specific_algorithm}")
                return

        print(f"\n[INFO] Algorithms to generate: {len(algorithms_to_generate)}")
        print(f"[INFO] Model: Claude 3.5 Sonnet | Temperature: 0.7 | Max tokens: 6000")

        # Track results
        success_count = 0
        failure_count = 0
        skipped_count = 0

        for idx, algorithm_info in enumerate(algorithms_to_generate, 1):
            print(f"\n{'='*60}")
            print(f"[{idx}/{len(algorithms_to_generate)}] {algorithm_info['title']}")
            print(f"{'='*60}")

            # Check if already generated (skip if exists)
            filename = algorithm_info['title'].lower().replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_') + '.json'
            output_path = self.output_dir / filename

            if output_path.exists():
                print(f"[SKIP] Already exists: {filename}")
                skipped_count += 1
                continue

            # Prepare prompt
            prompt = self.prepare_prompt(algorithm_info, template)

            # Generate content
            content = self.generate_algorithm_content(algorithm_info, prompt)

            if content:
                # Validate generated content
                if self.validate_generated_content(content, algorithm_info['title']):
                    # Save to file
                    self.save_generated_content(content, filename)
                    success_count += 1
                    print(f"[SUCCESS] ✅ Generated and validated")
                else:
                    print(f"[FAIL] ❌ Validation failed - not saved")
                    failure_count += 1
            else:
                print(f"[FAIL] ❌ Generation failed")
                failure_count += 1

            # Add small delay to avoid rate limits
            if idx < len(algorithms_to_generate):
                time.sleep(0.5)

        # Print final summary
        print("\n" + "=" * 60)
        print("GENERATION COMPLETE")
        print("=" * 60)
        print(f"\n[RESULTS]")
        print(f"   ✅ Success: {success_count}")
        print(f"   ❌ Failed:  {failure_count}")
        print(f"   ⏭️  Skipped: {skipped_count}")
        print(f"\n[COST REPORT]")
        print(f"   Total tokens: {self.total_tokens:,}")
        print(f"   Total cost:   ${self.total_cost:.4f}")
        print(f"   Avg per algo: ${self.total_cost / max(success_count, 1):.4f}")

        # Save cost report
        report_path = self.output_dir / "cost_report.json"
        cost_report = {
            "total_algorithms": len(algorithms_to_generate),
            "success_count": success_count,
            "failure_count": failure_count,
            "skipped_count": skipped_count,
            "total_tokens": self.total_tokens,
            "total_cost_usd": round(self.total_cost, 4),
            "avg_cost_per_algorithm": round(self.total_cost / max(success_count, 1), 4),
            "model": "claude-3-5-sonnet-20241022",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(report_path, 'w') as f:
            json.dump(cost_report, f, indent=2)

        print(f"\n[SAVE] Cost report saved to: {report_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Algorithm content generation tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Run validation checks only (Phase 1)'
    )

    parser.add_argument(
        '--generate',
        action='store_true',
        help='Generate algorithm content using AI (Phase 2)'
    )

    parser.add_argument(
        '--algorithm',
        type=str,
        help='Generate content for specific algorithm only'
    )

    args = parser.parse_args()

    generator = AlgorithmContentGenerator()

    if args.validate:
        success = generator.run_validation_only()
        sys.exit(0 if success else 1)
    elif args.generate:
        generator.run_generation(args.algorithm)
    else:
        # Default: run validation
        print("No mode specified. Running validation mode.")
        print("Use --generate for content generation (Phase 2)")
        print()
        success = generator.run_validation_only()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
