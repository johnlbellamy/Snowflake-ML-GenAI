create or replace TABLE WINE.PUBLIC.WINE_QUALITY (
	FIXED_ACIDITY NUMBER(38,2),
	VOLATILE_ACIDITY NUMBER(38,3),
	CITRIC_ACID NUMBER(38,2),
	RESIDUAL_SUGAR NUMBER(38,2),
	CHLORIDES NUMBER(38,3),
	FREE_SULFUR_DIOXIDE NUMBER(38,1),
	TOTAL_SULFUR_DIOXIDE NUMBER(38,1),
	DENSITY NUMBER(38,6),
	PH NUMBER(38,2),
	SULPHATES NUMBER(38,2),
	ALCOHOL NUMBER(38,14),
	QUALITY NUMBER(38,0),
	TYPE VARCHAR(16777216)
);
