# About gen-atomic

LLM code <u>**gen**</u>eration and benchmarking framework aiming to support a wide range of <u>**atom**</U>ic artifacts, from compiled languages to semi-structured markups.

Here is the initial sketch. More will be here...
![image](https://github.com/gokhanercan/gen-atomic/assets/1479777/912bada9-f907-4a4a-9ea7-341d3da60403)
https://pitch.com/v/gen-atomic-tyqhkw

# Getting Started

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
+----+----------+--------------------+---------------------------+----------+---------------------------------------------------------------------+-------------------------------------------------------------------+
|    | Type     | Name               | Case                      | Passed   | Generated Code                                                      | Desc                                                              |
|----+----------+--------------------+---------------------------+----------+---------------------------------------------------------------------+-------------------------------------------------------------------|
|  1 | RegexVal | Email              | CC-> mail@gokhanercan.com | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic email address                                             |
|  2 | RegexVal | Email              | CC-> amojtehed@gmail.com  | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic email address                                             |
|  3 | RegexVal | Email              | IC-> dsadsadasda          | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic email address                                             |
|  4 | RegexVal | Email              | IC-> http://invalidaemail | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Generic email address                                             |
|  5 | RegexVal | PriceInTurkishLira | CC-> 1.550,5              | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
|  6 | RegexVal | PriceInTurkishLira | CC-> 100                  | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
|  7 | RegexVal | PriceInTurkishLira | IC-> 090                  | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
|  8 | RegexVal | PriceInTurkishLira | IC-> 0,23,34              | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
|  9 | RegexVal | PriceInTurkishLira | IC-> 12.11,23             | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
| 10 | RegexVal | PriceInTurkishLira | IC-> aaaa                 | X        | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
| 11 | RegexVal | PriceInTurkishLira | IC-> mail@gokhan.com      | OK       | [CODE] ^[a-zA-Z0-9.!#$%&'*+ ..[TRIM].. ,61}[a-zA-Z0-9])?)*$ [/CODE] | Price formatted with thousands seperator in Turkish Lira currency |
+----+----------+--------------------+---------------------------+----------+---------------------------------------------------------------------+-------------------------------------------------------------------+
```

# Dependencies

Python 3.6+ (currently)

This project might depend on some certain LLM Hosts in the future, such as Ollama, LangChain, etc.

# Contribute

## To Code

1. Excited to have you onboard! Here's how you can contribute:
2. Fork the Project: Make a copy of our project on your GitHub.
3. Choose a Task: Look through the open issues or suggest your own improvements. Check out the [Project tasks](https://github.com/users/gokhanercan/projects/3).
4. Make Changes: Write your code and test it thoroughly.
5. Submit a Pull Request: Share your changes with us for review.

## To Datasets

Currently, datasets are version controlled. Please, send a pull request for now (see 'src/data folder). We are planning to use a ata versioning system for this.
