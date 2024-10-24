# FFIEC Data Transformation

## Table of Contents

- [FFIEC Data Transformation](#ffiec-data-transformation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
    - [Purpose](#purpose)
    - [Data Sources](#data-sources)
    - [Technology](#technology)
    - [Demonstrations](#demonstrations)
  - [Important: Installation Dependencies](#important-installation-dependencies)
    - [Environment Variables](#environment-variables)
      - [Setting Environment Variables](#setting-environment-variables)
    - [Docker Installation](#docker-installation)
      - [Why Use Docker?](#why-use-docker)
      - [Docker Commands](#docker-commands)
    - [Connecting to Postgres Locally](#connecting-to-postgres-locally)
  - [Problem Brief: Customer Segmentation](#problem-brief-customer-segmentation)
    - [Background](#background)
    - [Problem](#problem)
      - [Currently](#currently)
      - [Desired](#desired)
    - [Objectives](#objectives)
    - [Personas](#personas)
    - [Industry](#industry)
    - [Customers](#customers)
    - [Stakeholders](#stakeholders)
  - [Solution](#solution)
    - [Vision of Scope](#vision-of-scope)
    - [High Level Stories](#high-level-stories)
    - [KPIs (Key Performance Indicators)](#kpis-key-performance-indicators)
    - [High Level Acceptance Criteria](#high-level-acceptance-criteria)
    - [Strategic Direction](#strategic-direction)
    - [Technologies](#technologies)
    - [Out of Scope](#out-of-scope)
  - [Understanding the Data](#understanding-the-data)
    - [FFEIC.gov](#ffeicgov)
      - [Attributes](#attributes)
      - [Relationships](#relationships)
      - [Transforamtions](#transforamtions)
      - [Bank Holding Company Financials](#bank-holding-company-financials)
    - [Census.gov](#censusgov)
    - [Treasury.gov](#treasurygov)
    - [Data Dictionairies](#data-dictionairies)
  - [Implementation and Analysis](#implementation-and-analysis)
    - [Implementation Summary](#implementation-summary)
    - [Analysis Summary](#analysis-summary)
    - [FI Attributes](#fi-attributes)
    - [FI Relationships](#fi-relationships)
    - [FI Transformations](#fi-transformations)
    - [NAICS (North American Industry Classification System)](#naics-north-american-industry-classification-system)
    - [FIPS (Federal Information Processing Standards)](#fips-federal-information-processing-standards)
    - [FI Call Reports](#fi-call-reports)
  - [SQL Transformations](#sql-transformations)
    - [Transformation Summary](#transformation-summary)
    - [Script Files](#script-files)
    - [SQL Examples](#sql-examples)
      - [Functions](#functions)
      - [Insert Select Where not Exists](#insert-select-where-not-exists)
      - [Insert Select with Casting](#insert-select-with-casting)
  - [SQL Analysis](#sql-analysis)
    - [Institution Branches](#institution-branches)
    - [FFIEC Assets](#ffiec-assets)
    - [Transformation Trends](#transformation-trends)

## Introduction

### Purpose

This project primarily utilized SQL for insert, update, and delete statements. The intent is to showcase skills needed to transform datasets. This is not an in-depth demonstration of analyzing a dataset with SQL. While some analysis is performed, it is limited by the available data. The data is a subset to accomodate local storage limitations.

---

### Data Sources

Data was sourced from public data sources. No sensitive data is included.

Data sources include:

- FFIEC.gov
- Census.gov
- Treasury.gov

Source data can be located in `./imports` from the root directory. Data is label encoded. Data dictionaries have been supplied, located in `./documents` from the root directory.

A more in-depth explanation of the data can be found in the [Understanding the Data](#understanding-the-data) section.

---

### Technology

Technologies used throughout this project include Python, Docker, and the PostgreSQL dialect of SQL. The primary technology showcased is SQL, which is central for this project. While familiarity with the other technologies listed is beneficial, it is not required.

- **Python**\
  Chosen for the Pandas (data science) and SQLAlchemy (Object-Relational Mapping, or ORM) libraries.
- **Docker**\
  Chosen to provide a consistent environment for running the code.
- **PostgreSQL**\
  Chosen due to its feature rich dialect of SQL and its popularity as an open-source RDBMS.

---

### Demonstrations

Primarily focusing on SQL acumen in this project, demonstrations include the following:

- **DML (Data Manipulation Language)**\
  Operations include select, insert, update, delete, common table expressions, subqueries, window functions, etc.
- **DDL (Data Definition Language)**\
  Operations include table creation, table definitions, etc.
- **PL/pgSQL (Procedural Language/SQL)**\
  Procedures include variable declaration, loops, dynamic SQL, etc.

---

## Important: Installation Dependencies

### Environment Variables

This project is dependent upon several environment variables being set.

#### Setting Environment Variables

- Create a `.env` file in the root directory, then copy and paste the following variables into the file.

  > **Tip**: root directory is referred to as the directory containing main.py, Docker-related files, etc.

  ```python
  # These are for the database connection string.
  DB_DRIVER=postgresql+psycopg2   # database driver
  DB_USRNM=postgres               # username
  DB_PWD=****                     # change this to your password, "****" is not valid
  DB_HOST=postgres-db             # set for running Docker
  DB_PORT=5432                    # port number
  ```

---

### Docker Installation

This project was developed using Docker. If you do not have Docker installed locally or if you have not used Docker before, please refer to the following link.

[Install Docker](https://docs.docker.com/engine/install/)

> **Tip**: The installation guide will help make the installation process seamless.

#### Why Use Docker?

Using Docker helps maintain a consistent development environment, ensuring that all users will have the same experience.

#### Docker Commands

- **Start Containers**: `docker-compose up -d`\
  Starts the containers in detached mode, allowing the containers to run in the background without running any specified commands in the Dockerfile.
- **Build Image and Start Containers**: `docker-compose up --build`\
  Forces a build of the images and runs the commands specified in the `Dockerfile`.
- **Stop Containers**:\
  Press `ctrl+c` to disrupt a current process to return to the terminal.
- **Shut Down Containers**: `docker-compose down`\
  Stops and removes the containers when done.

---

### Connecting to Postgres Locally

To connect to the Postgres instance hosted in Docker, use your preferred database management tool.

> **Tip**: Port must be set to **5444**, not **5432**, for a successful connection. The Postgres instance was exposed externally for connections outside of the Docker network on a different port to avoid conflict for any pre-existing local Postgres instances.

---

## Problem Brief: Customer Segmentation

### Background

Financial Institutions (FIs) are federally regulated and are mandated to report information to the FFIEC (Federal Finance Institutions Examination Council). This is information publically avaliable at [FFIEC.gov](https://www.ffiec.gov/NPW). For peer group analysis, total assets reported on an FI's balance sheet is used as a basis.

To segment, total assets must be analyzed on a more granular level. Some subsections of total assest include consumer (also known as retail lending) and commercial assets.

Let us assume that the reason for targeting an FI is to offer products and services to support commercial lending activities. The following example is intended to provide further context.

> **Example**: On average, a [Credit Union (CU)](#customers) reports an 80/20 portfolio mixture compared to the average 50/50 reported by a [Community Bank (CB)](#customers). For example, a CU reporting $4B in total assets, which is a relatively larger institution, may only have $800MM in assets for their commercial portfolio.

On the balance sheet, consumer and commercial assets are subtotals of more granuarly reported assets. Proper segmentation of an FI, requires analysis of these assets.

FFIEC FI data is provided in two forms:

- [Institution Search](https://www.ffiec.gov/NPW)
- [Bulk Download](https://www.ffiec.gov/npw/FinancialReport/FinancialDataDownload)

---

### Problem

Research is conducted informally on an ad-hoc basis by marketing, sales, and product. Decentralized research leads to redundancy and inconsistent findings. Redundancy leads to teams spending more time on research and less time spent on primary responsibilities. Inconsistency leads to miscommunication and conflicting messages to executive leadership, leading to increased difficulty in decision-making.

#### Currently

Currently teams perform research on a per institution basis utilizing the institution search feature for simplicity and ease of use. To leverage data in bulk for a holistic view by team members, Excel or Power BI were used, which leads to tasks that are repetitious and time intensive.

Managing this data in Excel or Power BI leads to unnecessary maintenance overhead that includes refresh rates, broken links, and performing the tasks to transform refreshed data on a scheduled cadence that leads to integrity concerns.

#### Desired

Streamline FFIEC research with transparent data refreshes free of redundancy and centralized reporting for consistent findings. Scheduled updates with notifications are essential.

Streamlining this process, teams can access the same data in a consistent way in a centralized location. This will allow teams to spend more time on identifying actionable insights.

---

### Objectives

- Streamline redundant tasks of manually staging FFIEC data for analysis by 100%, allowing time allotted for analytics to focus solely on identifying actionable insights.
- Centralize reports for [teams](#problem) that align with corporate goals for consistent messaging to leadership.
- Remove the need for teams to externally search for FFIEC data.

---

### Personas

- **Product Analyst**:\
  Performs analysis on market data for TAM (Total Addressable Market) assessment and competitive research.
- **Marketing Analyst**:\
  Performs analysis for segmenting marketing campaigns.
- **Sales Consultant**:\
  Performs analysis for segmenting sales campaigns.

---

### Industry

The following industries are the primary target of business activities and the focal point of business analytics.

- 52211 - Commercial Banking
- 52213 - Credit Unions

> **Tip**: [NAICS] - [Industry]

---

### Customers

- **Community Banks**:\
  Community Banks are known for their local presence and relationships, distinct from larger banks such as Bank of America.
- **Credit Unions**:\
  Credit Unions are member-owned institutions, pooling the resources of its members, to provide credit services to the community.

---

### Stakeholders

- **Chief Product Officer**:\
  Leader of the product organization, responsible for product strategy and identifying the TAM.
- **Chief Marketing Officer**:\
  Leader of the marketing organization, responsible for marketing strategy for messaging to the TAM, opening the door for sales.
- **Chief Sales Officer**:\
  Leader of the sales organization, responsible for sales strategy for meeting revenue goals.

## Solution

### Vision of Scope

Store publicly reported FFIEC call reports for business analytics.

---

### High Level Stories

As a Product Manager, I want my team to be empowered to analyze market trends by performing a quarter over quarter trend analysis of FIs in our TAM. Our analytics of the market is informal and extremely flat. Material is stored in the form of notes, excel sheet, power points, and word documents.

As the Marketing Director, I want to increase the click through rate of campaigns. I have a list of contacts and that are targeted for marketing campaigns. Currently all contacts get the same messaging, equating to a poor click through rate. I would like to segment to increase click through rates. To increase click-through rates, a deeper analysis of lending products offered by FIs in our TAM is needed.

As a Sales Consultant, I want to increase the focus of the sales campaign by aligning with marketing segmentation to sell products and services more effectively.

---

### KPIs (Key Performance Indicators)

- Time spent gathering data to analyze.
- Segmenation of the market.

---

### High Level Acceptance Criteria

1. Centralize and store FFIEC quarterly reported call reports.
2. Implementation must provide flexibility for further extensions for the centralizing of competitive research, marketing, and sales information.
3. Extend a Jaspersoft read connection for distribution of initial reporting.
4. Extend select user read access to the database.

---

### Strategic Direction

This section provides context for long-term strategic direction.

The strategic direction includes the centralization of business intelligence. The primary focus of business intelligence revolves around FI data. FIs are the primary customer and focus for all teams including operation, marketing, sales, and product. Data for each team lives in silo and adds limited value in isolation. It is the desire of the business to tear down these silos to have a unified view. Each team except for product has a dedicated application for data entry. Through preliminary review, each application has a similar data structure and public api exposure for data extraction.

This solution is not intended to replace any existing applications or data recovery strategies.

---

### Technologies

This section describes the technologies chosen for this iteration.

TThe following technologies were chosen due to their current use and implementation.

- PostgreSQL (RMDB)
- TIBCO Jaspersoft (Reporting Software)

---

### Out of Scope

This section describes items that are not essential to realize immediate value to maintain focus on a quick deliverable. Items listed will be revisited for future iterations.

- **Web Scraping**:\
  Call reports are refreshed quarterly, and FI data is refreshed daily. An automated refresh is not needed currently.
- **Product, Marketing, and Sales Data**:\
  Product competitive intelligence is the only data that lacks formal storage and will continue to use spreadsheets until future iterations. Marketing data will continue to live in Hubspot soley and Sales data will continue to live in the CRM.
- **Data Visualization**:\
  Formal visualization via Microsoft Power BI will not be included in this iteration. SQL scripts will be written to generalize an output and distribute information via Jaspersoft in the form of csv.
- **API Support**:\
  API support for server or client-side operations is not needed at this time. Operations will be handled by the Data Integrity team.
- **Data Pipelines**:\
  Automated ETF (Export Transform Load) or ELT (Export Load Transform) is not needed currently due to the infrequent refresh requirements.

---

## Understanding the Data

This section provides context into the datasets used. All datasets can be located in `./imports`.

### FFEIC.gov

#### Attributes

The data are broken down into three files based on the status of the institution or branch.

- **CSV_ATTRIBUTES_ACTIVE**: Provides information describing the characteristics of open and active institutions.
- **CSV_ATTRIBUTES_CLOSED**: Povides the last instance of closed / failed institutions.
- **CSV_ATTRIBUTES_BRANCHES**: Provides the last instance of branches whose head office is listed in either the Active or Closed Attributes tables.

#### Relationships

- **CSV_RELATIONSHIPS**: Provides the history of ownership between two entities.

#### Transforamtions

- **CSV_TRANSFORMATIONS**: Provides information on mergers and failures.

#### Bank Holding Company Financials

- **BHCF20240630**: Provides information on reported financials as of 20240630.

---

### Census.gov

- **CSV_COUNTY_CODES**: Provides FIPS county codes.
- **CSV_STATE_CODES**: Provides FIPS state codes.

---

### Treasury.gov

- **CSV_COUNTRY_CODES**: Provides country codes.

### Data Dictionairies

- [**NPW Data Dictionary**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/documents/NPW%20Data%20Dictionary.pdf): Provides context for FFIEC attributes, relationships, and transformations.
- [**Financial Download Dictionary**](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fi-am-bl%2Fffiec-data-transformation%2Frefs%2Fheads%2Fmain%2Fdocuments%2FFinancial_Download_Dictionary.xlsx&wdOrigin=BROWSELINK): Provides context for BHCF data.

---

## Implementation and Analysis

### Implementation Summary

Code can be executed with `main.py`.

CSV import and script execution is configured by JSONs found in `./src/constants`. All configurations except the file path, which is dynamically added during code execution, can be modified in the JSON. A table-driven solution would provide a more scalable solution but was not demonstrated due to the added complexity.

---

### Analysis Summary

Analyst remained conservative in implementation. Requirements stated a need for flexibility in design for future iterations. Objectives listed did not explicitly state the exclusion of any data from the data source. Upon review of the csv files, data was label encoded. A supplementary data dictionary was provided. For analytical purposes, data was transformed to include a more descriptive naming convention. Analyst expanded data structure to include the details of the data dictionary. Label encoded values were retained for ease of use. Data structure was further normalized when feasible.

---

### FI Attributes

Attributes were delivered in three forms: active, branches, and closed. The data structure was the design and appeared to be split for the purpose of simplicity for the audience. This data was combined into one entity which equated to approximately 400k records.

Closed institutions were included by analyst due to assumed relevance for identifying market trends for institution closure. It is assumed there is potential correlation between economic indicators, institution size, and geographic location.

Branches were included by analyst due to assumed relevance for identifying a correlation between institution asset size, geographic locations, lending portfolio mixtures, and more. Analyst also assumes there is opportunity to identify trends in the health of the institution through review of financial indicators and market expansion (opening of new branches or locations).

Duplicity in the data set provided was present and was excluded from import.

> **Example**: Duplication in date fields where the source provided made a design decision to shift from storage of date as an integer in yyyymmdd to a datetime format.

Due to the overall size of the attribute data set and expanding due to label decoding, attribute data was divided for clarification purposes to exist in the following entities: `institutions`, `inst_dates`, `inst_ids`, `inst_cds`, `inst_indicators`, and `inst_addresses`. Design decision was made upon review of other data structures there would be a need for many addresses (e.g., billing address, service address, etc.), additional identifiers, and status codes (e.g, customer status, additional label encoding, etc.).

Inapplicable values were set to null from 0 and whitespace were removed.

---

### FI Relationships

Relationships were delivered in one form and was included by analyst due to assumed relevance. Data includes historical records for the relationship lifecycles between institutions. Due to label encoding, additional columns were added for ease of use. Data was not divided into addtional entities at this time.

This entity can be found as `inst_relationships`.

---

### FI Transformations

Transformations were delivered in one form and were included by analyst due to assume relevance. Data included historical records documenting institution transition. Analyst assumed relevance due to the nature of historical information documenting the discontinuation or transition of charters. Trends identified can provide market indicators that are pertitent for developing a forward-looking market strategy.

This entity can be found as `inst_transformations`.

---

### NAICS (North American Industry Classification System)

Upon review of the attributes dataset, the primary focus of business for the institution has been described with the use of NAICS (North American Industry Classification System). Analyst identified a source provider for this informaiton and has included it in the data model for analystical purposes. This data is not refreshed frequently.

This entity can be found as `naics`.

---

### FIPS (Federal Information Processing Standards)

Upon review of the attribute’s dataset, geographic information was partially described by abbreivation or an FIPS (Federal Information Processing Standards) code. This is industry standard, for future data sets that do not have any safeguards around location information, it has been included in this iteration for the purpose of standardization. This dataset is not refreshed frequently.

These entities can be found as `county_cds`, `state_cds`, and `country_cds`.

---

### FI Call Reports

Analyst obtained call report from FFIEC. Insufficient details were provided at this time for a full import of the dataset. Implementation was left open for expansion.

> **Please note**: Call reports are extremely detailed and reports data from the perspective of a BHC only, a consolidated view of Parent BHC, and more. This demonstration was limited to Total Assets of BHC for simplicity.

---

## SQL Transformations

### Transformation Summary

SQL showcasing the transformation of the dataset can be found in `./scripts`. This section offers a summary.

---

### Script Files

- [**001_preflight**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/001_preflight.sql): Fail safe to remove potential conflict, in the event load process is interuptted and then rexecuted.
- [**002_functions**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/002_functions.sql): Creates functions required for cleaning data.
- [**003_tables**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/003_tables.sql): Creation of production tables.
- [**004_tmp_tables**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/004_tmp_tables.sql): Creation of temporary table for isolating data transformation.
- [**005_attributes_inst**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/005_attributes_inst.sql): Tranforms data targeting `institutions`.
- [**006_attributes_ids**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/006_attributes_ids.sql): Tranforms data targeting `inst_ids`.
- [**007_attributes_dates**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/007_attributes_dates.sql): Tranforms data targeting `inst_attr_dates`.
- [**008_attributes_inds**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/008_attributes_inds.sql): Tranforms data targeting `inst_attr_indicators.
- [**009_attributes_codes**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/009_attributes_codes.sql): Tranforms data targeting `inst_attr_cds`.
- [**010_attributes_load**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/010_attributes_load.sql): Loads all transformed data sourced from attributes.
- [**011_relationships**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/011_relationships.sql): Transforms data targeting `inst_relationships`.
- [**012_relationships_load**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/012_relationships_load.sql): Loads tranformed data to `inst_relationships`.
- [**013_transformations**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/013_transformations.sql): Transforms and load data to `inst_transformations`.
- [**014_inst_addresses_load**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/014_inst_addresses_load.sql): Transforms and loads data to `inst_addresses`.
- [**015_fips_load**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/015_fips_load.sql): Transforms and loads data to `country_cds`, `state_cds`, and `country_cds`.
- [**016_naics**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/016_naics.sql): Transforms and load data to `naics`.
- [**017_call_reports**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/017_call_reports.sql): Transforms and loads data to `call_reports`.
- [**099_cleanup**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/099_cleanup.sql): Post deployment script for dropping all temporary tables and functions.
- [**100_drop_all_tables**](https://github.com/i-am-bl/ffiec-data-transformation/blob/main/scripts/100_drop_all_tables.sql): Scritps for removing all tables.

---

### SQL Examples

This section highlights more advanced SQL applied in this project and is not a comprehensive explanation of all SQL. Script files include comments, and all SQL used in this project.

#### Functions

Function features dynamic SQL that will execute a `select` statment. By specifying a table name and data type, a `select` operation is performed on `information_schema` to generate a list of columns in specified table with specified data type. The generated list is iterated through in a `loop`, executing specified validation query. In this case, the query was looking for columns that contained whitespace. Output returns a list of columns with a count of rows that contain whitespace.

```sql
create or replace function col_w_whitespace(input_schema_table_name text)
returns table(column_name text,record_count int) as $$
declare
  input_table_name text;
  input_schema text;
  input_table text;
  input_data_type text;
  sql_query text;
  rec record;
  result_count int;

begin
  input_schema := split_part(input_schema_table_name,'.',1);
  input_table := split_part(input_schema_table_name,'.',2);
  input_data_type := 'character varying';
  -- logging
  raise notice 'table_schema: %',input_schema;
  raise notice 'table: %',input_table;
  raise notice 'data_type: %', input_data_type;

  for rec in
    select cols.column_name
    from information_schema.columns cols
    where
      cols.table_schema = input_schema
    and
      cols.table_name = input_table
    and
      cols.data_type = input_data_type
  loop
    raise notice  'Column name: %', rec.column_name;
    sql_query := format(
      'select count(*) from %I where length(%I) <> length(trim(%I))',
      input_table,
      rec.column_name,
      rec.column_name
    );
    execute sql_query into result_count;
    if result_count > 0 then
      raise notice 'column: %s',rec.column_name;
      raise notice 'record_count: %s', result_count;
      return query select rec.column_name::text, result_count;
    end if;
  end loop;
  return;
end;
$$ language plpgsql;
```

#### Insert Select Where not Exists

Insert features a select from clause with a where not exist clause. The `where` clause executes a sub query on the target table, not allowing for an insert to be made where record already exists in the target table.

```sql
insert into call_reports(rssd_id, reporting_pd, tot_assets)
select "RSSD9001", cast(cast("RSSD9999" as varchar(20))as date), "BHCA2170"
from tmp_bhcf b
where not exists (
   select 1 from call_reports c
   where b."RSSD9001" = c.rssd_id and cast(cast(b."RSSD9999"as varchar(20))as date) = c.reporting_pd);
```

#### Insert Select with Casting

Conversion of data type can be peformed with `casting`. Certain data types do not allow for the direct conversion to another data type. To properly handle this, a nested `cast` can properly convert the data to a data type that is compatiable with with the desired data type.

```sql
insert into tmp_dates (rssd_id, start_date, end_date,open_date,commencement_date,termination_date,insured_date)
select
id_rssd,
cast(d_dt_start as date),
cast(d_dt_end as date),
cast(d_dt_open as date),
cast(cast(dt_exist_cmnc as varchar(10)) as date),
cast(cast(dt_exist_term as varchar(10)) as date),
cast(cast(dt_insur as varchar(10)) as date)
from tmp_attributes;
```

---

## SQL Analysis

Analysis is limited by available data. Data was intentionally restricted to limit the scope of this demonstration. A short analysis was conducted to add variety to skills showcased.

### Institution Branches

By reviewing both the count and location of branches, an assessment could be made of the FI's footprint in the market. With the use of window functions, a list of institutions can be generated with a running total of branches.

```sql
/*
By self-joining on the institutions table, we can partition to provide an output that produces a running count to quickly see how many branches an FI has.
*/

select i.rssd_id,i."name" head_office, ii."name" branch, row_number() over (partition by i."name" order by i."name", ii."name") branch_number
from institutions i
join institutions ii on i.rssd_id = ii.rssd_id_hd_off
limit 5;

 rssd_id | head_office          | branch                  | branch_number |
---------+----------------------+-------------------------+---------------+
  297734 | 1 JEFFERSON OFF      | 502 E OAK ST OFF        |             1 |
  362445 | 1 MERCHANTS PLAZA BR | 1015 E STATE ROAD 44 BR |             1 |
  362445 | 1 MERCHANTS PLAZA BR | 10841 E U S 36 BR       |             2 |
  362445 | 1 MERCHANTS PLAZA BR | 114 E WALNUT OFF        |             3 |
  362445 | 1 MERCHANTS PLAZA BR | 13756 N MERIDIAN ST OFF |             4 |

```

### FFIEC Assets

To perform a trend analysis, a minimum of three years is required. This is just a quick demonstration of the efforts to ingest fiscal information.

> **Please Note**: Total assts is reported in thousands (M)

```sql
select i."name" , i.entity_type , to_char(cr.tot_assets, 'FM$0,000,000') tot_assets_m, cr.reporting_pd
from institutions i
join call_reports cr  on i.rssd_id = cr.rssd_id and cr.tot_assets is not null limit 5;

 name               | entity_type                     | tot_assets_m | reporting_pd |
--------------------+---------------------------------+--------------+--------------+
 LAURITZEN CORP     | Financial Holding Company / BHC | $1,717,685   |   2024-06-30 |
 FORBRIGHT          | Bank Holding Company            | $7,016,795   |   2024-06-30 |
 GREEN DOT CORP     | Financial Holding Company / BHC | $5,517,354   |   2024-06-30 |
 FORESIGHT FNCL GRP | Financial Holding Company / BHC | $1,599,675   |   2024-06-30 |
 MVB FC             | Financial Holding Company / BHC | $3,297,283   |   2024-06-30 |
```

### Transformation Trends

Discontinued Charters for M&A (Merger & Acquisition) has significantly declined per year. A four-year average for the most recent four years was taken for comparison with the average of the previous four years. The most recent four-year average is down approximately 30% at 497 from 734 per year. This comparison was made due to the most recent unprecedented economic impact that is the lagging effects of inflation, montary policy restrictions, and COVID-19.

The year-over-year change reflects a decline at a decreasing rate. This is a potential indicator that the market is approaching equilibrium in this recession.

> **Please Note**: Analyst annualized 2024 using the straight growth rate method for comparison purposes.

```sql
/*
To provide a combined output of the different methods of aggregation, we can use common table expression with a cross join.
*/

with trends as (select
it.transformation,
(count(case when extract(year from it.transformation_date) = 2024 and it.transformation_cd = 1 then 1 end)/10)*12 ct_2024,
count(case when extract(year from it.transformation_date) = 2023 and it.transformation_cd = 1 then 1 end) ct_2023,
count(case when extract(year from it.transformation_date) = 2022 and it.transformation_cd = 1 then 1 end) ct_2022,
count(case when extract(year from it.transformation_date) = 2021 and it.transformation_cd = 1 then 1 end) ct_2021,
count(case when extract(year from it.transformation_date) = 2020 and it.transformation_cd = 1 then 1 end) ct_2020,
count(case when extract(year from it.transformation_date) = 2019 and it.transformation_cd = 1 then 1 end) ct_2019,
count(case when extract(year from it.transformation_date) = 2018 and it.transformation_cd = 1 then 1 end) ct_2018,
count(case when extract(year from it.transformation_date) = 2017 and it.transformation_cd = 1 then 1 end) ct_2017
from inst_transformations it
-- 1 == Charter Discontinued (Merger or Purchase & Assumption)
where extract(year from it.transformation_date) in (2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017)
group by  transformation
),
averages as
(select
round(avg(ct_2024 + ct_2023 + ct_2022 +ct_2021),4)avg_24_21,
round(avg(ct_2020 + ct_2019 + ct_2018 + ct_2017),4)avg_20_17
from trends
)
select a.*, '...'"...",
t.ct_2024"2024", t.ct_2024-t.ct_2023 chg23,
t.ct_2023"2023", t.ct_2023-t.ct_2022 chg22,
t.ct_2022"2022", t.ct_2022-t.ct_2021 chg21,
t.ct_2021"2021"
from trends t cross join averages a where t.transformation = 'Charter Discontinued';

 avg_24_21 | avg_20_17 | ... | 2024 | chg23 | 2023 | chg22 | 2022 | chg21 | 2021 |
-----------+-----------+-----+------+-------+------+-------+------+-------+------+
  496.7500 |  734.2500 | ... |  336 |  -123 |  459 |  -154 |  613 |    34 |  579 |
```
