from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent


@CrewBase
class Appdeveloper():
    """Appdeveloper crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            # type: ignore[index]
            config=self.agents_config['frontend_engineer'],
            verbose=True
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            # type: ignore[index]
            config=self.agents_config['backend_engineer'],
            verbose=True
        )

    @task
    def build_backend(self) -> Task:
        return Task(
            config=self.tasks_config['build_backend'],  # type: ignore[index]
            output_file="output/backend.js"
        )

    @task
    def build_frontend(self) -> Task:
        return Task(
            config=self.tasks_config['build_frontend'],  # type: ignore[index]
            output_file='output/index.html'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Appdeveloper crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
