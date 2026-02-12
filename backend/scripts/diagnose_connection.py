"""PostgreSQL 연결 진단 스크립트"""
import socket
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings

def test_tcp_connection():
    """TCP 소켓 레벨 연결 테스트"""
    print("=" * 70)
    print("1. TCP 소켓 연결 테스트")
    print("=" * 70)

    host = settings.POSTGRES_SERVER
    port = settings.POSTGRES_PORT

    try:
        print(f"연결 시도: {host}:{port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))

        if result == 0:
            print(f"✅ TCP 연결 성공: {host}:{port}")

            # Keep-alive 테스트
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            print("✅ Keep-alive 설정 성공")

            # 간단한 데이터 전송 테스트
            try:
                sock.send(b'\x00')
                print("✅ 데이터 전송 테스트 성공")
            except Exception as e:
                print(f"❌ 데이터 전송 실패: {e}")

        else:
            print(f"❌ TCP 연결 실패: 에러 코드 {result}")

        sock.close()
    except Exception as e:
        print(f"❌ 연결 테스트 실패: {e}")

def test_psql_command():
    """psql 명령어로 연결 테스트"""
    print("\n" + "=" * 70)
    print("2. psql 명령어 연결 테스트")
    print("=" * 70)

    print("\n다음 명령어를 직접 실행해보세요:")
    print(f"psql -h {settings.POSTGRES_SERVER} -p {settings.POSTGRES_PORT} -U {settings.POSTGRES_USER} -d {settings.POSTGRES_DB}")
    print("\n만약 psql이 연결된다면:")
    print("  → asyncpg 특정 문제")
    print("만약 psql도 연결 안 된다면:")
    print("  → 서버 설정 또는 네트워크 문제")

def check_postgresql_server_logs():
    """PostgreSQL 서버 로그 확인 가이드"""
    print("\n" + "=" * 70)
    print("3. PostgreSQL 서버 로그 확인 방법")
    print("=" * 70)

    print(f"\n192.168.164.1 서버에 접속해서 다음 명령어 실행:")
    print("\n# Docker로 실행 중인 경우:")
    print("docker logs <postgres-container-name> --tail 100")
    print("\n# 직접 실행 중인 경우:")
    print("tail -f /var/log/postgresql/postgresql-*.log")
    print("\n찾아야 할 내용:")
    print("  - 'connection reset by peer'")
    print("  - 'no pg_hba.conf entry'")
    print("  - 'SSL required'")
    print("  - 'authentication failed'")

def check_server_config():
    """서버 설정 확인 가이드"""
    print("\n" + "=" * 70)
    print("4. PostgreSQL 서버 설정 확인")
    print("=" * 70)

    print(f"\n192.168.164.1 서버에서 다음 확인:")

    print("\n## A. SSL 설정 확인")
    print("psql -h 192.168.164.1 -U postgres -d postgres")
    print("postgres=# SHOW ssl;")
    print("postgres=# SHOW ssl_cert_file;")

    print("\n## B. pg_hba.conf 확인")
    print("cat /var/lib/postgresql/data/pg_hba.conf")
    print("\n필요한 라인:")
    print("host    all    all    192.168.164.0/24    md5")
    print("또는")
    print("host    all    all    0.0.0.0/0    md5")

    print("\n## C. postgresql.conf 확인")
    print("cat /var/lib/postgresql/data/postgresql.conf | grep -E '(listen_addresses|max_connections|ssl)'")

def check_network_firewall():
    """네트워크 및 방화벽 확인"""
    print("\n" + "=" * 70)
    print("5. 네트워크 및 방화벽 확인")
    print("=" * 70)

    print("\n## Windows 방화벽 확인")
    print("1. 제어판 → Windows Defender 방화벽")
    print("2. 고급 설정 → 아웃바운드 규칙")
    print("3. 포트 5432가 허용되어 있는지 확인")

    print("\n## 안티바이러스 소프트웨어")
    print("일부 안티바이러스가 데이터베이스 연결을 차단할 수 있음")
    print("임시로 비활성화하고 테스트해보기")

    print("\n## 라우터/스위치")
    print("네트워크 장비가 연결을 끊고 있을 수 있음")

def check_asyncpg_compatibility():
    """asyncpg 호환성 확인"""
    print("\n" + "=" * 70)
    print("6. asyncpg 및 PostgreSQL 버전 호환성")
    print("=" * 70)

    print("\n현재 설치된 버전:")
    try:
        import asyncpg
        print(f"asyncpg 버전: {asyncpg.__version__}")
    except ImportError:
        print("❌ asyncpg가 설치되지 않음")

    try:
        import sqlalchemy
        print(f"SQLAlchemy 버전: {sqlalchemy.__version__}")
    except ImportError:
        print("❌ SQLAlchemy가 설치되지 않음")

    print("\n서버 PostgreSQL 버전 확인 필요:")
    print("psql -h 192.168.164.1 -U postgres -c 'SELECT version();'")

def main():
    """모든 진단 실행"""
    print("\n")
    print("🔍 PostgreSQL 연결 진단 도구")
    print("=" * 70)
    print(f"대상 서버: {settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}")
    print(f"데이터베이스: {settings.POSTGRES_DB}")
    print(f"사용자: {settings.POSTGRES_USER}")
    print(f"스키마: {settings.POSTGRES_SCHEMA}")
    print("=" * 70)

    test_tcp_connection()
    test_psql_command()
    check_postgresql_server_logs()
    check_server_config()
    check_network_firewall()
    check_asyncpg_compatibility()

    print("\n" + "=" * 70)
    print("📋 원인 파악 우선순위")
    print("=" * 70)
    print("\n1순위: PostgreSQL 서버 로그 확인 (가장 정확한 정보)")
    print("2순위: psql 명령어로 직접 연결 시도")
    print("3순위: pg_hba.conf 설정 확인")
    print("4순위: SSL 요구사항 확인")
    print("5순위: 방화벽/네트워크 확인")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
