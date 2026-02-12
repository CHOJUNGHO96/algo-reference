"""Test PostgreSQL connection with asyncpg"""
import asyncio
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Windows compatibility
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test_connection():
    """Test database connection with timeout settings"""
    # Get connection details from environment or use defaults
    from app.core.config import settings

    print(f"Testing connection to: {settings.DATABASE_URL}")
    print(f"Using schema: {settings.POSTGRES_SCHEMA}")

    engine = create_async_engine(
        str(settings.DATABASE_URL),
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_timeout=settings.DB_POOL_TIMEOUT,
        connect_args={
            "timeout": settings.DB_CONNECT_TIMEOUT,
            "command_timeout": settings.DB_COMMAND_TIMEOUT,
            "server_settings": {"search_path": settings.POSTGRES_SCHEMA},
            "ssl": settings.DB_SSL_MODE,
        },
    )

    try:
        print("\n🔄 Attempting connection...")
        async with engine.connect() as conn:
            # Test basic connection
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ Connection successful!")
            print(f"📊 PostgreSQL version: {version[:80]}...")

            # Test schema
            result = await conn.execute(text("SELECT current_schema()"))
            schema = result.scalar()
            print(f"📁 Current schema: {schema}")

            # Test if schema exists
            result = await conn.execute(text(
                "SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema"
            ), {"schema": settings.POSTGRES_SCHEMA})
            schema_exists = result.scalar()
            if schema_exists:
                print(f"✅ Schema '{settings.POSTGRES_SCHEMA}' exists")
            else:
                print(f"⚠️  Schema '{settings.POSTGRES_SCHEMA}' does NOT exist")

            print("\n✅ All connection tests passed!")

    except asyncio.TimeoutError:
        print("❌ Connection timeout - check network and server availability")
        print("   - Verify server is running at the configured address")
        print("   - Check firewall settings")
        print("   - Increase timeout values if needed")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("  1. Check if PostgreSQL server is running")
        print("  2. Verify connection details in .env file")
        print("  3. Test with psql: psql -h <host> -U <user> -d <database>")
        print("  4. Check server logs for authentication errors")
    finally:
        await engine.dispose()

async def test_pool():
    """Test connection pool limits"""
    from app.core.config import settings

    print("\n🔄 Testing connection pool...")
    print(f"Pool configuration: size={settings.DB_POOL_SIZE}, overflow={settings.DB_MAX_OVERFLOW}")

    engine = create_async_engine(
        str(settings.DATABASE_URL),
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_timeout=settings.DB_POOL_TIMEOUT,
        connect_args={
            "timeout": settings.DB_CONNECT_TIMEOUT,
            "command_timeout": settings.DB_COMMAND_TIMEOUT,
            "ssl": settings.DB_SSL_MODE
        },
    )

    try:
        # Try to create max connections (pool_size + max_overflow)
        max_connections = settings.DB_POOL_SIZE + settings.DB_MAX_OVERFLOW
        print(f"Attempting to create {max_connections} concurrent connections...")

        tasks = [engine.connect() for _ in range(max_connections)]
        connections = await asyncio.gather(*tasks)
        print(f"✅ Successfully created {len(connections)} concurrent connections")

        # Clean up
        for conn in connections:
            await conn.close()

        print("✅ Pool test passed!")
    except Exception as e:
        print(f"❌ Pool test failed: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    print("=" * 70)
    print("PostgreSQL Connection Test")
    print("=" * 70)
    asyncio.run(test_connection())
    asyncio.run(test_pool())
    print("\n" + "=" * 70)
    print("Test completed!")
    print("=" * 70)
