# ------------------------Heuristic based agentic model--------------------------
# import statistics

# class BehaviorAgent:
#     def analyze(self,completed):
#         if not completed:
#             return {"fav_category":"Unknown","avg_duration":0, "tasks_completed":0}
#         category_count = {}
#         durations = []
#         for task in completed:
#             cat = task.category if task.category else "Unknown"
#             category_count[cat] = category_count.get(cat,0)+1
            
#             if task.duration and str(task.duration).isdigit():
#                 durations.append(int(task.duration))
#         fav_category = max(category_count, key=category_count.get)
#         avg_duration = statistics.mean(durations) if durations else 0
#         return { "fav_category": fav_category, "avg_duration": round(avg_duration), "tasks_completed":len(completed)}
# # Workload Agent ---------
# class WorkloadAgent:
#     def analyze(self,pending):
#         priority_score = {"High": 3, "Medium": 2, "Low": 1}
#         load_score = sum(priority_score.get(t.priority,1) for t in pending) 
#         return {"pending_tasks": len(pending),
#                 "load_score": load_score}
# #-----identifying trends --------------
# class TrendAgent:
#     def analyze(self,completed):
#         if not completed:
#             return {
#                 "avg_completed_duration": 0,
#                 "total_history": 0
#             }
#         durations = [int(t.duration) for t in completed if t.duration and str(t.duration).isdigit()]
#         avg = statistics.mean(durations) if durations else 0
#         return {
#             "avg_completed_duration": round(avg),
#             "total_history": len(completed)
#         }
# #----Preditcing---------
# class PredictionAgent:
#     def predict(self, pending, behavior):
#         if not pending:
#             return None
#         priority_weight = {"High": 3, "Medium": 2, "Low": 1}
#         best_task = None
#         best_score = -1
#         for task in pending:
#             score = priority_weight.get(task.priority,1)
#             if task.duration and str(task.duration).isdigit():
#                 diff = abs(int(task.duration) - behavior["avg_duration"])
#                 score += max(0,10-diff)
#             if score > best_score:
#                 best_score = score
#                 best_task = task
#         return best_task
# # Scheduling task 
# class SchedulingAgent:
#     def schedule(self,pending,behavior):
#         if not pending:
#             return []
#         priority_weight = {"High":3, "Medium":2, "Low": 1}
#         scored_tasks = []
#         for task in pending:
#             score = priority_weight.get(task.priority,1)
            
#             if task.duration and str(task.duration).isdigit():
#                 # Prefer tasks close to your habit duration
#                 diff = abs(int(task.duration) - behavior["avg_duration"])
#                 score += max(0,10-diff)
#             scored_tasks.append((score,task))
#         # Sort tasks by best score
#         scored_tasks.sort(key=lambda x: x[0],reverse = True)
#         return [t[1] for t in scored_tasks]
# # Decision Agent
# class DecisionAgent:
#     def decide(self,behavior,workload,weather,predicted):
#         advice = []
#         if workload["load_score"] > 10:
#             advice.append("Heavy workload detected. Focus on high priority tasks.")
#         if workload["pending_tasks"] == 0:
#             advice.append("No pending tasks. Great productivity!")
#         if behavior["fav_category"] != "Unknown":
#             advice.append(f"You perform best in {behavior['fav_category']} tasks.")
#         if behavior["avg_duration"] > 60:
#             advice.append("Tasks are taking longer than expected.")
#         if predicted:
#             advice.append(
#                 f"Recommended next task: {predicted.title}"
#             )
#         if "rain" in weather.lower():
#             advice.append("Weather alert: prefer indoor tasks.")
#         return advice
# # Report Agent
# class ReportAgent:
#     def generate(self,behavior, workload, trends, predicted, decisions, schedule):
#         # report = "\n Productivity Intelligence Report\n"
#         # report += "-" * 40 + "\n"
#         # report += f"Completed Tasks: {behavior['tasks_completed']}\n"
#         # report += f"Prefered Category: {behavior['fav_category']}\n"
#         # report += f"Average Duration: {behavior['avg_duration']} mins\n\n"
#         # report += f"Pending Tasks: {workload['pending_tasks']}\n"
#         # report += f"Workload Score: {workload['load_score']}\n\n"
#         # report += "Habit Trends:\n"
#         # report += f"- Avg Completion Duration: {trends['avg_completed_duration']} mins\n"
#         # report += f"- Total Completed: {trends['total_history']}\n\n"
#         # if predicted:
#             # report += f"Best Next Task: {predicted.get('title')}\n\n"
#         report = "Productivity Report\n"
#         report += f"**Done: {behavior['tasks_completed']} | Top Cart: {behavior['fav_category']} | Avg: {trends['avg_completed_duration']}m\n"
#         report += f"**Pending: {workload['pending_tasks']} | Load Score: {workload['load_score']}\n\n"

