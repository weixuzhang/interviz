from preprocess import *


################################## sparc_train ##################################
data_filepath = "data/sparc/train.json"
db_path = "data/sparc/database"

examples=generate_examples_lst(data_filepath, db_path)
with open("data/sparc/examples_train.json", "w") as out_file:
    json.dump(examples, out_file,indent=4)

schemas=generate_schemas_lst(data_filepath, db_path)
with open("data/sparc/schemas_train.json", "w") as out_file:
    json.dump(schemas, out_file,indent=4)

schema_examples=[sparc_add_schema(example) for example in examples]
# with open("data/sparc/schema_data.json", "w", encoding="utf-8") as f:
#     json.dump(schema_examples, f, ensure_ascii=False,indent=4)

interaction_examples=[sparc_add_interactions(example) for example in examples]
# with open("data/sparc/interactions_data.json", "w", encoding="utf-8") as f:
#     json.dump(interaction_examples, f, ensure_ascii=False,indent=4)

serialized_examples=[sparc_add_serialized_interactions(example) for example in examples]
# with open("data/sparc/serialized_data.json", "w", encoding="utf-8") as f:
#     json.dump(serialized_examples, f, ensure_ascii=False,indent=4)

serialized_str=["interactions:"+ example['interactions'] +" serialized_schema:"+example['serialized_schema'] for example in serialized_examples]
with open("data/sparc/serialized_str_train.json", "w", encoding="utf-8") as f:
    json.dump(serialized_str, f, ensure_ascii=False,indent=4)

# schema_str=["serialized_schema:"+example['serialized_schema'] for example in serialized_examples]
# with open("data/sparc/schema_str_train.json", "w", encoding="utf-8") as f:
#     json.dump(schema_str, f, ensure_ascii=False,indent=4)

print(len(examples)) 
print(len(schemas)) 

################################## sparc_dev ##################################
data_filepath = "data/sparc/dev.json"
db_path = "data/sparc/database"

examples=generate_examples_lst(data_filepath, db_path)
with open("data/sparc/examples_dev.json", "w") as out_file:
    json.dump(examples, out_file,indent=4)

schemas=generate_schemas_lst(data_filepath, db_path)
with open("data/sparc/schemas_dev.json", "w") as out_file:
    json.dump(schemas, out_file,indent=4)

schema_examples=[sparc_add_schema(example) for example in examples]
interaction_examples=[sparc_add_interactions(example) for example in examples]
serialized_examples=[sparc_add_serialized_interactions(example) for example in examples]

serialized_str=["interactions:"+ example['interactions'] +" serialized_schema:"+example['serialized_schema'] for example in serialized_examples]
with open("data/sparc/serialized_str_dev.json", "w", encoding="utf-8") as f:
    json.dump(serialized_str, f, ensure_ascii=False,indent=4)

# schema_str=["serialized_schema:"+example['serialized_schema'] for example in serialized_examples]
# with open("data/sparc/schema_str_dev.json", "w", encoding="utf-8") as f:
#     json.dump(schema_str, f, ensure_ascii=False,indent=4)

print(len(examples)) 
print(len(schemas)) 
