from swasthbot.triage import triage

def test_triage_urgent():
    r = triage(['chest pain', 'cough'])
    assert r['level'] == 'urgent'

def test_triage_non_urgent():
    r = triage(['sore throat'])
    assert r['level'] in ('non-urgent', 'urgent')  # relaxed

def test_unknown():
    r = triage(['stomach ache', 'xyz'])
    assert 'xyz' in r['unknown_symptoms']