#         # for new schedule 

#         if schedule:
#             report += "Recommended Task Order:\n"
#             for i, t in enumerate(schedule[:3],1):
#                 report += f"{i}.{t.title} ({t.priority})\n"
            
#         report += "\n**Agent Recommendations:**\n"
#         for d in decisions:
#             report += f"- {d}\n"
#         return report
# # Master Agent--------
# class MasterAgent:
#     def __init__(self):
#         self.behavior_agent = BehaviorAgent()
#         self.workload_agent = WorkloadAgent()
#         self.trend_agent = TrendAgent()
#         self.prediction_agent =  PredictionAgent()
#         self.scheduling_agent = SchedulingAgent()
#         self.decision_agent = DecisionAgent()
#         self.report_agent = ReportAgent()
#     def run(self,db_tasks, weather= "Clear"):
#         completed = [t for t in db_tasks if t.completed]
#         pending = [t for t in db_tasks if not t.completed]
#         # tasks = context.get("tasks", [])
#         # weather = context.get("weather","")
        
#         behavior = self.behavior_agent.analyze(completed)
#         workload = self.workload_agent.analyze(pending)
#         trends = self.trend_agent.analyze(completed)
#         predicted = self.prediction_agent.predict(pending,behavior)
#         schedule = self.scheduling_agent.schedule(pending, behavior)
#         decisions = self.decision_agent.decide(behavior, workload, weather, predicted)

#         return self.report_agent.generate(behavior, workload,trends, predicted, decisions, schedule)

#------------------------Advanced llm-rag induced analytical_agent with context-injection (RAG) ----------
import statistics
import datetime
import os
from openai import OpenAI
class BehaviorAgent:
    def analyze(self,completed):
        if not completed:
            return {"fav_category": "Unknown", "avg_duration": 0, "tasks_completed":0,"history_summary":[]}
        category_count = {}
        durations = []
        for task in completed:
            cat = task.category if task.category else "Unknown"
            category_count[cat] = category_count.get(cat,0) + 1
            if hasattr(task, 'duration') and str(task.duration).isdigit():
                durations.append(int(task.duration))
        fav_category = max(category_count, key= category_count.get)
        avg_duration = statistics.mean(durations) if durations else 0
        return {
            "fav_category": fav_category,
            "avg_duration": round(avg_duration),
            "tasks_completed": len(completed),
            # RAH Providing the last 5 completed tasks so the LLM understands recent context.
            "history_summary": [f"{t.title} ({t.category})" for t in completed[-5:]]
        }
class WorkloadAgent:
    def analyze(self,pending):
        priority_score = {"High":3, "Medium":2, "Low":1}
        load_score = sum(priority_score.get(t.priority,1) for t in pending)
        # add task aging, so that llm can see which tasks are stalled or not yet completed
        task_details = []
        for t in pending:
            # we will use created_at 
            age_str = ""
            # check if task are pending from long time.
            if hasattr(t, 'created_at') and t.created_at:
                days_old = (datetime.datetime.now() - t.created_at).days
                if days_old == 0:
                    age_str = "(Added: Today)"
                else:
                    age_str = f", Age: {days_old} days"
            task_info = f"-{t.title} [Priority: {t.priority}, Time: {t.duration}m]{age_str}"
            task_details.append(task_info)
        return {
            "pending_tasks": len(pending),
            "load_score": load_score,
            # semantic RAG providing a list of current tasks so the LLM can prioritize them
            "task_details": task_details
        }
