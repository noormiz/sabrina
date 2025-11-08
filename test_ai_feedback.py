from ai_feedback import get_ai_chat_response, get_ai_explanation

def test_mock_chat():
    print("--- test_mock_chat ---")
    resp = get_ai_chat_response('MOCK', 'Why does fuel matter for rockets?')
    print('Chat response:', resp)
    assert 'Mock AI Reply' in resp

def test_mock_explain():
    print("--- test_mock_explain ---")
    state = {'fuel': 5.0, 'velocity_km_s': 0.1, 'altitude_km': 100}
    resp = get_ai_explanation('MOCK', 'LOW_FUEL_LAUNCH', state)
    print('Explanation:', resp)
    assert 'Mission Failure' in resp or 'Try' in resp

if __name__ == '__main__':
    test_mock_chat()
    test_mock_explain()
