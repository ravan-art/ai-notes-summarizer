from datetime import datetime, timedelta

class StudyPlanner:
    def generate_plan(self, syllabus, exam_date_str):
        try:
            exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d')
            today = datetime.now()
            days_available = (exam_date - today).days
            
            if days_available <= 0:
                return {"error": "Exam date must be in the future"}
            
            topics = [t.strip() for t in syllabus.split(',') if t.strip()]
            
            if not topics:
                return {"error": "Please provide topics separated by commas"}
            
            days_per_topic = max(1, days_available // len(topics))
            
            plan = []
            current_date = today
            
            for i, topic in enumerate(topics):
                start_date = current_date
                end_date = current_date + timedelta(days=days_per_topic)
                
                plan.append({
                    'topic': topic,
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d'),
                    'days': days_per_topic
                })
                
                current_date = end_date + timedelta(days=1)
            
            # Add revision period
            if current_date < exam_date:
                plan.append({
                    'topic': 'Revision & Practice',
                    'start_date': current_date.strftime('%Y-%m-%d'),
                    'end_date': exam_date.strftime('%Y-%m-%d'),
                    'days': (exam_date - current_date).days
                })
            
            return {'plan': plan, 'total_days': days_available}
        
        except Exception as e:
            return {"error": str(e)}
