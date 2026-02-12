"""Initial schema with all tables

Revision ID: 001
Revises:
Create Date: 2026-02-11 19:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Create difficulty_levels table
    op.create_table('difficulty_levels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('color', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_difficulty_levels_id'), 'difficulty_levels', ['id'], unique=False)

    # Create programming_languages table
    op.create_table('programming_languages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('extension', sa.String(length=10), nullable=False),
        sa.Column('prism_key', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_programming_languages_id'), 'programming_languages', ['id'], unique=False)
    op.create_index(op.f('ix_programming_languages_slug'), 'programming_languages', ['slug'], unique=True)

    # Create categories table
    op.create_table('categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('color', sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(['parent_id'], ['categories.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_index(op.f('ix_categories_slug'), 'categories', ['slug'], unique=True)

    # Create algorithms table
    op.create_table('algorithms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('slug', sa.String(length=200), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('difficulty_id', sa.Integer(), nullable=False),
        sa.Column('concept_summary', sa.Text(), nullable=False),
        sa.Column('core_formulas', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('thought_process', sa.Text(), nullable=True),
        sa.Column('application_conditions', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('time_complexity', sa.String(length=50), nullable=False),
        sa.Column('space_complexity', sa.String(length=50), nullable=False),
        sa.Column('problem_types', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('common_mistakes', sa.Text(), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('view_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('search_vector', postgresql.TSVECTOR(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['difficulty_id'], ['difficulty_levels.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_algorithms_category_difficulty', 'algorithms', ['category_id', 'difficulty_id'], unique=False)
    op.create_index(op.f('ix_algorithms_id'), 'algorithms', ['id'], unique=False)
    op.create_index(op.f('ix_algorithms_is_published'), 'algorithms', ['is_published'], unique=False)
    op.create_index('ix_algorithms_published_created', 'algorithms', ['is_published', 'created_at'], unique=False)
    op.create_index('ix_algorithms_search_vector', 'algorithms', ['search_vector'], unique=False, postgresql_using='gin')
    op.create_index(op.f('ix_algorithms_slug'), 'algorithms', ['slug'], unique=True)

    # Create code_templates table
    op.create_table('code_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('algorithm_id', sa.Integer(), nullable=False),
        sa.Column('language_id', sa.Integer(), nullable=False),
        sa.Column('code', sa.Text(), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['algorithm_id'], ['algorithms.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['language_id'], ['programming_languages.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_code_templates_algorithm_id'), 'code_templates', ['algorithm_id'], unique=False)
    op.create_index(op.f('ix_code_templates_id'), 'code_templates', ['id'], unique=False)
    op.create_index('ix_code_templates_algorithm_language', 'code_templates', ['algorithm_id', 'language_id'], unique=True)

    # Insert seed data for difficulty_levels
    op.execute("""
        INSERT INTO difficulty_levels (id, name, color) VALUES
        (1, 'Easy', '#22c55e'),
        (2, 'Medium', '#f59e0b'),
        (3, 'Hard', '#ef4444')
    """)

    # Insert seed data for programming_languages
    op.execute("""
        INSERT INTO programming_languages (id, name, slug, extension, prism_key) VALUES
        (1, 'Python', 'python', '.py', 'python'),
        (2, 'JavaScript', 'javascript', '.js', 'javascript'),
        (3, 'TypeScript', 'typescript', '.ts', 'typescript'),
        (4, 'Java', 'java', '.java', 'java'),
        (5, 'C++', 'cpp', '.cpp', 'cpp'),
        (6, 'Go', 'go', '.go', 'go'),
        (7, 'Rust', 'rust', '.rs', 'rust')
    """)

    # Insert seed data for categories
    op.execute("""
        INSERT INTO categories (id, name, slug, description, display_order, parent_id, color) VALUES
        (1, 'Two Pointer', 'two-pointer', 'Algorithms using two pointers for array/string manipulation', 1, NULL, '#0969da'),
        (2, 'Sliding Window', 'sliding-window', 'Techniques for processing sequential data in windows', 2, NULL, '#1f883d'),
        (3, 'Binary Search', 'binary-search', 'Efficient searching in sorted arrays', 3, NULL, '#8250df'),
        (4, 'Dynamic Programming', 'dynamic-programming', 'Optimization through subproblem solutions', 4, NULL, '#bf3989'),
        (5, 'Greedy', 'greedy', 'Locally optimal choices for global optimization', 5, NULL, '#d29922'),
        (6, 'Backtracking', 'backtracking', 'Exploring all possible solutions systematically', 6, NULL, '#cf222e'),
        (7, 'Graph Algorithms', 'graph-algorithms', 'Algorithms for graph traversal and analysis', 7, NULL, '#0969da'),
        (8, 'Tree Algorithms', 'tree-algorithms', 'Algorithms for tree traversal and manipulation', 8, NULL, '#1f883d'),
        (9, 'Heap/Priority Queue', 'heap-priority-queue', 'Priority-based data structure algorithms', 9, NULL, '#8250df'),
        (10, 'String Algorithms', 'string-algorithms', 'Pattern matching and string manipulation', 10, NULL, '#bf3989')
    """)

    # Insert default admin user (password: admin123 hashed with bcrypt)
    op.execute("""
        INSERT INTO users (email, password_hash, role) VALUES
        ('admin@algoref.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5aeWZ.JbHDUDy', 'admin')
    """)


def downgrade() -> None:
    op.drop_table('code_templates')
    op.drop_table('algorithms')
    op.drop_table('categories')
    op.drop_table('programming_languages')
    op.drop_table('difficulty_levels')
    op.drop_table('users')
