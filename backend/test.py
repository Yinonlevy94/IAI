"""
test_app.py
backend tests - covers api endpoints and basic logic
run: pytest test_app.py -v
"""

import pytest
from app import create_app


@pytest.fixture
def client():
    """create test client for making requests"""
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()


class TestHealth:
    """make sure health check works"""
    
    def test_health_endpoint(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['status'] == 'ok'


class TestListUsers:
    """test getting all users"""
    
    def test_list_users(self, client):
        response = client.get('/api/users')
        assert response.status_code == 200
        data = response.json
        
        # should have users array and total count
        assert 'users' in data
        assert 'total' in data
        assert len(data['users']) > 0
    
    def test_email_not_exposed(self, client):
        """emails should never be in the response"""
        response = client.get('/api/users')
        users = response.json['users']
        
        for user in users:
            assert 'email' not in user


class TestSearch:
    """test search endpoint with query params"""
    
    def test_search_valid(self, client):
        response = client.get('/api/users/search?id=1')
        assert response.status_code == 200
        assert 'user' in response.json
    
    def test_search_missing_param(self, client):
        """search without id param should fail"""
        response = client.get('/api/users/search')
        assert response.status_code == 400
    
    def test_search_invalid_format(self, client):
        """search with bad id format should fail"""
        response = client.get('/api/users/search?id=invalid')
        assert response.status_code == 400


class TestSecurity:
    """security-related checks"""
    
    def test_security_headers(self, client):
        """make sure security headers are present"""
        response = client.get('/api/users')
        assert 'X-Content-Type-Options' in response.headers
        assert 'X-Frame-Options' in response.headers
    
    def test_email_never_exposed(self, client):
        """triple check emails aren't leaked anywhere"""
        # list endpoint
        response = client.get('/api/users')
        for user in response.json['users']:
            assert 'email' not in user
        
        # single user endpoint
        response = client.get('/api/users/1')
        assert 'email' not in response.json['user']
        
        # search endpoint
        response = client.get('/api/users/search?id=1')
        if response.json['user']:
            assert 'email' not in response.json['user']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
