# Documentation

## Project Glossary

The gen-atomic project defines a set of **atomic** **language units** (aka LangUnit). Please refer to the Terms in the project glossary if this doesn't make any sense:


| Term          | Description                                                                                                       | Abbr     | Example                     |
| --------------- | ------------------------------------------------------------------------------------------------------------------- | ---------- | ----------------------------- |
| Grammar       | Parsable syntax and structure rules of string statements.                                                         |          |                             |
| Language      | Any full or semi structured programming, markup, expression or meta language that has a clearly defined_grammar_. | Lang     |                             |
| Atomic        | Reusable and fine-grained structures of languages that cannot be decomposable into smaller parts.                 |          |                             |
| Unit          | Any_atomic_ unit that has a clearly defined_schema_.                                                              |          | Expression, Function, Class |
| Schema        | Clearly defined input/output data types                                                                           |          | (str)->bool                 |
| Language Unit | A specific_unit_ of a language that supports easy evaluation and execution                                        | LangUnit | Regex-Validator             |
| Code          | An instance of a_LangUnit_ aiming to provide a specific described functionality                                   |          | `^.{3}$`                    |

Here is a list of the LangUnit types that gen-atomic is planning to support. LangUnits denoted in _{Language}-{Unit}_ format.


| Lang-Unit                | Description                                            | Lang   | Schema              | UnitType   | Example                               |
| -------------------------- | -------------------------------------------------------- | -------- | --------------------- | ------------ | --------------------------------------- |
| Regex-Validator          | Validation expressions of the Regex language           | Regex  | f(str)->bool        | Expression | `^.{3}$`                              |
| Python-StringTransformer | String transformer function of the Python language     | Python | f(str)->str         | Function   | `def(x:str):return "Transformed" + x` |
| Java-StringTransformer   | String transformer function of the Java language       | Java   | f(str)->str         | Function   | `f(x){return "Transformed" + x;}`     |
| JS-StringTransformer     | String transformer function of the Javascript language | JS     | f(str)->str         | Function   | `f(x){return "Transformed" + x;}`     |
| SQL-SelectQuery          | Select query of universal ANSI-SQL                     | SQL    | f(TableSchema)->str | Query      | `select * from members`               |
| TSQL-SelectQuery         | Select query specific to MS SQL Server                 | TSQL   | f(TableSchema)->str | Query      | `select TOP 10 * from members`        |

Here are some example schema explanations:


| Schema              | Description                                                                                         |
| --------------------- | ----------------------------------------------------------------------------------------------------- |
| f(str)->str         | A function unit that accepts a string input and returns a string                                    |
| f(str)->bool        | A function unit that accepts a string input and returns a bool output                               |
| f([str])->str       | A function unit that accepts a string array and returns a string                                    |
| f(TableSchema)->str | A function unit that accepts a metadata object that represent a database table and returns a string |

## Implementation Notes

### Types of Plugins


| PluginType        | Base Type         | Factory         | Example(s)          | Example Key | Desc. |
| ------------------- | ------------------- | ----------------- | --------------------- | ------------- | ------- |
| **Model**         | ModelBase         | ModelFactory    | RandomModel         | np-random   |       |
| **ModelProvider** | ModelProviderBase | ModelFactory    | OllamaModelProvider | ol          |       |
| **LangUnit**      | LangUnit          | LangUnitFactory | RegexVal, SqlSelect | _n/a_       |       |

(*) np means NoProvider. ModelProviders are inherited from ModelBase.

### Types, Names, and Identifiers

Some notes on the Type and Identity system of the library that can help you implement plugins.


| Impl. Type           | Name/ModelName/ConfigName or SubModel?? | PlainName  | TypeName                                                 | Key          | ConfigName | ConfigKey    |
| ---------------------- | ----------------------------------------- | ------------ | ---------------------------------------------------------- | -------------- | ------------ | -------------- |
| Standalone Model Ex. | RandomModel                             | Random     | models.RandomModel.RandomModel                           | np-random    | _n\a_      | np-random    |
| ModelProvider Ex.    | Codellama?                              | Codellama? | models.providers.OllamaModelProvider.OllamaModelProvider | ol-codellama | _n\a_      | ol-random:7b |
