import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from src.infrastructure.db.base import Base
from src.infrastructure.db.main import get_session
import uuid
from src import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL)

TestAsyncSession = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False
)

@pytest_asyncio.fixture(scope="session")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="module")
async def test_client(db_session):
    # Мокаем функции инициализации БД И саму сессию
    with patch('src.infrastructure.db.main.init_db', new_callable=AsyncMock), \
         patch('src.infrastructure.db.main.close_db', new_callable=AsyncMock), \
         patch('src.infrastructure.db.main.AsyncSession', TestAsyncSession):
        
        # ИСПРАВЛЕНИЕ: Правильное переопределение зависимости
        async def override_get_session():
            async with TestAsyncSession() as session:
                try:
                    yield session
                except Exception:
                    await session.rollback()
                    raise
                finally:
                    await session.close()
        
        app.dependency_overrides[get_session] = override_get_session
        
        transport = ASGITransport(app=app)
        
        async with AsyncClient(transport=transport, base_url='http://test') as client:
            yield client
        
        # Очищаем переопределения
        app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def created_profile(test_client: AsyncClient):
    unique_id = uuid.uuid4()
    
    response = await test_client.post("/api/0.1.0/profiles/", json={
            "name": "John",
            "email": f"john.doe.{unique_id}@example.com",
            "external_id": f"123456_{unique_id}",
            "surname": "Doe",
            "birthday": "1991-01-01",
            "wallet_address": f"0x1234567890_{unique_id}"
        })
    assert response.status_code == 201
    return response.json()


@pytest_asyncio.fixture
async def created_talent(test_client: AsyncClient, created_profile: dict):
    
    unique_data = uuid.uuid4()

    talent_to_add = {
        'bio': 'amazing developer',
        'role': f'{unique_data}java dev',
        'portfolio_link': 'https://something.com',
        'project_price': 299.0,
        'rating': 50
    }

    profile_id = created_profile['id']

    response = await test_client.post(f'/api/0.1.0/profiles/{profile_id}/talent/',
                                    json=talent_to_add)
    
    assert response.status_code == 201
    return response.json()