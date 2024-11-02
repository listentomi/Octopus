CREATE TABLE "country" (
"country_code" TEXT,
  "short_name" TEXT,
  "table_name" TEXT,
  "long_name" TEXT,
  "2_alpha_code" TEXT,
  "currency_unit" TEXT,
  "special_notes" TEXT,
  "region" TEXT,
  "income_group" TEXT,
  "wb_2_code" TEXT,
  "national_accounts_base_year" TEXT,
  "national_accounts_reference_year" REAL,
  "sna_price_valuation" TEXT,
  "lending_category" TEXT,
  "other_groups" TEXT,
  "system_of_national_accounts" TEXT,
  "balance_of_payments_manual_in_use" TEXT,
  "external_debt_reporting_status" TEXT,
  "system_of_trade" TEXT,
  "government_accounting_concept" TEXT,
  "imf_data_dissemination_standard" TEXT,
  "latest_population_census" TEXT,
  "latest_household_survey" TEXT,
  "source_of_most_recent_income_and_expenditure_data" TEXT,
  "vital_registration_complete" TEXT,
  "latest_agricultural_census" TEXT,
  "latest_industrial_data" REAL,
  "latest_trade_data" REAL
);
CREATE TABLE "country_notes" (
"country_code" TEXT,
  "indicator_code" TEXT,
  "description" TEXT
);
CREATE TABLE "footnotes" (
"country_code" TEXT,
  "indicator_code" TEXT,
  "year" TEXT,
  "description" TEXT
);
CREATE TABLE "series" (
"indicator_code" TEXT,
  "topic" TEXT,
  "indicator_name" TEXT,
  "short_definition" TEXT,
  "long_definition" TEXT,
  "unit_of_measure" TEXT,
  "periodicity" TEXT,
  "base_period" TEXT,
  "other_notes" TEXT,
  "aggregation_method" TEXT,
  "limitations_and_exceptions" TEXT,
  "notes_from_original_source" TEXT,
  "general_comments" TEXT,
  "source" TEXT,
  "statistical_concept_and_methodology" TEXT,
  "development_relevance" TEXT,
  "related_source_links" TEXT,
  "other_web_links" TEXT,
  "related_indicators" TEXT,
  "license_type" TEXT
);
CREATE TABLE "series_notes" (
"indicator_code" TEXT,
  "year" TEXT,
  "description" TEXT
);
CREATE TABLE "indicators" (
"country_name" TEXT,
  "country_code" TEXT,
  "indicator_name" TEXT,
  "indicator_code" TEXT,
  "year" INTEGER,
  "value" REAL
);
