load csv with headers from "file:////synthea200_addresses.csv" as value
merge (s:Address {id:value.id}) set s += value;

load csv with headers from "file:////synthea200_allergies.csv" as value
merge (s:Allergy {id:value.id}) set s += value;

load csv with headers from "file:////synthea200_careplanes.csv" as value
merge (s:CarePlan {id:value.id}) set s += value;

load csv with headers from "file:////synthea200_conditions.csv" as value
merge (s:Condition {id:value.id}) set s += value;

load csv with headers from "file:////synthea200_drugs.csv" as value
merge (s:Drug {id:value.id}) set s += value;

load csv with headers from "file:////synthea200_encounters.csv" as value
merge (s:Encounter {id:value.id}) set s += value;

load csv with headers from "file:////synthea200_observations.csv" as value
merge (s:Observation {id:value.id}) set s += value;

load csv with headers from "file:////synthea200_organizations.csv" as value
merge (s:Organization {id:value.id}) set s += value;

load csv with headers from "file:////synthea200_patients.csv" as value
merge (s:Patient {id:value.id}) set s += value;

load csv with headers from "file:////synthea200_payers.csv" as value
merge (s:Payer {id:value.id}) set s += value;

load csv with headers from "file:////synthea200_procedures.csv" as value
merge (s:Procedure {id:value.id}) set s += value;

load csv with headers from "file:////synthea200_providers.csv" as value
merge (s:Provider {id:value.id}) set s += value;

load csv with headers from "file:////synthea200_specialities.csv" as value
merge (s:Speciality {id:value.id}) set s += value;

load csv with headers from "file:////synthea200_violations.csv" as value
merge (s:Violation {id:value.id}) set s += value;
