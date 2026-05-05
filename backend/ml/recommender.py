"""
AI-powered study recommendation engine.
Generates personalised, priority-ranked tips based on student inputs and predicted score.
"""
from typing import List, Dict


def get_recommendations(
    study_hours: float,
    attendance: float,
    sleep_hours: float,
    previous_score: float,
    extra_curricular: bool,
    predicted_score: float
) -> List[Dict]:
    """
    Analyse student profile and return a list of personalised recommendations.

    Each recommendation dict has:
        icon, title, description, priority  ('high' | 'medium' | 'low' | 'success')
    """
    tips: List[Dict] = []

    # ── Study Hours ───────────────────────────────────────────
    if study_hours < 2:
        tips.append({
            'icon': '📚',
            'title': 'Critically Low Study Hours',
            'description': (
                f'You are studying only {study_hours:.1f} hrs/day. Students who score '
                'above 75% typically study at least 5–6 hours daily. '
                'Create a timetable with dedicated study blocks and eliminate distractions.'
            ),
            'priority': 'high'
        })
    elif study_hours < 4:
        tips.append({
            'icon': '📖',
            'title': 'Increase Your Daily Study Time',
            'description': (
                f'{study_hours:.1f} hrs/day is below the recommended 4–6 hours. '
                'Try the Pomodoro technique: 25-min focused sessions with 5-min breaks. '
                'Even one extra hour daily can boost your score by 8–10 points.'
            ),
            'priority': 'medium'
        })
    elif study_hours >= 8:
        tips.append({
            'icon': '⚡',
            'title': 'Study Smarter, Not Just Longer',
            'description': (
                f'Great dedication! You study {study_hours:.1f} hrs/day. '
                'At this intensity, focus on quality over quantity — use active recall, '
                'spaced repetition (Anki), and mind maps to maximise retention.'
            ),
            'priority': 'low'
        })

    # ── Attendance ────────────────────────────────────────────
    if attendance < 60:
        tips.append({
            'icon': '🏫',
            'title': 'Attendance is Critically Low',
            'description': (
                f'Your attendance is {attendance:.0f}% — below the 60% pass threshold in most '
                'institutions. You are missing crucial in-class explanations and Q&A sessions. '
                'Attend every class and catch up on missed notes immediately.'
            ),
            'priority': 'high'
        })
    elif attendance < 75:
        tips.append({
            'icon': '🎯',
            'title': 'Improve Your Class Attendance',
            'description': (
                f'{attendance:.0f}% attendance puts you at risk. Aim for 85%+. '
                'Students with higher attendance understand exam patterns better and '
                'build stronger relationships with teachers for guidance.'
            ),
            'priority': 'high'
        })
    elif attendance >= 95:
        tips.append({
            'icon': '✅',
            'title': 'Excellent Attendance — Keep It Up!',
            'description': (
                f'Outstanding! {attendance:.0f}% attendance is a top-percentile habit. '
                'Use class time to ask questions, clarify doubts, and engage actively. '
                'This consistency will reflect strongly in your results.'
            ),
            'priority': 'success'
        })

    # ── Sleep ─────────────────────────────────────────────────
    if sleep_hours < 5.5:
        tips.append({
            'icon': '😴',
            'title': 'Sleep Deprivation is Hurting Your Performance',
            'description': (
                f'Only {sleep_hours:.1f} hrs of sleep severely impacts memory consolidation and focus. '
                'Research shows sleep deprivation reduces cognitive performance by 20–40%. '
                'Aim for 7–8 hours — set a consistent bedtime and avoid screens 1 hour before sleep.'
            ),
            'priority': 'high'
        })
    elif sleep_hours < 7:
        tips.append({
            'icon': '🌙',
            'title': 'Optimise Your Sleep Schedule',
            'description': (
                f'{sleep_hours:.1f} hrs of sleep is below optimal (7–8 hrs). '
                'During sleep, your brain consolidates information learned during the day. '
                'A short 20-min afternoon nap can also boost alertness significantly.'
            ),
            'priority': 'medium'
        })
    elif sleep_hours > 9:
        tips.append({
            'icon': '☀️',
            'title': 'Balance Sleep and Productive Hours',
            'description': (
                f'You sleep {sleep_hours:.1f} hrs — slightly above optimal. '
                'Oversleeping can cause grogginess. Stick to 7–8 hrs for peak mental performance. '
                'Use a consistent wake time even on weekends.'
            ),
            'priority': 'low'
        })

    # ── Previous Score ────────────────────────────────────────
    if previous_score < 40:
        tips.append({
            'icon': '🔄',
            'title': 'Build From Your Previous Performance',
            'description': (
                f'A previous score of {previous_score:.0f}% indicates foundational gaps. '
                'Start by revisiting core concepts from the beginning. '
                'Seek help from teachers or tutors, use YouTube tutorials, and practice past papers daily.'
            ),
            'priority': 'high'
        })
    elif previous_score >= 80:
        tips.append({
            'icon': '🏆',
            'title': 'Leverage Your Strong Track Record',
            'description': (
                f'Excellent previous score of {previous_score:.0f}%! '
                'Maintain momentum by attempting advanced problems, participating in academic competitions, '
                'and teaching concepts to peers — the best way to reinforce your own understanding.'
            ),
            'priority': 'success'
        })

    # ── Extra-Curricular ──────────────────────────────────────
    if not extra_curricular:
        tips.append({
            'icon': '🎭',
            'title': 'Consider Joining Extra-Curricular Activities',
            'description': (
                'Students involved in clubs, sports, or volunteering develop better time management, '
                'stress resilience, and social skills — all of which positively impact academic performance. '
                'Even one activity per week makes a measurable difference.'
            ),
            'priority': 'low'
        })

    # ── Predicted Score Based Tips ────────────────────────────
    if predicted_score >= 85:
        tips.append({
            'icon': '🌟',
            'title': 'You Are on Track for Excellence!',
            'description': (
                f'Your predicted score of {predicted_score:.1f}% places you in the top tier. '
                'Focus on consistency, review edge cases, and practice time management in mock exams. '
                'Consider helping classmates — peer teaching deepens your own mastery.'
            ),
            'priority': 'success'
        })
    elif predicted_score >= 65:
        tips.append({
            'icon': '📈',
            'title': 'Good Progress — Push for the Next Level',
            'description': (
                f'Predicted score: {predicted_score:.1f}%. You are performing well! '
                'Identify your 2–3 weakest subjects and dedicate extra time there. '
                'Use past exam papers to practise under timed conditions.'
            ),
            'priority': 'medium'
        })
    elif predicted_score < 50:
        tips.append({
            'icon': '🚨',
            'title': 'Urgent: Academic Intervention Needed',
            'description': (
                f'Predicted score of {predicted_score:.1f}% is below passing threshold. '
                'This is a wake-up call. Create an emergency study plan, talk to your teacher today, '
                'and commit to changing at least 2 habits from this recommendation list immediately.'
            ),
            'priority': 'high'
        })

    # ── Sort by priority ──────────────────────────────────────
    priority_order = {'high': 0, 'medium': 1, 'low': 2, 'success': 3}
    tips.sort(key=lambda t: priority_order.get(t['priority'], 99))

    return tips
