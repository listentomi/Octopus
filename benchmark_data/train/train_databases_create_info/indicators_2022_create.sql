CREATE TABLE Country (
    CountryCode TEXT,
    ShortName TEXT,
    TableName TEXT,
    LongName TEXT,
    Alpha2Code TEXT,
    CurrencyUnit TEXT,
    SpecialNotes TEXT,
    Region TEXT,
    IncomeGroup TEXT,
    Wb2Code TEXT,
    NationalAccountsBaseYear TEXT,
    NationalAccountsReferenceYear TEXT,
    SnaPriceValuation TEXT,
    LendingCategory TEXT,
    OtherGroups TEXT,
    SystemOfNationalAccounts TEXT,
    AlternativeConversionFactor TEXT,
    PppSurveyYear TEXT,
    BalanceOfPaymentsManualInUse TEXT,
    ExternalDebtReportingStatus TEXT,
    SystemOfTrade TEXT,
    GovernmentAccountingConcept TEXT,
    ImfDataDisseminationStandard TEXT,
    LatestPopulationCensus TEXT,
    LatestHouseholdSurvey TEXT,
    SourceOfMostRecentIncomeAndExpenditureData TEXT,
    VitalRegistrationComplete TEXT,
    LatestAgriculturalCensus TEXT,
    LatestIndustrialData NUMERIC,
    LatestTradeData NUMERIC,
    LatestWaterWithdrawalData NUMERIC);
CREATE TABLE CountryNotes (
    Countrycode TEXT,
    Seriescode TEXT,
    Description TEXT);
CREATE TABLE Series (
    SeriesCode TEXT,
    Topic TEXT,
    IndicatorName TEXT,
    ShortDefinition TEXT,
    LongDefinition TEXT,
    UnitOfMeasure TEXT,
    Periodicity TEXT,
    BasePeriod TEXT,
    OtherNotes NUMERIC,
    AggregationMethod TEXT,
    LimitationsAndExceptions TEXT,
    NotesFromOriginalSource TEXT,
    GeneralComments TEXT,
    Source TEXT,
    StatisticalConceptAndMethodology TEXT,
    DevelopmentRelevance TEXT,
    RelatedSourceLinks TEXT,
    OtherWebLinks NUMERIC,
    RelatedIndicators NUMERIC,
    LicenseType TEXT);
CREATE TABLE Indicators (
    CountryName TEXT,
    CountryCode TEXT,
    IndicatorName TEXT,
    IndicatorCode TEXT,
    Year INTEGER,
    Value NUMERIC);
CREATE TABLE SeriesNotes (
    Seriescode TEXT,
    Year TEXT,
    Description TEXT);
CREATE TABLE Footnotes (
    Countrycode TEXT,
    Seriescode TEXT,
    Year TEXT,
    Description TEXT);
