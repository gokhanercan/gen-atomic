# About gen-atomic

[![Python application](https://github.com/gokhanercan/gen-atomic/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/gokhanercan/gen-atomic/actions/workflows/python-app.yml)
[![Demo](https://img.shields.io/badge/Streamlit_Demo-Visit-blue.svg)](https://gen-atomic.streamlit.app/)

An LLM code **gen**eration and benchmarking framework aiming to support a wide range of **atom**ic _language units_, from compiled to semi-structured markups.
Please refer to the [Project Glossary on the Documentation page](DOC.md) for clarification.

Here is the initial sketch. We will share more about the theoretical foundation and goals of the project. Some hints: Atomic Design, Flow Engineering, Specification-by-example.
![image](https://github.com/gokhanercan/gen-atomic/assets/1479777/912bada9-f907-4a4a-9ea7-341d3da60403)
https://pitch.com/v/gen-atomic-tyqhkw

# Getting Started

## See the Demo

Check out the [streamlit app](https://gen-atomic.streamlit.app/) to get an idea of what we are trying to accomplish. Sorry for the bad UX. We are new to streamlit.

## Installing gen-atomic

1. Extract project files to a folder
2. Run the setup by typing

   ```
   .\setup.sh
   ```

## Run the Code

1. Run main method of the file 'ExperimentHost.py'. You will see the default experiment/benchmark scores like the following:

```
-- REGEXVAL EXPERIMENT --
+---------------+-----------------------+-----------------+---------------+--------------------+------------------------+---------------------+---------------------+----------------+--------------------+--------------------+-----------------+
|               |   ol-codellama:7b (%) |   ol-llama3 (%) |   ol-phi3 (%) |   ol-codegemma (%) |   ol-codellama:70b (%) |   ol-llama3:70b (%) |   ol-starcoder2 (%) |   ol-gemma (%) |   ol-tinyllama (%) |   np-emailstub (%) |   np-random (%) |
|---------------+-----------------------+-----------------+---------------+--------------------+------------------------+---------------------+---------------------+----------------+--------------------+--------------------+-----------------|
| CorrectCase   |                 79.07 |           72.09 |         79.07 |              72.09 |                  69.77 |               72.09 |               86.05 |          69.77 |              67.44 |              11.63 |            0.00 |
| IncorrectCase |                 80.65 |           75.81 |         83.87 |              83.87 |                  82.26 |               80.65 |               77.42 |          85.48 |              87.10 |              95.16 |          100.00 |
| Overall       |                 80.00 |           74.29 |         81.90 |              79.05 |                  77.14 |               77.14 |               80.95 |          79.05 |              79.05 |              60.95 |           59.05 |
+---------------+-----------------------+-----------------+---------------+--------------------+------------------------+---------------------+---------------------+----------------+--------------------+--------------------+-----------------+
```

See a full experiment log from the [link](Experiment.md).

## Run the Tests

In the project root directory, run 'pytest' to test integrations:

```
pytest
```

or

```
.\pytest.sh
```

# Dependencies

Python 3.8+

This project might depend on some certain LLM Hosts in the future, such as Ollama, LangChain, etc.

# Contribute

## To Project

You can attend one of our remote meetings. We read papers and share ideas. Feel free to drop us a line.

## To Code

Excited to have you onboard! Here's how you can contribute:

1. Choose a Task. You can check out the [Project tasks](https://github.com/users/gokhanercan/projects/3), or look through the open issues or suggest your own improvements via [discussion board](https://github.com/gokhanercan/gen-atomic/discussions).
2. Fork the Project: Make a copy of our project on your GitHub.
3. Make Changes: Write your code and test it thoroughly. Ensure that pytest passes successfully.
4. Submit a Pull Request: Share your changes with us for review.

## To Datasets

Currently, datasets are version controlled. Please send a pull request for now (see 'src/data' folder). We are planning to use a data versioning system for this.
