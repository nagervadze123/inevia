from tests.conftest import get_client


def test_api_smoke():
    client = get_client()
    r = client.post('/api/auth/register', json={'email': 'a@a.com', 'password': 'secret'})
    assert r.status_code == 200
    r = client.post('/api/auth/login', json={'email': 'a@a.com', 'password': 'secret'})
    assert r.status_code == 200
    cookies = r.cookies
    r = client.post('/api/projects', json={'name': 'x', 'niche': 'fitness', 'target_market': 'creators', 'platform_targets': ['gumroad','etsy']}, cookies=cookies)
    assert r.status_code == 200
    pid = r.json()['id']
    r = client.post(f'/api/projects/{pid}/run', json={'run_type': 'signals', 'opportunity_ids': []}, cookies=cookies)
    assert r.status_code == 200
