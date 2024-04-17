# About gen-atomic

[![Python application](https://github.com/gokhanercan/gen-atomic/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/gokhanercan/gen-atomic/actions/workflows/python-app.yml)
[![Demo](https://img.shields.io/badge/Streamlit_Demo-Visit-blue.svg)](https://gen-atomic.streamlit.app/)

LLM code <u>**gen**</u>eration and benchmarking framework aiming to support a wide range of <u>**atom**</U>ic artifacts, from compiled languages to semi-structured markups.

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
-- CASE RESULTS --
+----+----------+--------------------------+-----------------------------------------+----------+---------------------------------------------------------------------+-------------------------------------------------------------------+
|    | Type     | Name                     | Case                                    | Passed   | Generated Code                                                      | Desc                                                              |
|----+----------+--------------------------+-----------------------------------------+----------+---------------------------------------------------------------------+-------------------------------------------------------------------|
|  1 | RegexVal | Email                    | CC-> mail@gokhanercan.com               | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic email address                                             |
|  2 | RegexVal | Email                    | CC-> amojtehed@gmail.com                | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic email address                                             |
|  3 | RegexVal | Email                    | IC-> dsadsadasda                        | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic email address                                             |
|  4 | RegexVal | Email                    | IC-> http://invalidaemail               | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic email address                                             |
|  5 | RegexVal | EmailRFC5322             | CC-> some+test@gmail.com                | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | General email regex compliant to RFC 5322 official standard       |
|  6 | RegexVal | EmailRFC5322             | CC-> _valid@mail.com                    | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | General email regex compliant to RFC 5322 official standard       |
|  7 | RegexVal | EmailRFC5322             | CC-> stuart.sillitoe@prodirectsport.net | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | General email regex compliant to RFC 5322 official standard       |
|  8 | RegexVal | EmailRFC5322             | IC-> invalidÂ£@domain.com               | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | General email regex compliant to RFC 5322 official standard       |
|  9 | RegexVal | EmailRFC5322             | IC-> valid%$@domain.com                 | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | General email regex compliant to RFC 5322 official standard       |
| 10 | RegexVal | PriceInTurkishLira       | CC-> 1.550,5                            | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
| 11 | RegexVal | PriceInTurkishLira       | CC-> 100                                | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
| 12 | RegexVal | PriceInTurkishLira       | IC-> 090                                | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
| 13 | RegexVal | PriceInTurkishLira       | IC-> 0,23,34                            | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
| 14 | RegexVal | PriceInTurkishLira       | IC-> 12.11,23                           | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
| 15 | RegexVal | PriceInTurkishLira       | IC-> aaaa                               | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
| 16 | RegexVal | PriceInTurkishLira       | IC-> mail@gokhan.com                    | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
| 17 | RegexVal | IPAddressV4              | CC-> 127.0.0.1                          | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic IP address in IPv4 format, 4 blocks of numbers            |
| 18 | RegexVal | IPAddressV4              | CC-> 192.1.1.12                         | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic IP address in IPv4 format, 4 blocks of numbers            |
| 19 | RegexVal | IPAddressV4              | IC-> 127,0,0,1                          | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic IP address in IPv4 format, 4 blocks of numbers            |
| 20 | RegexVal | IPAddressV4              | IC-> 127:0:0:1                          | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic IP address in IPv4 format, 4 blocks of numbers            |
| 21 | RegexVal | IPAddressV4              | IC-> 1.0.0.0.0.0                        | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic IP address in IPv4 format, 4 blocks of numbers            |
| 22 | RegexVal | IPAddressV4              | IC-> 0,23,34                            | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic IP address in IPv4 format, 4 blocks of numbers            |
| 23 | RegexVal | IPAddressV4              | IC-> 12.11,23                           | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic IP address in IPv4 format, 4 blocks of numbers            |
| 24 | RegexVal | IPAddressV4              | IC-> gokhan                             | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic IP address in IPv4 format, 4 blocks of numbers            |
| 25 | RegexVal | IPAddressV4              | IC-> 2001:db8:1234::1                   | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic IP address in IPv4 format, 4 blocks of numbers            |
| 26 | RegexVal | LocalhostIPv4OrLocalText | CC-> 127.0.0.1                          | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Local IP address or 'localhost' text                              |
| 27 | RegexVal | LocalhostIPv4OrLocalText | CC-> localhost                          | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Local IP address or 'localhost' text                              |
| 28 | RegexVal | LocalhostIPv4OrLocalText | IC-> 192.1.1.12                         | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Local IP address or 'localhost' text                              |
+----+----------+--------------------------+-----------------------------------------+----------+---------------------------------------------------------------------+-------------------------------------------------------------------+
+---------------+----------------+
|               |   Accuracy (%) |
|---------------+----------------|
| CorrectCase   |          45.45 |
| IncorrectCase |          88.24 |
| Overall       |          71.43 |
+---------------+----------------+

Process finished with exit code 0

```

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

Currently, datasets are version controlled. Please send a pull request for now (see 'src/data folder). We are planning to use a data versioning system for this.