#------TrendAgent for raw data extraction-------------------
class TrendAgent:
    def analyze(self, completed):
        if not completed:
            return {"avg_completed_duration": 0, "total_history": 0}
        durations = [int(t.duration)for t in completed if hasattr(t, 'duration') and str(t.duration).isdigit()]
        avg = statistics.mean(durations) if durations else 0
        return {"avg_completed_duration": round(avg), "total_history": len(completed)}
#----------------Simple Decision Agent only use heuristic data (No llm)-----------------------
class SimpleDecisionAgent:
    def generate(self,behavior,workload):
        advice = []
        if workload["load_score"] > 7:
            advice.append("Heavy Workload. Focus on high priority tasks")
        if workload['pending_tasks'] == 0:
            advice.append("No pending tasks. You're doing great.")
        if behavior["fav_category"] != "Unknown":
            advice.append(f"You perform best in {behavior['fav_category']} tasks.")
        if behavior["avg_duration"] > 60:
            advice.append("Tasks are taking longer than usual.")
        return "\n".join(advice)
    
#-----LLM rasoning Agent in place of heuristic engine it will run when we want it using openai.--------------
class ReasoningAgent:
    def __init__(self, api_key = None):
        # Configuring api key again so that the agent can work standalone if needed.
        # if api_key:
        #     genai.configure(api_key = api_key)
        # self.model = genai.GenerativeModel('gemini-1.5-flask')
        # using openai
        self.client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

    async def generative_intelligence(self, behavior, workload,weather):
        # The agent uses LLM to reason through the data provided by other agents.
        # Constructing the RAG Prompt
        weather = weather or "Clear"
        current_time = datetime.now().strftime("%A, %b, %d, %H:%M") # add temporal function 
        
        prompt = f"""
        You are a elite productivity stratigist and Agent_master.
        Your goal is to analyse the user's current situation and provide tactical, high-level advice.
        Today is {current_time}.

        ### ENVIRONMENT & HABITS
        - Current Weather: {weather}
        - User's Productivity Peak: Performs best in '{behavior['fav_category']}' tasks.
        - Habitual Task Length: {behavior['avg_duration']} minutes.
        - Recent Success: {",".join(behavior['history_summary']) if behavior['history_summary'] else "None yet."}

        ### CURRENT BACKLOG (The Data)
        - Pending Tasks Count: {workload['pending_tasks']}
        - System Load Score: {workload['load_score']} (Scale: <5 chill, ==7 Busy, >15 Overload)
        - Active Tasks: {",".join(workload['task_details'])}

        ### INSTRUCTIONS
        1. Compare weather to task list (e.g., Don't suggest outdoor tasks if rainy).
        2. Identify the 'stale' tasks (highest age) and give a nudge.
        3. Recommend the 'Best Next Move' matching the user's habit of {behavior['avg_duration']}m.
        4. Use a wise, mentor-like tone. Format in Markdown.
        """
        try:
            response = self.client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = [
                    {"role":"user","content":prompt}
                ],
                temperature = 0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return (
                "Agent connection lost.\n\n"
                f"You have {workload['pending_tasks']} tasks pending "
                f"with load score {workload['load_score']}."
            )
        
class MasterAgent:
    def __init__(self,api_key=None):
        self.behavior_agent = BehaviorAgent()
        self.workload_agent = WorkloadAgent()
        self.trend_agent = TrendAgent()
        self.reasoning_agent = ReasoningAgent(api_key=api_key)
    async def run(self,tasks, context_data, use_llm: bool=False):
        """Main entry point for the agentic analysis"""
        completed = [t for t in tasks if t.completed]
        pending = [t for t in tasks if not t.completed]
        # Retrieval & HEURISTIC Analysis 
        behavior = self.behavior_agent.analyze(completed)
        workload = self.workload_agent.analyze(pending)
        trends = self.trend_agent.analyze(completed)
        # LLM control Reasoning (LLM intelligence)
        if use_llm:
            report = await self.reasoning_agent.generative_intelligence(behavior, workload, context_data)
        else:
            # Simple fallback if no llm to be used
            report = (
                f"Quick Report:\n"
                f"- Pending Tasks: {workload['pending_tasks']}\n"
                f"- Load Score: {workload['load_score']}\n"
                f"- Best Category: {behavior['fav_category']}"
                f"- Local Time: {context_data.get('local_time_str','N/A')}"
            )
        return report
    
    
        
        
