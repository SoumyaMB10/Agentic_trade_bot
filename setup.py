from setuptools import find_packages, setup

setup(name="agentic_trading_sysytem",
      version="0.0.1",
      author="soumya",
      author_email="mbsoumya10@gmail.com",
      packages=find_packages(),
      install_requires = ['lancedb','langchain','langgraph','tavily-python','polygon']
      )