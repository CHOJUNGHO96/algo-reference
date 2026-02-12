"""
Database seeding script for algorithm content.

Reads generated JSON files from content-generator and populates the database.

Usage:
    python -m scripts.seed_data
    OR (if using Docker):
    docker-compose exec backend python -m scripts.seed_data
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path for imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.models.algorithm import Algorithm
from app.models.category import Category
from app.models.difficulty import DifficultyLevel, DifficultyEnum
from app.models.language import ProgrammingLanguage
from app.models.code_template import CodeTemplate


class DatabaseSeeder:
    """Seed database with algorithm content"""

    def __init__(self, content_dir: Path):
        self.content_dir = content_dir
        self.stats = {
            "algorithms": 0,
            "code_templates": 0,
            "categories": 0,
            "difficulties": 0,
            "languages": 0,
            "skipped": 0,
            "errors": 0
        }

    async def seed_base_data(self, session: AsyncSession) -> Dict[str, int]:
        """
        Seed base reference data (categories, difficulties, languages).

        Returns:
            Dictionary mapping difficulty names to IDs
        """
        print("\n[1/4] Seeding base reference data...")

        # 1. Seed difficulty levels
        difficulty_map = {}
        difficulties = [
            {"name": DifficultyEnum.EASY, "color": "#22c55e"},
            {"name": DifficultyEnum.MEDIUM, "color": "#f59e0b"},
            {"name": DifficultyEnum.HARD, "color": "#ef4444"}
        ]

        for diff_data in difficulties:
            result = await session.execute(
                select(DifficultyLevel).where(DifficultyLevel.name == diff_data["name"])
            )
            difficulty = result.scalar_one_or_none()

            if not difficulty:
                difficulty = DifficultyLevel(**diff_data)
                session.add(difficulty)
                await session.flush()
                self.stats["difficulties"] += 1
                print(f"   Created difficulty: {diff_data['name'].value}")

            difficulty_map[diff_data["name"].value] = difficulty.id

        # 2. Seed programming languages
        languages = [
            {"name": "Python", "slug": "python", "extension": ".py", "prism_key": "python"},
            {"name": "C++", "slug": "cpp", "extension": ".cpp", "prism_key": "cpp"},
            {"name": "Java", "slug": "java", "extension": ".java", "prism_key": "java"}
        ]

        for lang_data in languages:
            result = await session.execute(
                select(ProgrammingLanguage).where(ProgrammingLanguage.slug == lang_data["slug"])
            )
            language = result.scalar_one_or_none()

            if not language:
                language = ProgrammingLanguage(**lang_data)
                session.add(language)
                self.stats["languages"] += 1
                print(f"   Created language: {lang_data['name']}")

        await session.commit()
        print(f"[OK] Base data ready: {self.stats['difficulties']} difficulties, {self.stats['languages']} languages")

        return difficulty_map

    async def find_or_create_category(
        self,
        session: AsyncSession,
        category_name: str
    ) -> Category:
        """Find existing category or create new one"""
        slug = category_name.lower().replace(' ', '-').replace('/', '-')

        result = await session.execute(
            select(Category).where(Category.slug == slug)
        )
        category = result.scalar_one_or_none()

        if not category:
            # Create new category
            category = Category(
                name=category_name,
                slug=slug,
                description=f"Algorithms related to {category_name}",
                display_order=self.stats["categories"],
                color="#0969da"
            )
            session.add(category)
            await session.flush()
            self.stats["categories"] += 1
            print(f"   Created category: {category_name}")

        return category

    async def seed_algorithm(
        self,
        session: AsyncSession,
        content: Dict,
        difficulty_map: Dict[str, int]
    ) -> Optional[Algorithm]:
        """
        Seed a single algorithm with its code templates.

        Args:
            session: Database session
            content: Algorithm content from JSON
            difficulty_map: Mapping of difficulty names to IDs

        Returns:
            Created Algorithm or None if skipped/failed
        """
        title = content.get("title")
        slug = title.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_')

        # Check if algorithm already exists
        result = await session.execute(
            select(Algorithm).where(Algorithm.slug == slug)
        )
        existing = result.scalar_one_or_none()

        if existing:
            print(f"   [SKIP] Already exists: {title}")
            self.stats["skipped"] += 1
            return None

        try:
            # Find or create category
            category = await self.find_or_create_category(session, content["category"])

            # Get difficulty ID
            difficulty_id = difficulty_map.get(content["difficulty"])
            if not difficulty_id:
                print(f"   [ERROR] Invalid difficulty for {title}: {content['difficulty']}")
                self.stats["errors"] += 1
                return None

            # Create algorithm
            algorithm = Algorithm(
                title=title,
                slug=slug,
                category_id=category.id,
                difficulty_id=difficulty_id,
                concept_summary=content["concept_summary"],
                core_formulas=content.get("core_formulas", []),
                thought_process=content.get("thought_process"),
                application_conditions=content.get("application_conditions", {}),
                time_complexity=content["time_complexity"],
                space_complexity=content["space_complexity"],
                problem_types=content.get("problem_types", []),
                common_mistakes=content.get("common_mistakes"),
                is_published=True  # Auto-publish AI-generated content
            )

            session.add(algorithm)
            await session.flush()  # Get algorithm.id
            self.stats["algorithms"] += 1

            # Create code templates
            code_templates = content.get("code_templates", {})
            language_map = {"python": "python", "cpp": "cpp", "java": "java"}

            for lang_key, code in code_templates.items():
                if not code or len(code.strip()) < 50:
                    continue

                # Get language ID
                lang_slug = language_map.get(lang_key)
                if not lang_slug:
                    continue

                result = await session.execute(
                    select(ProgrammingLanguage).where(ProgrammingLanguage.slug == lang_slug)
                )
                language = result.scalar_one_or_none()

                if language:
                    template = CodeTemplate(
                        algorithm_id=algorithm.id,
                        language_id=language.id,
                        code=code,
                        explanation=None  # Can be enhanced later
                    )
                    session.add(template)
                    self.stats["code_templates"] += 1

            await session.flush()
            print(f"   [SUCCESS] ✅ {title} ({self.stats['code_templates'] % 3} templates)")

            return algorithm

        except Exception as e:
            print(f"   [ERROR] ❌ Failed to seed {title}: {str(e)}")
            self.stats["errors"] += 1
            await session.rollback()
            return None

    async def run_seeding(self) -> None:
        """Main seeding workflow"""
        print("=" * 60)
        print("DATABASE SEEDING - Algorithm Reference Platform")
        print("=" * 60)

        # Check content directory
        if not self.content_dir.exists():
            print(f"\n[ERROR] Content directory not found: {self.content_dir}")
            print("Please run content generation first:")
            print("   cd content-generator && python generate_algorithms.py --generate")
            return

        # Find JSON files
        json_files = list(self.content_dir.glob("*.json"))
        json_files = [f for f in json_files if not f.name.startswith("cost_")]

        if not json_files:
            print(f"\n[ERROR] No JSON files found in: {self.content_dir}")
            return

        print(f"\n[INFO] Found {len(json_files)} algorithm files")

        async with AsyncSessionLocal() as session:
            try:
                # Seed base data
                difficulty_map = await self.seed_base_data(session)

                # Seed algorithms
                print(f"\n[2/4] Seeding {len(json_files)} algorithms...")

                for idx, json_file in enumerate(json_files, 1):
                    print(f"\n[{idx}/{len(json_files)}] Processing: {json_file.name}")

                    # Load JSON content
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            content = json.load(f)
                    except Exception as e:
                        print(f"   [ERROR] Failed to load JSON: {e}")
                        self.stats["errors"] += 1
                        continue

                    # Seed algorithm
                    await self.seed_algorithm(session, content, difficulty_map)

                # Commit all changes
                print(f"\n[3/4] Committing changes to database...")
                await session.commit()
                print("[OK] Changes committed successfully")

            except Exception as e:
                print(f"\n[ERROR] Seeding failed: {str(e)}")
                await session.rollback()
                raise

        # Print final report
        print("\n" + "=" * 60)
        print("SEEDING COMPLETE")
        print("=" * 60)
        print(f"\n[RESULTS]")
        print(f"   ✅ Algorithms:      {self.stats['algorithms']}")
        print(f"   ✅ Code Templates:  {self.stats['code_templates']}")
        print(f"   ✅ Categories:      {self.stats['categories']}")
        print(f"   ✅ Difficulties:    {self.stats['difficulties']}")
        print(f"   ✅ Languages:       {self.stats['languages']}")
        print(f"   ⏭️  Skipped:        {self.stats['skipped']}")
        print(f"   ❌ Errors:          {self.stats['errors']}")

        # Verification queries
        print(f"\n[4/4] Running verification queries...")
        async with AsyncSessionLocal() as session:
            # Count algorithms
            result = await session.execute(select(Algorithm))
            all_algorithms = result.scalars().all()
            print(f"   Total algorithms in DB: {len(all_algorithms)}")

            # Count code templates
            result = await session.execute(select(CodeTemplate))
            all_templates = result.scalars().all()
            print(f"   Total code templates in DB: {len(all_templates)}")

        print("\n[OK] Verification complete!")


async def main():
    """Entry point"""
    # Path to generated content
    backend_dir = Path(__file__).parent.parent
    project_root = backend_dir.parent
    content_dir = project_root / "content-generator" / "generated"

    print(f"\n[INFO] Content directory: {content_dir}")
    print(f"[INFO] Backend directory: {backend_dir}")

    # Run seeding
    seeder = DatabaseSeeder(content_dir)
    await seeder.run_seeding()


if __name__ == "__main__":
    asyncio.run(main())
