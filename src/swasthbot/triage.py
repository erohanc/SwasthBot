from typing import List, Dict

SUPPORTED = {
    'fever', 'cough', 'chest_pain', 'shortness_of_breath', 'headache', 'sore_throat',
    'abdominal_pain', 'nausea', 'vomiting', 'diarrhea', 'rash', 'weakness', 'dizziness'
}

def triage(symptoms: List[str], age: int | None = None) -> Dict:
    s = set(x.strip().lower().replace(' ', '_') for x in symptoms if x)
    unknown = [x for x in s if x not in SUPPORTED]

    # Basic rules (illustrative only)
    urgent = False
    reasons = []

    if 'chest_pain' in s or ('shortness_of_breath' in s and 'cough' in s):
        urgent = True
        reasons.append('Possible cardiopulmonary concern')
    if 'fever' in s and ('rash' in s or 'headache' in s) and (age and age < 5):
        urgent = True
        reasons.append('Fever with rash/headache in young child')
    if len(s) >= 4:
        reasons.append('Multiple concurrent symptoms')

    level = 'urgent' if urgent else 'non-urgent'
    recommendation = 'Seek emergency care immediately.' if urgent else 'Consult a clinician within 24-48 hours.'
    return {
        'level': level,
        'reasons': reasons or ['General advice only; not a diagnosis.'],
        'unknown_symptoms': unknown,
    }
